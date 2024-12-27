# Transcriptor

This Python project lets you create multiple transcripts from YouTube videos using Whisper AI. Originally designed for Google Colab, it now works both locally and on Colab with GPU acceleration.

## Features

- Downloads and processes multiple YouTube videos from `youtube_urls.txt`
- Creates accurate transcripts using OpenAI's Whisper AI model
- Automatically manages audio files (downloads and cleanup)
- Organized output structure with all transcripts in a dedicated directory
- Comprehensive error handling and logging
- GPU acceleration support (both local and Colab)
- Uses `youtube-dl` in nightly mode for better compatibility

## Project Structure

```
transcriptor/
├── models/          # Stores Whisper AI models
├── transcripts/     # Stores generated transcripts
├── config.py        # Configuration settings
├── main.py         # Main transcription logic
├── download.py     # Model download script
└── youtube_urls.txt # Input YouTube URLs
```

## Dependencies

- Python 3.x
- whisper
- torch
- youtube-dl (included)

## Setup and Usage

### Local Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/byigitt/transcriptor.git
   cd transcriptor
   ```
2. Install dependencies:
   ```bash
   pip install whisper torch
   chmod 755 youtube-dl
   ```
3. Download the Whisper model:
   ```bash
   python download.py
   ```
4. Create `youtube_urls.txt` with your YouTube URLs (one per line)
5. Run the transcription:
   ```bash
   python main.py
   ```

### Google Colab Setup

1. Create a new Colab notebook
2. Change runtime type to GPU
3. Clone the repository:
   ```bash
   !git clone https://github.com/byigitt/transcriptor.git
   %cd transcriptor
   ```
4. Install dependencies and run:
   ```bash
   !chmod 755 youtube-dl
   !pip install whisper torch
   !python download.py
   !python main.py
   ```

## Configuration

The project uses `config.py` for centralized settings:

- Model selection and device settings
- Input/output paths configuration
- YouTube download settings
- Logging configuration

## Output

- Transcripts are saved in the `transcripts/` directory
- Each transcript is named after its video with `-transcript.txt` suffix
- Audio files are automatically cleaned up after transcription

## Troubleshooting

- If you encounter GPU-related errors, the system will automatically fall back to CPU
- Check the logs for detailed error messages and debugging information
- Make sure your YouTube URLs are valid and accessible
- Keep the Colab tab open during processing to prevent file deletion

## For Issues and Questions

Feel free to:

- Open an issue for bugs or questions
- Submit pull requests for improvements
- Check existing issues for common problems

## Why Google Colab?

Google Colab provides free GPU access and faster processing. The project works particularly well with Turkish language content (tested with Google Oyun ve Uygulama Akademisi education videos) but supports all languages supported by Whisper AI.
