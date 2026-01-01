"""
Tesseract OCR Configuration
This file helps configure Tesseract OCR path for Windows users.
"""
import os
import sys
import pytesseract

def setup_tesseract():
    """
    Automatically detect and configure Tesseract OCR path for Windows.
    For macOS and Linux, Tesseract is usually in PATH after installation.
    """
    if sys.platform == "win32":
        # Common Tesseract installation paths on Windows
        possible_paths = [
            r"C:\Program Files\Tesseract-OCR\tesseract.exe",
            r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe",
            r"C:\Tesseract-OCR\tesseract.exe",
        ]
        
        # Check if tesseract is already in PATH
        try:
            pytesseract.get_tesseract_version()
            print("✓ Tesseract found in PATH")
            return True
        except:
            pass
        
        # Try to find tesseract in common installation paths
        for path in possible_paths:
            if os.path.exists(path):
                pytesseract.pytesseract.tesseract_cmd = path
                print(f"✓ Tesseract found at: {path}")
                return True
        
        # If not found, show error message
        print("✗ Tesseract OCR not found!")
        print("\nPlease install Tesseract OCR:")
        print("1. Download from: https://github.com/UB-Mannheim/tesseract/wiki")
        print("2. Install it")
        print("3. Restart the application")
        return False
    
    # For macOS and Linux, assume it's in PATH
    try:
        pytesseract.get_tesseract_version()
        print("✓ Tesseract found in PATH")
        return True
    except:
        print("✗ Tesseract OCR not found!")
        print("\nPlease install Tesseract OCR:")
        if sys.platform == "darwin":
            print("Run: brew install tesseract")
        else:
            print("Run: sudo apt-get install tesseract-ocr")
        return False

if __name__ == "__main__":
    setup_tesseract()
