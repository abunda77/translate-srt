# Changelog

## [1.2.0] - 2026-01-01

### Added
- **Beautiful Translation Result Window**: Completely redesigned result display
  - Eye-catching gradient header with icons
  - Dual text display (Original + Translated) with color-coded sections
  - Statistics bar showing character and word counts
  - Multiple copy options: Copy Both, Copy Translation, individual copy buttons
  - Toast notifications for copy confirmations
  - Scrollable text areas for long content
  - Auto-centered modal window
  
- **New Files**:
  - `translation_result_window.py`: Custom result window classes
  - `UI_UX_UPDATE.md`: Documentation for new UI features

- **New Dependency**:
  - `pyperclip`: Cross-platform clipboard functionality

### Enhanced
- **OCR Results Display**: Now uses beautiful custom window instead of simple messagebox
  - Extract Text: Shows extracted text in modern window
  - Extract & Translate: Shows both original and translated with separator
- **User Experience**: Professional, modern look that's more informative and functional

### Technical Details
- Created `TranslationResultWindow` base class for translation results
- Created `OCRResultWindow` specialized class for OCR results
- Integrated with existing OCR workflow in `gui.py`

## [1.1.0] - 2026-01-01

### Fixed
- **OCR Clipboard Paste Error**: Fixed "Unsupported image format/type" error when pasting images from clipboard
  - Added automatic image format conversion (RGBA → RGB, P → RGB, etc.)
  - Images with transparency (RGBA) are now converted to RGB with white background
  - All clipboard image modes are now properly handled before OCR processing
  
### Enhanced
- **Better Paste Feedback**: Paste image function now shows image size and color mode in the log
  - Example: "Image pasted successfully! Size: (1920, 1080), Mode: RGBA"
  - Helps with debugging and understanding image properties

### Technical Details
- Modified `backend.py::extract_text_from_image()` to convert images to compatible formats
- Enhanced `gui.py::paste_image()` to provide detailed image information
- Added specific error handling for TesseractNotFoundError

## [1.0.0] - 2026-01-01

### Added
- **OCR Feature**: Extract text from images using Tesseract OCR
  - Upload image files (PNG, JPG, JPEG, BMP, TIFF, GIF)
  - Paste images from clipboard (Ctrl+V)
  - Support for 10+ OCR languages (English, Indonesian, Japanese, Chinese, Korean, etc.)
  - Two modes: "Extract Text" (OCR only) and "Extract & Translate" (OCR + Translation)
  
- **New Files**:
  - `tesseract_config.py`: Auto-configuration helper for Tesseract OCR
  - `OCR_TROUBLESHOOTING.md`: Comprehensive troubleshooting guide
  
- **Dependencies**:
  - `pytesseract`: Python wrapper for Tesseract OCR
  - `Pillow`: Image processing library (PIL fork)

### Changed
- Updated GUI window size from 700x550 to 700x800 to accommodate OCR section
- Renamed "Translate Now" button to "Translate File" for clarity
- Enhanced README.md with OCR installation and usage instructions

### Existing Features
- Multi-format document translation (SRT, TXT, DOCX, PDF)
- DeepL API integration
- Modern dark-themed GUI with CustomTkinter
- Threaded operations for responsive UI
- Secure API key management via .env file
