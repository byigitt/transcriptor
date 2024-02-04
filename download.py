import sys
from whisper import _download, _MODELS

_download(_MODELS["medium"], "./models/", False)