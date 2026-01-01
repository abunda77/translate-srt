import os
import threading
import customtkinter as ctk
from tkinter import filedialog, messagebox
from backend import DeepLTranslator
from dotenv import load_dotenv
from PIL import ImageGrab, Image
import io
from translation_result_window import TranslationResultWindow, OCRResultWindow

# Load env to get key if available
load_dotenv()

class DeepLApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("DeepL Document Translator")
        self.geometry("700x800")
        
        # Set theme
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("blue")

        # Variables
        self.api_key_var = ctk.StringVar(value=os.getenv("DEEPL_API_KEY", ""))
        self.file_path_var = ctk.StringVar()
        self.target_lang_var = ctk.StringVar(value="ID") # Default to Indonesian
        self.status_var = ctk.StringVar(value="Ready")
        
        # OCR Variables
        self.image_path_var = ctk.StringVar()
        self.ocr_lang_var = ctk.StringVar(value="eng+ind")
        self.ocr_text = ""
        self.pasted_image = None
        
        self.create_widgets()

    def create_widgets(self):
        # --- Header ---
        self.header_frame = ctk.CTkFrame(self)
        self.header_frame.pack(pady=20, padx=20, fill="x")
        
        self.title_label = ctk.CTkLabel(self.header_frame, text="DeepL Translator", font=("Roboto", 24, "bold"))
        self.title_label.pack(side="left", padx=10)

        # --- API Key Section ---
        self.api_frame = ctk.CTkFrame(self)
        self.api_frame.pack(pady=10, padx=20, fill="x")
        
        self.api_label = ctk.CTkLabel(self.api_frame, text="API Key:")
        self.api_label.pack(side="left", padx=10)
        
        self.api_entry = ctk.CTkEntry(self.api_frame, textvariable=self.api_key_var, width=400, show="*")
        self.api_entry.pack(side="left", padx=10)
        
        # --- File Selection ---
        self.file_frame = ctk.CTkFrame(self)
        self.file_frame.pack(pady=10, padx=20, fill="x")
        
        self.file_btn = ctk.CTkButton(self.file_frame, text="Select File", command=self.select_file)
        self.file_btn.pack(side="left", padx=10, pady=10)
        
        self.file_label = ctk.CTkLabel(self.file_frame, textvariable=self.file_path_var, text_color="gray")
        self.file_label.pack(side="left", padx=10)

        # --- Language Selection ---
        self.lang_frame = ctk.CTkFrame(self)
        self.lang_frame.pack(pady=10, padx=20, fill="x")
        
        self.lang_label = ctk.CTkLabel(self.lang_frame, text="Target Language:")
        self.lang_label.pack(side="left", padx=10)
        
        # Common DeepL languages
        languages = ["ID", "EN-US", "EN-GB", "DE", "FR", "ES", "IT", "JA", "ZH", "RU", "PT-BR", "PT-PT"]
        self.lang_menu = ctk.CTkOptionMenu(self.lang_frame, variable=self.target_lang_var, values=languages)
        self.lang_menu.pack(side="left", padx=10, pady=10)

        # --- OCR Section ---
        self.ocr_separator = ctk.CTkLabel(self, text="──────────── OR ────────────", font=("Roboto", 14))
        self.ocr_separator.pack(pady=10)
        
        self.ocr_title = ctk.CTkLabel(self, text="📸 OCR - Extract Text from Image", font=("Roboto", 18, "bold"))
        self.ocr_title.pack(pady=5)
        
        # Image Selection Frame
        self.image_frame = ctk.CTkFrame(self)
        self.image_frame.pack(pady=10, padx=20, fill="x")
        
        self.image_btn = ctk.CTkButton(self.image_frame, text="Upload Image", command=self.select_image)
        self.image_btn.pack(side="left", padx=10, pady=10)
        
        self.paste_btn = ctk.CTkButton(self.image_frame, text="Paste Image (Ctrl+V)", command=self.paste_image)
        self.paste_btn.pack(side="left", padx=10, pady=10)
        
        self.image_label = ctk.CTkLabel(self.image_frame, textvariable=self.image_path_var, text_color="gray")
        self.image_label.pack(side="left", padx=10)
        
        # OCR Language Selection
        self.ocr_lang_frame = ctk.CTkFrame(self)
        self.ocr_lang_frame.pack(pady=10, padx=20, fill="x")
        
        self.ocr_lang_label = ctk.CTkLabel(self.ocr_lang_frame, text="OCR Language:")
        self.ocr_lang_label.pack(side="left", padx=10)
        
        ocr_languages = ["eng+ind", "eng", "ind", "jpn", "chi_sim", "chi_tra", "kor", "ara", "fra", "deu", "spa"]
        self.ocr_lang_menu = ctk.CTkOptionMenu(self.ocr_lang_frame, variable=self.ocr_lang_var, values=ocr_languages)
        self.ocr_lang_menu.pack(side="left", padx=10, pady=10)
        
        # OCR Action Buttons
        self.ocr_action_frame = ctk.CTkFrame(self)
        self.ocr_action_frame.pack(pady=10, padx=20, fill="x")
        
        self.extract_btn = ctk.CTkButton(self.ocr_action_frame, text="Extract Text", command=self.start_ocr_thread, height=40)
        self.extract_btn.pack(side="left", padx=10, pady=10, expand=True, fill="x")
        
        self.translate_ocr_btn = ctk.CTkButton(self.ocr_action_frame, text="Extract & Translate", command=self.start_ocr_translate_thread, height=40)
        self.translate_ocr_btn.pack(side="left", padx=10, pady=10, expand=True, fill="x")
        
        # Bind Ctrl+V for paste
        self.bind('<Control-v>', lambda e: self.paste_image())

        # --- Action Button (for file translation) ---
        self.action_btn = ctk.CTkButton(self, text="Translate File", command=self.start_translation_thread, height=50, font=("Roboto", 16, "bold"))
        self.action_btn.pack(pady=20, padx=20, fill="x")

        # --- Log/Status Area ---
        self.log_textbox = ctk.CTkTextbox(self, height=150)
        self.log_textbox.pack(pady=10, padx=20, fill="both", expand=True)
        self.log_textbox.configure(state="disabled")

    def log(self, message):
        self.log_textbox.configure(state="normal")
        self.log_textbox.insert("end", message + "\n")
        self.log_textbox.see("end")
        self.log_textbox.configure(state="disabled")

    def select_file(self):
        filetypes = (
            ("All Supported", "*.srt *.txt *.docx *.pdf"),
            ("Subtitle", "*.srt"),
            ("Text", "*.txt"),
            ("Word", "*.docx"),
            ("PDF", "*.pdf"),
            ("All Files", "*.*")
        )
        filename = filedialog.askopenfilename(title="Select a file to translate", filetypes=filetypes)
        if filename:
            self.file_path_var.set(filename)
            self.log(f"Selected file: {filename}")

    def start_translation_thread(self):
        # Run in thread to keep UI responsive
        threading.Thread(target=self.run_translation, daemon=True).start()

    def run_translation(self):
        api_key = self.api_key_var.get().strip()
        filepath = self.file_path_var.get()
        target_lang = self.target_lang_var.get()

        if not api_key:
            self.log("Error: API Key is missing.")
            return
        if not filepath:
            self.log("Error: No file selected.")
            return
        
        self.action_btn.configure(state="disabled", text="Translating...")
        self.log("-" * 30)
        self.log(f"Starting translation for {os.path.basename(filepath)} -> {target_lang}")

        try:
            translator = DeepLTranslator(api_key)
            
            # Validate key first (optional, but good for UX)
            valid, msg = translator.validate_api_key()
            if not valid:
                raise Exception(f"Invalid API Key: {msg}")
            
            # Determine output path
            directory = os.path.dirname(filepath)
            filename = os.path.basename(filepath)
            name, ext = os.path.splitext(filename)
            output_filename = f"{name}_{target_lang}{ext}"
            output_path = os.path.join(directory, output_filename)
            
            self.log(f"Output will be saved to: {output_filename}")
            
            # Dispatch based on extension
            ext_lower = ext.lower()
            if ext_lower == ".txt":
                translator.translate_txt_file(filepath, target_lang, output_path)
            elif ext_lower == ".srt":
                translator.translate_srt_file(filepath, target_lang, output_path)
            elif ext_lower in [".docx", ".pdf"]:
                self.log("Uploading document...")
                translator.translate_document(filepath, target_lang, output_path)
            else:
                raise Exception(f"Unsupported file format: {ext}")
            
            self.log("SUCCESS! Translation completed.")
            self.log(f"Saved to: {output_path}")
            messagebox.showinfo("Success", f"File translated successfully!\nSaved to: {output_path}")

        except Exception as e:
            self.log(f"ERROR: {str(e)}")
            messagebox.showerror("Error", str(e))
        finally:
            self.action_btn.configure(state="normal", text="Translate File")

    def select_image(self):
        """Select an image file for OCR"""
        filetypes = (
            ("Image Files", "*.png *.jpg *.jpeg *.bmp *.tiff *.gif"),
            ("All Files", "*.*")
        )
        filename = filedialog.askopenfilename(title="Select an image for OCR", filetypes=filetypes)
        if filename:
            self.image_path_var.set(filename)
            self.pasted_image = None  # Clear any pasted image
            self.log(f"Selected image: {filename}")

    def paste_image(self):
        """Paste image from clipboard"""
        try:
            # Get image from clipboard
            image = ImageGrab.grabclipboard()
            
            if image is None:
                self.log("No image found in clipboard. Copy an image first (Ctrl+C).")
                messagebox.showwarning("No Image", "No image found in clipboard.\nPlease copy an image first (Ctrl+C).")
                return
            
            # Check if it's an image
            if not isinstance(image, Image.Image):
                self.log("Clipboard content is not an image.")
                messagebox.showwarning("Invalid Content", "Clipboard content is not an image.")
                return
            
            # Store the pasted image
            self.pasted_image = image
            image_info = f"Image from clipboard ({image.size[0]}x{image.size[1]}, {image.mode})"
            self.image_path_var.set(image_info)
            self.log(f"Image pasted successfully! Size: {image.size}, Mode: {image.mode}")
            
        except Exception as e:
            self.log(f"Error pasting image: {str(e)}")
            messagebox.showerror("Paste Error", str(e))

    def start_ocr_thread(self):
        """Start OCR extraction in a separate thread"""
        threading.Thread(target=self.run_ocr, daemon=True).start()

    def start_ocr_translate_thread(self):
        """Start OCR + Translation in a separate thread"""
        threading.Thread(target=self.run_ocr_translate, daemon=True).start()

    def run_ocr(self):
        """Extract text from image using OCR"""
        api_key = self.api_key_var.get().strip()
        image_path = self.image_path_var.get()
        ocr_lang = self.ocr_lang_var.get()

        if not api_key:
            self.log("Error: API Key is missing.")
            return
        
        if not image_path and not self.pasted_image:
            self.log("Error: No image selected or pasted.")
            return

        self.extract_btn.configure(state="disabled", text="Extracting...")
        self.translate_ocr_btn.configure(state="disabled")
        self.log("-" * 30)
        self.log(f"Starting OCR with language: {ocr_lang}")

        try:
            translator = DeepLTranslator(api_key)
            
            # Determine image source
            if self.pasted_image:
                self.log("Processing pasted image...")
                extracted_text = translator.extract_text_from_image(self.pasted_image, lang=ocr_lang)
            else:
                self.log(f"Processing image: {os.path.basename(image_path)}")
                extracted_text = translator.extract_text_from_image(image_path, lang=ocr_lang)
            
            if not extracted_text:
                self.log("WARNING: No text found in the image.")
                messagebox.showwarning("No Text", "No text was detected in the image.")
            else:
                self.ocr_text = extracted_text
                self.log("SUCCESS! Text extracted from image:")
                self.log("-" * 30)
                self.log(extracted_text)
                self.log("-" * 30)
                
                # Show beautiful result window
                OCRResultWindow(self, extracted_text, None, ocr_lang, "Extracted")

        except Exception as e:
            self.log(f"ERROR: {str(e)}")
            messagebox.showerror("OCR Error", str(e))
        finally:
            self.extract_btn.configure(state="normal", text="Extract Text")
            self.translate_ocr_btn.configure(state="normal")

    def run_ocr_translate(self):
        """Extract text from image and translate it"""
        api_key = self.api_key_var.get().strip()
        image_path = self.image_path_var.get()
        ocr_lang = self.ocr_lang_var.get()
        target_lang = self.target_lang_var.get()

        if not api_key:
            self.log("Error: API Key is missing.")
            return
        
        if not image_path and not self.pasted_image:
            self.log("Error: No image selected or pasted.")
            return

        self.extract_btn.configure(state="disabled")
        self.translate_ocr_btn.configure(state="disabled", text="Processing...")
        self.log("-" * 30)
        self.log(f"Starting OCR + Translation: {ocr_lang} -> {target_lang}")

        try:
            translator = DeepLTranslator(api_key)
            
            # Step 1: Extract text
            if self.pasted_image:
                self.log("Processing pasted image...")
                extracted_text = translator.extract_text_from_image(self.pasted_image, lang=ocr_lang)
            else:
                self.log(f"Processing image: {os.path.basename(image_path)}")
                extracted_text = translator.extract_text_from_image(image_path, lang=ocr_lang)
            
            if not extracted_text:
                self.log("WARNING: No text found in the image.")
                messagebox.showwarning("No Text", "No text was detected in the image.")
                return
            
            self.ocr_text = extracted_text
            self.log("Text extracted successfully!")
            self.log("Original text:")
            self.log("-" * 30)
            self.log(extracted_text)
            self.log("-" * 30)
            
            # Step 2: Translate
            self.log(f"Translating to {target_lang}...")
            translated_texts = translator.translate_text_content([extracted_text], target_lang)
            translated_text = translated_texts[0]
            
            self.log("SUCCESS! Translation completed:")
            self.log("-" * 30)
            self.log(translated_text)
            self.log("-" * 30)
            
            # Show beautiful result window
            OCRResultWindow(self, extracted_text, translated_text, ocr_lang, target_lang)

        except Exception as e:
            self.log(f"ERROR: {str(e)}")
            messagebox.showerror("Error", str(e))
        finally:
            self.extract_btn.configure(state="normal")
            self.translate_ocr_btn.configure(state="normal", text="Extract & Translate")


if __name__ == "__main__":
    app = DeepLApp()
    app.mainloop()
