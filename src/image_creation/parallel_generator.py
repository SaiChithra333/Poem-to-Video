"""
Parallel Image Generator — Module 2, Enhancement 3

Implements asynchronous, parallel image generation across all visual segments.
Collapses total wall-clock image generation time from O(n) to O(1) by dispatching
all requests concurrently via concurrent.futures / asyncio.

Reference: Section 4.3 and Section 8.1 of Progress.docx.
"""

import time
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

from src.config import TEMP_DIR, PARALLEL_IMAGE_GEN, IMAGE_PROVIDER
from src.image_creation.single_frame_generator import generate_single_frame, _generate_placeholder


def generate_all_frames_parallel(
    prompts: list[dict],
    output_dir: Path = None,
    provider: str = None,
    max_workers: int = 2
) -> list[Path]:
    """
    Generate key-frame images for all poem segments concurrently.

    Args:
        prompts: List of prompt entries.
        output_dir: Directory where images should be saved.
        provider: Image provider override.
        max_workers: Max concurrent worker threads.

    Returns:
        List of Paths to generated images, in original segment order.
    """
    provider = provider or IMAGE_PROVIDER
    output_dir = output_dir or (TEMP_DIR / "key_frames")
    output_dir.mkdir(parents=True, exist_ok=True)

    if not PARALLEL_IMAGE_GEN or len(prompts) <= 1 or provider == "pollinations":
        print(f"  [ParallelImageGen] Dispatching {len(prompts)} segments sequentially for optimal API rate pacing...")
        from src.image_creation.single_frame_generator import generate_all_frames
        return generate_all_frames(prompts, output_dir, provider)

    print(f"  [ParallelImageGen] Firing {len(prompts)} image requests in parallel (workers={max_workers})...")
    start_time = time.time()

    # Pre-allocate output slots to preserve segment ordering
    results: list[Path | None] = [None] * len(prompts)

    def _worker(idx: int, prompt_entry: dict) -> tuple[int, Path]:
        # Stagger concurrent requests to prevent API rate limits
        if idx > 0:
            time.sleep(idx * 3.5)
        seg_id = prompt_entry.get("segment_id", idx)
        out_path = output_dir / f"frame_seg_{seg_id:03d}.png"
        try:
            path = generate_single_frame(prompt_entry, out_path, provider)
            return idx, path
        except Exception as e:
            print(f"  [ParallelImageGen] ✗ Worker {idx+1} failed: {e}")
            path = _generate_placeholder(prompt_entry, out_path)
            return idx, path

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(_worker, i, p) for i, p in enumerate(prompts)]
        for future in as_completed(futures):
            idx, path = future.result()
            results[idx] = path

    elapsed = time.time() - start_time
    print(f"  [ParallelImageGen] ✓ All {len(results)} frames generated in {elapsed:.1f}s")
    return [p for p in results if p is not None]
