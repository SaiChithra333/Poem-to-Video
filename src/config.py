"""
Configuration module for the Poem-to-Video system.
Centralizes all settings: API keys, model choices, output paths, artistic styles,
and enhanced architecture settings (Semantic Segmentation, Prompt Refinement,
Parallel Generation, Multi-Language Subtitles & TTS).
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Ensure UTF-8 console output on Windows to prevent charmap UnicodeEncodeError
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

# Load environment variables from .env or env file
env_file = Path(__file__).parent.parent / ".env"
if not env_file.exists():
    env_file = Path(__file__).parent.parent / "env"
load_dotenv(dotenv_path=env_file)

# ─── Project Paths ───────────────────────────────────────────────────────────

PROJECT_ROOT = Path(__file__).parent.parent
OUTPUT_DIR = PROJECT_ROOT / "output"
MODELS_DIR = PROJECT_ROOT / "models"
EXAMPLES_DIR = PROJECT_ROOT / "examples"
TEMP_DIR = PROJECT_ROOT / "temp"

# Ensure directories exist
for d in [OUTPUT_DIR, MODELS_DIR, EXAMPLES_DIR, TEMP_DIR]:
    d.mkdir(parents=True, exist_ok=True)

# ─── LLM Configuration ──────────────────────────────────────────────────────

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
LLM_MODEL = os.getenv("LLM_MODEL", "gemini-3.5-flash-lite")

# Candidate models for fallback
GEMINI_MODEL_FALLBACKS = [
    "gemini-3.5-flash-lite",
    "gemini-3.1-flash-lite",
    "gemini-3.5-flash",
    "gemini-3.8-flash"
]

# ─── Enhanced Architecture Flags ───────────────────────────────────────────

PROMPT_REFINE = os.getenv("PROMPT_REFINE", "True").lower() in ("true", "1", "yes")
PARALLEL_IMAGE_GEN = os.getenv("PARALLEL_IMAGE_GEN", "True").lower() in ("true", "1", "yes")
ENABLE_SEMANTIC_SEGMENTATION = os.getenv("ENABLE_SEMANTIC_SEGMENTATION", "True").lower() in ("true", "1", "yes")

# Target languages for multi-language subtitles and narration (e.g. ['en', 'zh', 'fr'])
_langs_raw = os.getenv("TARGET_LANGUAGES", "en,zh")
TARGET_LANGUAGES = [lang.strip() for lang in _langs_raw.split(",") if lang.strip()]

# ─── Image Generation Configuration ─────────────────────────────────────────

# Provider: "pollinations" (fast & high quality), "huggingface", or "placeholder"
IMAGE_PROVIDER = os.getenv("IMAGE_PROVIDER", "pollinations")

STABILITY_API_KEY = os.getenv("STABILITY_API_KEY", "")
HUGGINGFACE_API_TOKEN = os.getenv("HUGGINGFACE_API_TOKEN", "")
HF_IMAGE_MODEL = os.getenv("HF_IMAGE_MODEL", "black-forest-labs/FLUX.1-schnell")

# Image dimensions (16:9 for cinematic video)
IMAGE_WIDTH = int(os.getenv("IMAGE_WIDTH", "1024"))
IMAGE_HEIGHT = int(os.getenv("IMAGE_HEIGHT", "576"))

# ─── TTS Configuration ──────────────────────────────────────────────────────

TTS_VOICE_CHINESE = os.getenv("TTS_VOICE_CHINESE", "zh-CN-YunxiNeural")
TTS_VOICE_ENGLISH = os.getenv("TTS_VOICE_ENGLISH", "en-US-AriaNeural")

LANGUAGE_VOICE_MAP = {
    "zh": "zh-CN-YunxiNeural",
    "chinese": "zh-CN-YunxiNeural",
    "en": "en-US-AriaNeural",
    "english": "en-US-AriaNeural",
    "fr": "fr-FR-DeniseNeural",
    "french": "fr-FR-DeniseNeural",
    "es": "es-ES-ElviraNeural",
    "spanish": "es-ES-ElviraNeural",
    "hi": "hi-IN-SwaraNeural",
    "hindi": "hi-IN-SwaraNeural",
    "de": "de-DE-KatjaNeural",
    "german": "de-DE-KatjaNeural",
    "ja": "ja-JP-NanamiNeural",
    "japanese": "ja-JP-NanamiNeural",
    "it": "it-IT-ElsaNeural",
    "italian": "it-IT-ElsaNeural",
    "ru": "ru-RU-SvetlanaNeural",
    "russian": "ru-RU-SvetlanaNeural",
    "pt": "pt-BR-FranciscaNeural",
    "portuguese": "pt-BR-FranciscaNeural",
    "ar": "ar-SA-ZariyahNeural",
    "arabic": "ar-SA-ZariyahNeural"
}

# ─── System Font Detection ──────────────────────────────────────────────────

def get_system_font(prefer_cjk: bool = True, text: str = "") -> str:
    """Find a valid system font file on Windows, macOS, or Linux matching script, or fallback gracefully."""
    import platform
    is_mac = platform.system() == "Darwin"

    # Devanagari / Hindi script
    if text and any('\u0900' <= c <= '\u097f' for c in text):
        devanagari_fonts = [
            "/System/Library/Fonts/Supplemental/DevanagariMT.ttc",
            "/System/Library/Fonts/Supplemental/Devanagari Sangam MN.ttc",
            "/System/Library/Fonts/Supplemental/ITFDevanagari.ttc",
            "C:/Windows/Fonts/Nirmala.ttc",
            "C:/Windows/Fonts/nirmala.ttf",
            "C:/Windows/Fonts/mangal.ttf",
            "/usr/share/fonts/truetype/lohit-devanagari/Lohit-Devanagari.ttf",
            "/usr/share/fonts/truetype/freefont/FreeSerif.ttf",
        ]
        for f in devanagari_fonts:
            if os.path.exists(f):
                return f

    # Japanese Kana script
    if text and any('\u3040' <= c <= '\u30ff' for c in text):
        jp_fonts = [
            "/System/Library/Fonts/Hiragino Sans GB.ttc",
            "/System/Library/Fonts/AquaKana.ttc",
            "C:/Windows/Fonts/msgothic.ttc",
            "C:/Windows/Fonts/YuGothR.ttc",
            "C:/Windows/Fonts/meiryo.ttc",
            "C:/Windows/Fonts/msyh.ttc",
            "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
        ]
        for f in jp_fonts:
            if os.path.exists(f):
                return f

    cjk_fonts = [
        "/System/Library/Fonts/Supplemental/Songti.ttc",
        "/System/Library/Fonts/Hiragino Sans GB.ttc",
        "/System/Library/Fonts/Supplemental/Arial Unicode.ttf",
        "C:/Windows/Fonts/msyh.ttc",     # Microsoft YaHei
        "C:/Windows/Fonts/msyhbd.ttc",   # Microsoft YaHei Bold
        "C:/Windows/Fonts/simhei.ttf",   # SimHei
        "C:/Windows/Fonts/simsun.ttc",   # SimSun
        "C:/Windows/Fonts/kaiu.ttf",     # DFKai-SB
        "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc",
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
    ]
    general_fonts = [
        "/System/Library/Fonts/Helvetica.ttc",
        "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/System/Library/Fonts/Supplemental/Arial Unicode.ttf",
        "C:/Windows/Fonts/segoeui.ttf",  # Segoe UI
        "C:/Windows/Fonts/arial.ttf",     # Arial
        "C:/Windows/Fonts/calibri.ttf",   # Calibri
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]

    # Check for CJK ideographs
    has_cjk = bool(text and any(
        ('\u4e00' <= c <= '\u9fff') or ('\u3400' <= c <= '\u4dbf') or ('\uf900' <= c <= '\ufaff')
        for c in text
    ))

    # If text explicitly contains CJK characters, prioritize CJK fonts
    if has_cjk:
        for f in cjk_fonts:
            if os.path.exists(f):
                return f

    # If text has Latin/Western characters and NO CJK or Devanagari, prioritize crisp Latin typography
    if text and not has_cjk:
        for f in general_fonts:
            if os.path.exists(f):
                return f

    # Fallback when text is empty: honor prefer_cjk preference
    if prefer_cjk:
        for f in cjk_fonts:
            if os.path.exists(f):
                return f
    else:
        for f in general_fonts:
            if os.path.exists(f):
                return f

    for f in general_fonts:
        if os.path.exists(f):
            return f

    for f in cjk_fonts:
        if os.path.exists(f):
            return f

    if is_mac and os.path.exists("/System/Library/Fonts/Supplemental/Arial Unicode.ttf"):
        return "/System/Library/Fonts/Supplemental/Arial Unicode.ttf"
    if is_mac and os.path.exists("/System/Library/Fonts/Helvetica.ttc"):
        return "/System/Library/Fonts/Helvetica.ttc"

    return "DejaVu-Sans"

# ─── Video Configuration ────────────────────────────────────────────────────

VIDEO_FPS = int(os.getenv("VIDEO_FPS", "24"))
VIDEO_CODEC = os.getenv("VIDEO_CODEC", "libx264")
TRANSITION_DURATION = float(os.getenv("TRANSITION_DURATION", "1.0"))  # seconds

# ─── Artistic Style Presets ──────────────────────────────────────────────────

STYLE_PRESETS = {
    "chinese_ink": {
        "name": "Chinese Ink Painting",
        "style_prompt": "traditional Chinese ink wash painting, sumi-e style, rice paper texture, "
                        "elegant brushwork, monochrome with subtle color washes, "
                        "traditional Chinese landscape painting, shanshui style",
        "lora_keywords": "chinese ink painting, traditional art, brush strokes"
    },
    "watercolor": {
        "name": "Watercolor",
        "style_prompt": "watercolor painting, soft washes, delicate blending, "
                        "luminous transparency, wet-on-wet technique, artistic",
        "lora_keywords": "watercolor, soft colors, artistic painting"
    },
    "oil_painting": {
        "name": "Oil Painting",
        "style_prompt": "oil painting, rich textures, impasto technique, "
                        "vibrant colors, classical artistic style, museum quality",
        "lora_keywords": "oil painting, classical art, rich textures"
    },
    "digital_art": {
        "name": "Digital Art",
        "style_prompt": "digital art, concept art, highly detailed, "
                        "cinematic lighting, artstation trending, 4K",
        "lora_keywords": "digital art, concept art, detailed illustration"
    },
    "anime": {
        "name": "Anime/Illustration",
        "style_prompt": "anime style illustration, beautiful scenery, "
                        "vibrant colors, Studio Ghibli inspired, detailed background",
        "lora_keywords": "anime, illustration, scenic"
    }
}

DEFAULT_STYLE = os.getenv("DEFAULT_STYLE", "chinese_ink")

# ─── Negative Prompts (from the paper) ───────────────────────────────────────

NEGATIVE_PROMPTS = (
    "worst quality, low quality, logo, text, watermark, username, Chinese text, stamp mark, "
    "blurry, distorted, deformed, disfigured, bad anatomy, extra limbs, "
    "poorly drawn, ugly, duplicate, morbid, mutilated, low contrast, underexposed, amateur"
)

# ─── 12-Dimensional Framework (from the paper) ──────────────────────────────

TWELVE_DIMENSIONS = [
    "Subject",         # people, animals, landscapes, buildings
    "Action",          # running, jumping, swimming, falling
    "Context",         # scene composition, spatial relationships
    "Environment",     # indoor/outdoor, season, weather
    "Lighting",        # natural, golden hour, moonlight, candlelight
    "Artist",          # reference artist style
    "Style",           # Chinese ink, watercolor, oil painting
    "Medium",          # oil on canvas, watercolor, ink on rice paper
    "Type",            # landscape, portrait, still life
    "Color Scheme",    # pastel, vibrant, muted, specific colors
    "Computer Graphics",  # 3D, octane render, cycles
    "Quality"          # HD, 4K, 8K, masterpiece, superior quality
]
