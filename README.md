# DeepL Document Translator

A Python desktop application to translate documents (SRT, TXT, DOCX, PDF) automatically using the DeepL API.

## Features

*   **Multi-Format Support**: Translates `.srt` (Subtitles), `.txt` (Text), `.docx` (Word), and `.pdf` (PDF).
*   **OCR Support**: Extract text from images (PNG, JPG, TIFF, etc.) and translate them.
    *   Upload images or paste from clipboard (Ctrl+V)
    *   Supports multiple OCR languages (English, Indonesian, Japanese, Chinese, Korean, etc.)
    *   Extract text only or extract & translate in one click
*   **Smart Processing**:
    *   **SRT**: Parses and translates only the subtitle text, preserving timestamps and structure.
    *   **Docs**: Uses DeepL's Document API to preserve original formatting (fonts, images, layout).
    *   **Images**: Uses Tesseract OCR to extract text from images.
*   **Modern GUI**: User-friendly interface built with `CustomTkinter` (Dark Mode).
*   **Secure**: API Key is managed via a `.env` file, not hardcoded.
*   **Threaded**: Keeps the UI responsive during large file uploads/downloads.

## Prerequisites

*   Python 3.8+
*   A DeepL API Key (Free or Pro). You can get one [here](https://www.deepl.com/pro-api).

## Installation

1.  **Clone the repository** (or download the files):
    ```bash
    git clone <repository-url>
    cd translate-srt
    ```

2.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Install Tesseract OCR** (Required for OCR feature):
    
    **Windows:**
    - Download the installer from: https://github.com/UB-Mannheim/tesseract/wiki
    - Run the installer and note the installation path (e.g., `C:\Program Files\Tesseract-OCR`)
    - Add Tesseract to your system PATH, or add this line to your Python code:
      ```python
      pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
      ```
    
    **macOS:**
    ```bash
    brew install tesseract
    ```
    
    **Linux (Ubuntu/Debian):**
    ```bash
    sudo apt-get install tesseract-ocr
    ```
    
    **Install additional language packs (optional):**
    - For Indonesian: `sudo apt-get install tesseract-ocr-ind` (Linux)
    - For Japanese: `sudo apt-get install tesseract-ocr-jpn` (Linux)
    - On Windows, select language packs during installation

4.  **Setup API Key**:
    *   Rename or copy `.env.example` (if available) to `.env`.
    *   Or create a new `.env` file in the root directory:
        ```env
        DEEPL_API_KEY=your-deepl-api-key-here
        ```
    *   *Note: Free tier keys usually end with `:fx`.*

## Usage

### File Translation

1.  Run the application:
    ```bash
    python main.py
    ```
2.  **Select File**: Click the button to choose your source file.
3.  **Target Language**: Select the language code (e.g., `ID` for Indonesian, `EN-US` for English).
4.  **Translate**: Click the "Translate File" button.
5.  **Output**: The translated file will be saved in the same folder as the source, with the language code appended (e.g., `video_ID.srt`).

### OCR - Extract Text from Images

1.  **Upload Image**: Click "Upload Image" to select an image file (PNG, JPG, JPEG, etc.)
    
    **OR**
    
    **Paste Image**: Copy an image to clipboard (Ctrl+C) and click "Paste Image (Ctrl+V)" or press Ctrl+V
    
2.  **Select OCR Language**: Choose the language of the text in the image:
    - `eng+ind`: English + Indonesian (default)
    - `eng`: English only
    - `ind`: Indonesian only
    - `jpn`: Japanese
    - `chi_sim`: Chinese Simplified
    - And more...

3.  **Extract Text**: Click "Extract Text" to extract text from the image (no translation)
    
    **OR**
    
    **Extract & Translate**: Click "Extract & Translate" to extract and translate in one step

4.  **View Results**: Extracted and translated text will appear in the log area and in a popup message.

## Project Structure

*   `main.py`: Entry point of the application.
*   `gui.py`: Handles the User Interface logic.
*   `backend.py`: Contains the `DeepLTranslator` class and API logic.
*   `requirements.txt`: List of Python dependencies.
*   `.env`: Configuration file for API keys.

## License

Free to use for personal and educational purposes.
