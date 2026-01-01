# OCR Troubleshooting Guide

## Common Issues and Solutions

### 1. "Tesseract not found" Error

**Problem:** The application can't find Tesseract OCR.

**Solutions:**

#### Windows:
1. Download Tesseract installer from: https://github.com/UB-Mannheim/tesseract/wiki
2. Run the installer (tesseract-ocr-w64-setup-v5.x.x.exe)
3. During installation:
   - Note the installation path (default: `C:\Program Files\Tesseract-OCR`)
   - Select additional language packs if needed (Indonesian, Japanese, etc.)
4. After installation, verify by running in PowerShell:
   ```powershell
   & "C:\Program Files\Tesseract-OCR\tesseract.exe" --version
   ```
5. If still not working, add to system PATH:
   - Search "Environment Variables" in Windows
   - Edit "Path" variable
   - Add: `C:\Program Files\Tesseract-OCR`
   - Restart the application

#### macOS:
```bash
brew install tesseract
```

#### Linux (Ubuntu/Debian):
```bash
sudo apt-get update
sudo apt-get install tesseract-ocr
```

### 2. "No text detected" or Poor OCR Results

**Problem:** OCR can't extract text or results are inaccurate.

**Solutions:**
- Ensure the image has good quality and resolution
- Make sure the text is clear and not too small
- Select the correct OCR language (e.g., `eng` for English, `ind` for Indonesian)
- For mixed languages, use combined language codes (e.g., `eng+ind`)
- Try preprocessing the image (increase contrast, remove noise)

### 3. Wrong Language Detected

**Problem:** OCR detects wrong characters or gibberish.

**Solutions:**
- Select the correct OCR language from the dropdown
- Install additional language packs:
  
  **Windows:** Re-run Tesseract installer and select language packs
  
  **Linux:**
  ```bash
  # Indonesian
  sudo apt-get install tesseract-ocr-ind
  
  # Japanese
  sudo apt-get install tesseract-ocr-jpn
  
  # Chinese Simplified
  sudo apt-get install tesseract-ocr-chi-sim
  
  # Korean
  sudo apt-get install tesseract-ocr-kor
  ```
  
  **macOS:**
  ```bash
  brew install tesseract-lang
  ```

### 4. Clipboard Paste Not Working

**Problem:** "Paste Image" button doesn't work.

**Solutions:**
- Make sure you copied an IMAGE (not text or file path)
- Try these methods to copy an image:
  - Right-click on image → Copy Image
  - In screenshot tool, use "Copy to Clipboard"
  - In image editor, Edit → Copy
- On Windows, use Snipping Tool or Snip & Sketch (Win+Shift+S)
- On macOS, use Cmd+Shift+Ctrl+4 to copy screenshot to clipboard

### 5. "Unsupported image format/type" Error (Clipboard Paste)

**Problem:** Error occurs when pasting image from clipboard, but upload works fine.

**Cause:** Images from clipboard may be in RGBA, P, or other color modes that need conversion.

**Solution:** This has been fixed in the latest version! The application now automatically converts:
- RGBA images to RGB (with white background)
- Palette (P) mode to RGB
- Other modes to compatible formats

**If you still get this error:**
1. Make sure you're using the latest version of the code
2. Try saving the screenshot as a file first, then upload it
3. Check the log area - it will show the image mode (e.g., "Mode: RGBA")
4. Report the issue with the image mode information

**Technical Details:**
- Tesseract OCR works best with RGB or grayscale (L) images
- Clipboard images are often in RGBA format (with transparency)
- The app now converts RGBA → RGB automatically before OCR

### 6. Supported Image Formats

The OCR feature supports:
- PNG (.png)
- JPEG (.jpg, .jpeg)
- TIFF (.tiff, .tif)
- BMP (.bmp)
- GIF (.gif)

### 7. Testing Tesseract Installation

Run this Python script to test:

```python
import pytesseract
from PIL import Image

# Test if Tesseract is found
try:
    version = pytesseract.get_tesseract_version()
    print(f"✓ Tesseract version: {version}")
except:
    print("✗ Tesseract not found!")

# Test OCR on a simple image
try:
    # Create a test image with text
    from PIL import Image, ImageDraw, ImageFont
    img = Image.new('RGB', (200, 50), color='white')
    d = ImageDraw.Draw(img)
    d.text((10,10), "Hello World", fill='black')
    
    text = pytesseract.image_to_string(img)
    print(f"✓ OCR test result: {text.strip()}")
except Exception as e:
    print(f"✗ OCR test failed: {e}")
```

### 8. Performance Tips

- For large images, OCR may take longer
- Close other applications to free up memory
- For batch processing, extract text first, then translate
- Use appropriate OCR language to improve accuracy and speed

## Getting Help

If you still have issues:
1. Check Tesseract version: `tesseract --version`
2. Check installed languages: `tesseract --list-langs`
3. Verify Python packages: `pip list | grep -E "pytesseract|Pillow"`
4. Check the application logs in the log area for specific error messages

## Useful Resources

- Tesseract Documentation: https://tesseract-ocr.github.io/
- Tesseract GitHub: https://github.com/tesseract-ocr/tesseract
- pytesseract Documentation: https://pypi.org/project/pytesseract/
- DeepL API Documentation: https://www.deepl.com/docs-api
