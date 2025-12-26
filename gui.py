import os
import threading
import customtkinter as ctk
from tkinter import filedialog, messagebox
from backend import DeepLTranslator
from dotenv import load_dotenv

# Load env to get key if available
load_dotenv()

class DeepLApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("DeepL Document Translator")
        self.geometry("700x550")
        
        # Set theme
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("blue")

        # Variables
        self.api_key_var = ctk.StringVar(value=os.getenv("DEEPL_API_KEY", ""))
        self.file_path_var = ctk.StringVar()
        self.target_lang_var = ctk.StringVar(value="ID") # Default to Indonesian
        self.status_var = ctk.StringVar(value="Ready")
        
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

        # --- Action Button ---
        self.action_btn = ctk.CTkButton(self, text="Translate Now", command=self.start_translation_thread, height=50, font=("Roboto", 16, "bold"))
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
            self.action_btn.configure(state="normal", text="Translate Now")

if __name__ == "__main__":
    app = DeepLApp()
    app.mainloop()
