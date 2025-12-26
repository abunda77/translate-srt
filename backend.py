import os
import time
import requests
import srt
from dotenv import load_dotenv

load_dotenv()

class DeepLTranslator:
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv("DEEPL_API_KEY")
        if not self.api_key:
            raise ValueError("API Key not found. Please set DEEPL_API_KEY in .env or pass it to the constructor.")
        
        self.base_url = "https://api-free.deepl.com/v2"
        # Check if key indicates Pro (usually doesn't end in :fx for Pro, but Free keys end in :fx)
        if not self.api_key.endswith(":fx"):
             self.base_url = "https://api.deepl.com/v2"

    def validate_api_key(self):
        """Checks if the API key is valid by querying usage."""
        try:
            response = requests.get(
                f"{self.base_url}/usage",
                headers={"Authorization": f"DeepL-Auth-Key {self.api_key}"}
            )
            response.raise_for_status()
            return True, response.json()
        except requests.exceptions.RequestException as e:
            return False, str(e)

    def translate_text_content(self, text, target_lang):
        """Translates a simple string or list of strings."""
        try:
            response = requests.post(
                f"{self.base_url}/translate",
                headers={"Authorization": f"DeepL-Auth-Key {self.api_key}"},
                data={
                    "text": text,
                    "target_lang": target_lang
                }
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
            response = requests.post(
                f"{self.base_url}/document",
                headers={"Authorization": f"DeepL-Auth-Key {self.api_key}"},
                data={"target_lang": target_lang},
                files={"file": f}
            )
        
        response.raise_for_status()
        data = response.json()
        doc_id = data["document_id"]
        doc_key = data["document_key"]
        
        # 2. Check Status
        while True:
            status_response = requests.post(
                f"{self.base_url}/document/{doc_id}",
                headers={"Authorization": f"DeepL-Auth-Key {self.api_key}"},
                data={"document_key": doc_key}
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
        download_response = requests.post(
            f"{self.base_url}/document/{doc_id}/result",
            headers={"Authorization": f"DeepL-Auth-Key {self.api_key}"},
            data={"document_key": doc_key},
            stream=True
        )
        download_response.raise_for_status()
        
        with open(output_path, "wb") as f:
            for chunk in download_response.iter_content(chunk_size=8192):
                f.write(chunk)

