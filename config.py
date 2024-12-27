from pathlib import Path

# Paths
MODELS_DIR = Path("./models")
MODEL_PATH = MODELS_DIR / "medium.pt"
URLS_FILE = Path("youtube_urls.txt")
OUTPUT_DIR = Path("transcripts")

# Model settings
MODEL_NAME = "medium"
DEFAULT_DEVICE = "cuda"  # Will fall back to CPU if CUDA is not available

# YouTube download settings
AUDIO_FORMAT = "140"  # Format code for audio-only in m4a format
YOUTUBE_DL_PATH = "./youtube-dl"

# Logging settings
LOG_FORMAT = '%(asctime)s - %(levelname)s - %(message)s'
LOG_LEVEL = "INFO"

# Create necessary directories
OUTPUT_DIR.mkdir(exist_ok=True)
MODELS_DIR.mkdir(exist_ok=True) 