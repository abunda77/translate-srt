import customtkinter as ctk
from tkinter import font as tkfont
import pyperclip

class TranslationResultWindow(ctk.CTkToplevel):
    """
    Beautiful, modern window to display translation results
    """
    def __init__(self, parent, original_text, translated_text, source_lang="Auto", target_lang="ID"):
        super().__init__(parent)
        
        self.original_text = original_text
        self.translated_text = translated_text
        self.source_lang = source_lang
        self.target_lang = target_lang
        
        # Window configuration
        self.title("Translation Result")
        self.geometry("800x600")
        
        # Make window modal
        self.transient(parent)
        self.grab_set()
        
        # Center window
        self.center_window()
        
        # Create UI
        self.create_widgets()
        
    def center_window(self):
        """Center the window on screen"""
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')
        
    def create_widgets(self):
        # Header with gradient effect (simulated with frame)
        self.header_frame = ctk.CTkFrame(self, fg_color=("#3b8ed0", "#1f6aa5"), corner_radius=0)
        self.header_frame.pack(fill="x", padx=0, pady=0)
        
        # Title with icon
        self.title_label = ctk.CTkLabel(
            self.header_frame, 
            text="✨ Translation Complete",
            font=("Roboto", 28, "bold"),
            text_color="white"
        )
        self.title_label.pack(pady=20)
        
        # Subtitle
        self.subtitle_label = ctk.CTkLabel(
            self.header_frame,
            text=f"Translated from {self.source_lang} to {self.target_lang}",
            font=("Roboto", 14),
            text_color=("#e0e0e0", "#c0c0c0")
        )
        self.subtitle_label.pack(pady=(0, 20))
        
        # Main content area with padding
        self.content_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.content_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Original Text Section
        self.create_text_section(
            self.content_frame,
            "📄 Original Text",
            self.original_text,
            row=0,
            copy_callback=lambda: self.copy_to_clipboard(self.original_text, "Original")
        )
        
        # Arrow separator
        self.arrow_label = ctk.CTkLabel(
            self.content_frame,
            text="⬇️",
            font=("Roboto", 24)
        )
        self.arrow_label.grid(row=1, column=0, pady=10)
        
        # Translated Text Section
        self.create_text_section(
            self.content_frame,
            "🌐 Translated Text",
            self.translated_text,
            row=2,
            copy_callback=lambda: self.copy_to_clipboard(self.translated_text, "Translation"),
            highlight=True
        )
        
        # Configure grid weights
        self.content_frame.grid_rowconfigure(0, weight=1)
        self.content_frame.grid_rowconfigure(2, weight=1)
        self.content_frame.grid_columnconfigure(0, weight=1)
        
        # Footer with action buttons
        self.footer_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.footer_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        # Statistics
        orig_chars = len(self.original_text)
        trans_chars = len(self.translated_text)
        orig_words = len(self.original_text.split())
        trans_words = len(self.translated_text.split())
        
        self.stats_label = ctk.CTkLabel(
            self.footer_frame,
            text=f"📊 Original: {orig_chars} chars, {orig_words} words  |  Translated: {trans_chars} chars, {trans_words} words",
            font=("Roboto", 11),
            text_color="gray"
        )
        self.stats_label.pack(pady=(0, 10))
        
        # Action buttons
        self.button_frame = ctk.CTkFrame(self.footer_frame, fg_color="transparent")
        self.button_frame.pack()
        
        self.copy_both_btn = ctk.CTkButton(
            self.button_frame,
            text="📋 Copy Both",
            command=self.copy_both,
            width=140,
            height=40,
            font=("Roboto", 13, "bold"),
            fg_color=("#2ecc71", "#27ae60"),
            hover_color=("#27ae60", "#229954")
        )
        self.copy_both_btn.pack(side="left", padx=5)
        
        self.copy_translation_btn = ctk.CTkButton(
            self.button_frame,
            text="📝 Copy Translation",
            command=lambda: self.copy_to_clipboard(self.translated_text, "Translation"),
            width=160,
            height=40,
            font=("Roboto", 13, "bold"),
            fg_color=("#3498db", "#2980b9"),
            hover_color=("#2980b9", "#21618c")
        )
        self.copy_translation_btn.pack(side="left", padx=5)
        
        self.close_btn = ctk.CTkButton(
            self.button_frame,
            text="✓ Close",
            command=self.destroy,
            width=100,
            height=40,
            font=("Roboto", 13, "bold"),
            fg_color=("#95a5a6", "#7f8c8d"),
            hover_color=("#7f8c8d", "#6c7a7b")
        )
        self.close_btn.pack(side="left", padx=5)
        
    def create_text_section(self, parent, title, text, row, copy_callback, highlight=False):
        """Create a text display section with title and copy button"""
        # Section frame
        section_frame = ctk.CTkFrame(
            parent,
            fg_color=("#f0f0f0", "#2b2b2b") if not highlight else ("#e8f5e9", "#1b5e20"),
            corner_radius=10
        )
        section_frame.grid(row=row, column=0, sticky="nsew", pady=5)
        
        # Header with title and copy button
        header_frame = ctk.CTkFrame(section_frame, fg_color="transparent")
        header_frame.pack(fill="x", padx=15, pady=(15, 5))
        
        title_label = ctk.CTkLabel(
            header_frame,
            text=title,
            font=("Roboto", 16, "bold"),
            anchor="w"
        )
        title_label.pack(side="left")
        
        copy_btn = ctk.CTkButton(
            header_frame,
            text="📋 Copy",
            command=copy_callback,
            width=80,
            height=28,
            font=("Roboto", 11),
            fg_color=("#3498db", "#2980b9") if not highlight else ("#4caf50", "#388e3c"),
            hover_color=("#2980b9", "#21618c") if not highlight else ("#388e3c", "#2e7d32")
        )
        copy_btn.pack(side="right")
        
        # Text display with scrollbar
        text_frame = ctk.CTkFrame(section_frame, fg_color="transparent")
        text_frame.pack(fill="both", expand=True, padx=15, pady=(5, 15))
        
        textbox = ctk.CTkTextbox(
            text_frame,
            font=("Segoe UI", 13),
            wrap="word",
            fg_color=("white", "#1e1e1e") if not highlight else ("#ffffff", "#0d3d0d"),
            border_width=0,
            corner_radius=8
        )
        textbox.pack(fill="both", expand=True)
        textbox.insert("1.0", text)
        textbox.configure(state="disabled")
        
    def copy_to_clipboard(self, text, label):
        """Copy text to clipboard with feedback"""
        try:
            pyperclip.copy(text)
            # Show temporary success message
            self.show_toast(f"✓ {label} copied to clipboard!")
        except:
            # Fallback: use tkinter clipboard
            self.clipboard_clear()
            self.clipboard_append(text)
            self.show_toast(f"✓ {label} copied to clipboard!")
            
    def copy_both(self):
        """Copy both original and translated text"""
        combined = f"Original:\n{self.original_text}\n\n{'='*50}\n\nTranslated ({self.target_lang}):\n{self.translated_text}"
        self.copy_to_clipboard(combined, "Both texts")
        
    def show_toast(self, message):
        """Show a temporary toast notification"""
        # Create toast label
        toast = ctk.CTkLabel(
            self,
            text=message,
            font=("Roboto", 12, "bold"),
            fg_color=("#2ecc71", "#27ae60"),
            text_color="white",
            corner_radius=8
        )
        toast.place(relx=0.5, rely=0.95, anchor="center")
        
        # Auto-hide after 2 seconds
        self.after(2000, toast.destroy)


class OCRResultWindow(TranslationResultWindow):
    """
    Specialized window for OCR results (can show just extracted text or translation)
    """
    def __init__(self, parent, extracted_text, translated_text=None, ocr_lang="eng+ind", target_lang="ID"):
        if translated_text:
            # Show both extraction and translation
            super().__init__(parent, extracted_text, translated_text, ocr_lang, target_lang)
            self.title("OCR & Translation Result")
            # Update header
            for widget in self.header_frame.winfo_children():
                if isinstance(widget, ctk.CTkLabel) and "Translation Complete" in widget.cget("text"):
                    widget.configure(text="🔍 OCR & Translation Complete")
        else:
            # Show only extracted text
            super().__init__(parent, "", extracted_text, ocr_lang, "Extracted")
            self.title("OCR Result")
            # Update header
            for widget in self.header_frame.winfo_children():
                if isinstance(widget, ctk.CTkLabel) and "Translation Complete" in widget.cget("text"):
                    widget.configure(text="🔍 Text Extraction Complete")
            # Hide original text section since we only have extracted text
            self.content_frame.grid_slaves(row=0)[0].grid_forget()
            self.arrow_label.grid_forget()
