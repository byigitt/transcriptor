import sys
import logging
from whisper import _download, _MODELS
import config

logging.basicConfig(
    level=getattr(logging, config.LOG_LEVEL),
    format=config.LOG_FORMAT
)
logger = logging.getLogger(__name__)

def download_model():
    try:
        logger.info(f"Downloading {config.MODEL_NAME} model...")
        _download(_MODELS[config.MODEL_NAME], str(config.MODELS_DIR), False)
        logger.info("Model downloaded successfully")
    except Exception as e:
        logger.error(f"Failed to download model: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    download_model()