# DeepL Document Translator

A Python desktop application to translate documents (SRT, TXT, DOCX, PDF) automatically using the DeepL API.

## Features

*   **Multi-Format Support**: Translates `.srt` (Subtitles), `.txt` (Text), `.docx` (Word), and `.pdf` (PDF).
*   **Smart Processing**:
    *   **SRT**: Parses and translates only the subtitle text, preserving timestamps and structure.
    *   **Docs**: Uses DeepL's Document API to preserve original formatting (fonts, images, layout).
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

3.  **Setup API Key**:
    *   Rename or copy `.env.example` (if available) to `.env`.
    *   Or create a new `.env` file in the root directory:
        ```env
        DEEPL_API_KEY=your-deepl-api-key-here
        ```
    *   *Note: Free tier keys usually end with `:fx`.*

## Usage

1.  Run the application:
    ```bash
    python main.py
    ```
2.  **Select File**: Click the button to choose your source file.
3.  **Target Language**: Select the language code (e.g., `ID` for Indonesian, `EN-US` for English).
4.  **Translate**: Click the "Translate Now" button.
5.  **Output**: The translated file will be saved in the same folder as the source, with the language code appended (e.g., `video_ID.srt`).

## Project Structure

*   `main.py`: Entry point of the application.
*   `gui.py`: Handles the User Interface logic.
*   `backend.py`: Contains the `DeepLTranslator` class and API logic.
*   `requirements.txt`: List of Python dependencies.
*   `.env`: Configuration file for API keys.

## License

Free to use for personal and educational purposes.
