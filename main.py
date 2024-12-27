import re
import os
import torch
import whisper
import subprocess
import logging
from pathlib import Path
from typing import Optional
import config

# Configure logging
logging.basicConfig(
    level=getattr(logging, config.LOG_LEVEL),
    format=config.LOG_FORMAT
)
logger = logging.getLogger(__name__)

class TranscriptionError(Exception):
    """Custom exception for transcription related errors"""
    pass

class YouTubeTranscriptor:
    def __init__(self, model_name: str = config.MODEL_NAME, device: Optional[str] = None):
        self.model_name = model_name
        self.device = device or (config.DEFAULT_DEVICE if torch.cuda.is_available() else "cpu")
        self.model = None
        
    def initialize_model(self):
        """Initialize the Whisper model"""
        try:
            if not config.MODEL_PATH.exists():
                logger.warning("Model file not found. Please run download.py first.")
                raise FileNotFoundError("Model file not found")
            
            self.model = whisper.load_model(str(config.MODEL_PATH), device=self.device)
            logger.info(f"Model loaded successfully on {self.device}")
        except Exception as e:
            logger.error(f"Failed to load model: {str(e)}")
            raise

    @staticmethod
    def is_valid_youtube_uri(url: str) -> bool:
        """Validate YouTube URL format"""
        regex = (
            r"(https?://)?(www\.)?"
            "(youtube|youtu|youtube-nocookie)\.(com|be)/"
            "(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})"
        )
        return re.match(regex, url) is not None

    def download_video_as_mp3(self, url: str) -> str:
        """Download YouTube video and convert to MP3"""
        try:
            command = [config.YOUTUBE_DL_PATH, "--get-filename", "--output", "%(title)s.%(ext)s", url]
            result = subprocess.run(command, capture_output=True, text=True, check=True)
            filename = result.stdout.strip().replace(".mp4", "")
            output_path = config.OUTPUT_DIR / filename

            logger.info(f"Downloading: {url}")
            download_result = subprocess.run(
                [config.YOUTUBE_DL_PATH, "-f", config.AUDIO_FORMAT, "--output", str(output_path), url],
                capture_output=True,
                text=True,
                check=True
            )
            
            audio_file = output_path.with_suffix(".mp3")
            if not audio_file.exists():
                raise FileNotFoundError(f"Download failed: {filename}")
                
            return str(audio_file)
        except subprocess.CalledProcessError as e:
            logger.error(f"Download failed: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error during download: {str(e)}")
            raise

    def transcribe_audio(self, filename: str) -> str:
        """Transcribe audio file using Whisper"""
        try:
            if self.model is None:
                self.initialize_model()
                
            logger.info(f"Transcribing: {filename}")
            result = self.model.transcribe(filename)
            return result["text"]
        except Exception as e:
            logger.error(f"Transcription failed: {str(e)}")
            raise TranscriptionError(f"Failed to transcribe {filename}: {str(e)}")

    def process_url(self, url: str) -> None:
        """Process a single YouTube URL"""
        try:
            if not self.is_valid_youtube_uri(url):
                logger.warning(f"Invalid YouTube URL: {url}")
                return

            filename = self.download_video_as_mp3(url)
            logger.info(f"Downloaded: {filename}")

            result = self.transcribe_audio(filename)
            output_path = Path(filename).with_suffix(".txt")
            output_path = config.OUTPUT_DIR / output_path.name.replace(".mp3", "-transcript.txt")

            with open(output_path, "w", encoding="utf-8") as transcript_file:
                transcript_file.write(result)
            
            os.remove(filename)
            logger.info(f"Transcript saved: {output_path}")
            
        except Exception as e:
            logger.error(f"Failed to process {url}: {str(e)}")
            if 'filename' in locals() and os.path.exists(filename):
                os.remove(filename)

def main():
    transcriptor = YouTubeTranscriptor()
    
    try:
        if not config.URLS_FILE.exists():
            logger.error(f"URLs file not found: {config.URLS_FILE}")
            return
            
        with open(config.URLS_FILE, "r") as file:
            urls = file.readlines()
            
        if not urls:
            logger.warning(f"No URLs found in {config.URLS_FILE}")
            return
            
        for url in urls:
            url = url.strip()
            if url:
                transcriptor.process_url(url)
                
    except Exception as e:
        logger.error(f"An unexpected error occurred: {str(e)}")

if __name__ == "__main__":
    main()