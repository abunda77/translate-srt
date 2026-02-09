import os
import time
import requests
import srt
from dotenv import load_dotenv
from PIL import Image
import pytesseract

load_dotenv()

# Setup Tesseract OCR path (especially for Windows)
try:
    from tesseract_config import setup_tesseract
    setup_tesseract()
except ImportError:
    pass  # tesseract_config.py not found, assume tesseract is in PATH

from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

class DeepLTranslator:
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv("DEEPL_API_KEY")
        if not self.api_key:
            raise ValueError("API Key not found. Please set DEEPL_API_KEY in .env or pass it to the constructor.")
        
        self.base_url = "https://api-free.deepl.com/v2"
        # Check if key indicates Pro (usually doesn't end in :fx for Pro, but Free keys end in :fx)
        if not self.api_key.endswith(":fx"):
             self.base_url = "https://api.deepl.com/v2"

        # Initialize session with retry strategy
        self.session = requests.Session()
        retry_strategy = Retry(
            total=3,  # Total number of retries
            backoff_factor=1,  # Wait 1s, 2s, 4s between retries
            status_forcelist=[429, 500, 502, 503, 504],  # Retry on these errors
            allowed_methods=["HEAD", "GET", "OPTIONS", "POST"]  # Retry on these methods
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("https://", adapter)
        self.session.mount("http://", adapter)
        
        # Standard timeout (connect, read)
        self.timeout = (10, 30)

    def validate_api_key(self):
        """Checks if the API key is valid by querying usage."""
        try:
            response = self.session.get(
                f"{self.base_url}/usage",
                headers={"Authorization": f"DeepL-Auth-Key {self.api_key}"},
                timeout=self.timeout
            )
            response.raise_for_status()
            return True, response.json()
        except requests.exceptions.RequestException as e:
            return False, str(e)

    def translate_text_content(self, text, target_lang):
        """Translates a simple string or list of strings."""
        try:
            response = self.session.post(
                f"{self.base_url}/translate",
                headers={"Authorization": f"DeepL-Auth-Key {self.api_key}"},
                data={
                    "text": text,
                    "target_lang": target_lang
                },
                timeout=self.timeout
            )
            response.raise_for_status()
            result = response.json()
            return [t["text"] for t in result["translations"]]
        except Exception as e:
            raise Exception(f"Translation failed: {str(e)}")

    def translate_txt_file(self, filepath, target_lang, output_path):
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        
        # DeepL can handle large text, but it's better to split if huge. 
        # For simplicity, assuming reasonable size or DeepL handles it.
        # Actually DeepL has a limit per request (128KB). 
        # If content is large, we should split. For now, let's assume it fits or simple split by lines.
        
        translated_texts = self.translate_text_content([content], target_lang)
        
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(translated_texts[0])
            
    def translate_srt_file(self, filepath, target_lang, output_path):
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
            
        subs = list(srt.parse(content))
        
        # Extract text to translate
        texts_to_translate = [sub.content for sub in subs]
        
        # Batching to avoid hitting request limits or size limits
        # DeepL allows up to 50 texts per request.
        batch_size = 50
        translated_texts = []
        
        for i in range(0, len(texts_to_translate), batch_size):
            batch = texts_to_translate[i:i+batch_size]
            translated_batch = self.translate_text_content(batch, target_lang)
            translated_texts.extend(translated_batch)
            
        # Reconstruct SRT
        for sub, trans_text in zip(subs, translated_texts):
            sub.content = trans_text
            
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(srt.compose(subs))

    def translate_document(self, filepath, target_lang, output_path):
        """Handles DOCX and PDF using DeepL Document API."""
        
        # 1. Upload
        with open(filepath, "rb") as f:
            response = self.session.post(
                f"{self.base_url}/document",
                headers={"Authorization": f"DeepL-Auth-Key {self.api_key}"},
                data={"target_lang": target_lang},
                files={"file": f},
                timeout=self.timeout
            )
        
        response.raise_for_status()
        data = response.json()
        doc_id = data["document_id"]
        doc_key = data["document_key"]
        
        # 2. Check Status
        while True:
            status_response = self.session.post(
                f"{self.base_url}/document/{doc_id}",
                headers={"Authorization": f"DeepL-Auth-Key {self.api_key}"},
                data={"document_key": doc_key},
                timeout=self.timeout
            )
            status_response.raise_for_status()
            status_data = status_response.json()
            
            status = status_data["status"]
            if status == "done":
                break
            elif status == "error":
                raise Exception(f"Document translation error: {status_data.get('error_message')}")
            
            # Wait before polling again
            seconds = status_data.get("seconds_remaining", 0)
            if seconds is None: seconds = 2
            time.sleep(min(seconds, 5)) # Sleep at least a bit, but max 5s to be responsive
            
        # 3. Download
        download_response = self.session.post(
            f"{self.base_url}/document/{doc_id}/result",
            headers={"Authorization": f"DeepL-Auth-Key {self.api_key}"},
            data={"document_key": doc_key},
            stream=True,
            timeout=(10, 300) # Longer timeout for download
        )
        download_response.raise_for_status()
        
        with open(output_path, "wb") as f:
            for chunk in download_response.iter_content(chunk_size=8192):
                f.write(chunk)

    def extract_text_from_image(self, image_path_or_pil, lang='eng+ind'):
        """
        Extracts text from an image using Tesseract OCR.
        
        Args:
            image_path_or_pil: Either a file path (str) or a PIL Image object
            lang: Language(s) for OCR. Default is 'eng+ind' (English + Indonesian)
                  Common options: 'eng', 'ind', 'eng+ind', 'jpn', 'chi_sim', etc.
        
        Returns:
            str: Extracted text from the image
        """
        import tempfile
        temp_file = None
        
        try:
            # If it's a string path, open the image
            if isinstance(image_path_or_pil, str):
                print(f"[DEBUG] Opening image from path: {image_path_or_pil}")
                image = Image.open(image_path_or_pil)
            else:
                # Assume it's already a PIL Image
                print(f"[DEBUG] Using PIL Image object")
                image = image_path_or_pil
            
            print(f"[DEBUG] Original image mode: {image.mode}, size: {image.size}")
            
            # Convert image to RGB if it's not already
            # This fixes issues with RGBA, P, L, and other modes from clipboard
            if image.mode not in ('RGB', 'L'):
                print(f"[DEBUG] Converting image from {image.mode} to RGB...")
                # Convert RGBA to RGB with white background
                if image.mode == 'RGBA':
                    background = Image.new('RGB', image.size, (255, 255, 255))
                    background.paste(image, mask=image.split()[3])  # Use alpha channel as mask
                    image = background
                    print(f"[DEBUG] RGBA converted to RGB with white background")
                else:
                    # Convert other modes to RGB
                    image = image.convert('RGB')
                    print(f"[DEBUG] Converted to RGB using convert() method")
            else:
                print(f"[DEBUG] Image already in compatible mode: {image.mode}")
            
            print(f"[DEBUG] Final image mode before OCR: {image.mode}")
            
            # Try direct OCR first
            try:
                print(f"[DEBUG] Attempting direct OCR with language: {lang}")
                text = pytesseract.image_to_string(image, lang=lang)
                print(f"[DEBUG] Direct OCR completed successfully, extracted {len(text)} characters")
                return text.strip()
            except Exception as direct_error:
                print(f"[DEBUG] Direct OCR failed: {str(direct_error)}")
                print(f"[DEBUG] Trying alternative method: saving to temp file first...")
                
                # Fallback: Save to temporary file and OCR from file
                temp_file = tempfile.NamedTemporaryFile(suffix='.png', delete=False)
                temp_path = temp_file.name
                temp_file.close()
                
                print(f"[DEBUG] Saving image to temp file: {temp_path}")
                image.save(temp_path, 'PNG')
                
                print(f"[DEBUG] Attempting OCR from temp file...")
                text = pytesseract.image_to_string(temp_path, lang=lang)
                print(f"[DEBUG] Temp file OCR completed successfully, extracted {len(text)} characters")
                
                # Clean up temp file
                try:
                    os.unlink(temp_path)
                    print(f"[DEBUG] Temp file cleaned up")
                except:
                    pass
                
                return text.strip()
                
        except pytesseract.TesseractNotFoundError:
            raise Exception("Tesseract OCR not found! Please install Tesseract OCR first.\n\nDownload from: https://github.com/UB-Mannheim/tesseract/wiki")
        except Exception as e:
            print(f"[DEBUG] OCR Error: {type(e).__name__}: {str(e)}")
            import traceback
            traceback.print_exc()
            raise Exception(f"OCR failed: {str(e)}")
        finally:
            # Clean up temp file if it exists
            if temp_file and os.path.exists(temp_file.name):
                try:
                    os.unlink(temp_file.name)
                except:
                    pass


