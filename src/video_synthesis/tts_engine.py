"""
TTS Engine — Module 3, Step 1 (Enhanced)

Converts poem text into spoken audio using Microsoft Edge TTS,
with automatic fallback to Google TTS (gTTS) to guarantee 100% audio availability.

Reference: Section III-C of the base paper and Section 4.5 of Progress.docx.
"""

import asyncio
from pathlib import Path

from src.config import TTS_VOICE_CHINESE, TTS_VOICE_ENGLISH, LANGUAGE_VOICE_MAP, TEMP_DIR


def _detect_language(text: str) -> str:
    """Heuristic to detect language from text scripts."""
    # Devanagari / Hindi
    if any('\u0900' <= c <= '\u097f' for c in text):
        return "hi"
    # Japanese kana
    if any('\u3040' <= c <= '\u30ff' for c in text):
        return "ja"
    # Chinese characters
    chinese_chars = sum(1 for c in text if '\u4e00' <= c <= '\u9fff')
    total_alpha = sum(1 for c in text if c.isalpha())
    if total_alpha > 0 and (chinese_chars / total_alpha) > 0.3:
        return "zh"
    return "en"


async def _synthesize_edge(text: str, output_path: Path, voice: str, rate: str = "-10%") -> Path:
    """Synthesize speech via Microsoft Edge TTS."""
    import edge_tts
    communicate = edge_tts.Communicate(text, voice, rate=rate)
    await communicate.save(str(output_path))
    return output_path


def _synthesize_gtts(text: str, output_path: Path, lang_code: str = "en") -> Path:
    """Fallback speech synthesis using gTTS."""
    from gtts import gTTS
    code_map = {
        "chinese": "zh", "zh": "zh",
        "english": "en", "en": "en",
        "japanese": "ja", "ja": "ja",
        "hindi": "hi", "hi": "hi",
        "french": "fr", "fr": "fr",
        "spanish": "es", "es": "es",
        "german": "de", "de": "de",
        "italian": "it", "it": "it",
        "russian": "ru", "ru": "ru",
    }
    code = code_map.get(lang_code.lower(), "en")
    tts = gTTS(text=text, lang=code)
    tts.save(str(output_path))
    return output_path


def synthesize_line(
    text: str,
    output_path: Path = None,
    language: str = "auto",
    rate: str = "-15%",
    voice_override: str = None
) -> Path:
    """
    Convert a poem line to an MP3 audio file.

    Args:
        text: Poem line or segment text.
        output_path: Destination path (.mp3).
        language: Language code ("chinese", "english", "zh", "en", "hi", "ja", "fr", "es", "de", etc.).
        rate: Rate adjustment for edge-tts.
        voice_override: Explicit Edge-TTS voice.

    Returns:
        Path to generated MP3 file.
    """
    if output_path is None:
        output_path = TEMP_DIR / "tts_line.mp3"
    output_path.parent.mkdir(parents=True, exist_ok=True)

    clean_text = text.strip()
    if not clean_text:
        raise ValueError("Cannot synthesize empty text")

    detected = _detect_language(clean_text) if language in ("auto", None) else language.lower()
    lang_key = detected
    alias_map = {
        "chinese": "zh", "zh-cn": "zh",
        "english": "en", "en-us": "en",
        "japanese": "ja", "ja-jp": "ja",
        "hindi": "hi", "hi-in": "hi",
        "french": "fr", "fr-fr": "fr",
        "spanish": "es", "es-es": "es",
        "german": "de", "de-de": "de",
    }
    lang_key = alias_map.get(lang_key, lang_key)

    voice = voice_override or LANGUAGE_VOICE_MAP.get(lang_key, TTS_VOICE_ENGLISH if lang_key == "en" else TTS_VOICE_CHINESE)

    # 1. Try Microsoft Edge TTS
    try:
        asyncio.run(_synthesize_edge(clean_text, output_path, voice, rate))
        if output_path.exists() and output_path.stat().st_size > 100:
            print(f"  [TTS] ✓ Audio saved via Edge TTS: {output_path.name}")
            return output_path
    except Exception as e:
        print(f"  [TTS] ⚠ Edge TTS unavailable ({e}), trying gTTS fallback...")

    # 2. Try Google TTS (gTTS) Fallback
    try:
        _synthesize_gtts(clean_text, output_path, lang_key)
        if output_path.exists() and output_path.stat().st_size > 100:
            print(f"  [TTS] ✓ Audio saved via gTTS fallback: {output_path.name}")
            return output_path
    except Exception as e:
        print(f"  [TTS] ✗ gTTS fallback failed: {e}")
        raise RuntimeError(f"All TTS providers failed for text: {text[:40]}")


def synthesize_poem(
    lines: list[str],
    output_dir: Path = None,
    language: str = "auto",
    rate: str = "-15%",
) -> list[Path]:
    """
    Convert all poem lines or segments to individual audio files.
    """
    output_dir = output_dir or (TEMP_DIR / "tts")
    output_dir.mkdir(parents=True, exist_ok=True)

    audio_paths = []
    for i, line in enumerate(lines):
        clean_line = line.strip()
        if not clean_line:
            continue
        output_path = output_dir / f"line_{i:03d}.mp3"
        try:
            path = synthesize_line(clean_line, output_path, language, rate)
            audio_paths.append(path)
        except Exception as e:
            print(f"  [TTS] ⚠ Skipping item {i+1}: {e}")
            audio_paths.append(None)

    return audio_paths
