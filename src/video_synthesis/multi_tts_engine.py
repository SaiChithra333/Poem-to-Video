"""
Multi-Language TTS Engine — Module 3, Enhancement 5

Dispatches TTS narration requests for all segments and all target languages
concurrently using a worker pool. Returns audio paths organized by language and segment.

Reference: Section 4.5 and Section 8.1 of Progress.docx.
"""

from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

from src.config import TEMP_DIR, TARGET_LANGUAGES
from src.video_synthesis.tts_engine import synthesize_line


def synthesize_multilingual_audio(
    segments_dict: dict[str, list[str]],
    output_dir: Path = None,
    max_workers: int = 4
) -> dict[str, list[Path]]:
    """
    Synthesize audio narration for multiple languages concurrently.

    Args:
        segments_dict: Dict mapping language code (e.g. 'en', 'zh', 'fr') to list of segment texts.
        output_dir: Base directory to save audio files.
        max_workers: Concurrent workers.

    Returns:
        Dict mapping language code to list of audio Paths: dict[lang][segment_idx] -> Path
    """
    output_dir = output_dir or (TEMP_DIR / "multi_tts")
    output_dir.mkdir(parents=True, exist_ok=True)

    results: dict[str, list[Path | None]] = {}
    tasks = []

    for lang, texts in segments_dict.items():
        lang_dir = output_dir / lang
        lang_dir.mkdir(parents=True, exist_ok=True)
        results[lang] = [None] * len(texts)

        for seg_idx, text in enumerate(texts):
            out_file = lang_dir / f"seg_{seg_idx:03d}_{lang}.mp3"
            tasks.append((lang, seg_idx, text, out_file))

    print(f"  [MultiTTS] Synthesizing {len(tasks)} audio files across {len(segments_dict)} languages...")

    def _worker(task_info):
        lang, seg_idx, text, out_file = task_info
        try:
            path = synthesize_line(text, out_file, language=lang)
            return lang, seg_idx, path
        except Exception as e:
            print(f"  [MultiTTS] ✗ Failed {lang} segment {seg_idx+1}: {e}")
            return lang, seg_idx, None

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(_worker, t) for t in tasks]
        for f in as_completed(futures):
            lang, seg_idx, path = f.result()
            results[lang][seg_idx] = path

    print("  [MultiTTS] ✓ Multilingual audio synthesis complete")
    return results
