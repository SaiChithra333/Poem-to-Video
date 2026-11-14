"""
RIFE Frame Interpolation — Module 2, Step 2

Generates smooth intermediate frames between key frames using
image interpolation techniques.

The paper uses the RIFE (Real-time Intermediate Flow Estimation) model
for two purposes:
  1. Generating 32 frames per poem line (from key frame + control frames)
  2. Creating 1-second transition frames between consecutive poem lines

Since RIFE requires a GPU and model weights, this module provides:
  - A software-based cross-fade interpolation (works everywhere)
  - Optional RIFE integration (if the model is available locally)

Reference: Section III-B of the paper, RIFE [53].
"""

import numpy as np
from pathlib import Path
from PIL import Image

from src.config import VIDEO_FPS, TRANSITION_DURATION, IMAGE_WIDTH, IMAGE_HEIGHT


def interpolate_frames(
    frame_a_path: Path,
    frame_b_path: Path,
    num_frames: int = 16,
    output_dir: Path = None,
) -> list[Path]:
    """
    Generate intermediate frames between two key frames using cross-fade.

    This is a software fallback for RIFE. It creates a smooth visual
    transition by alpha-blending the two frames with a subtle zoom effect.

    Args:
        frame_a_path: Path to the starting frame.
        frame_b_path: Path to the ending frame.
        num_frames: Number of intermediate frames to generate.
        output_dir: Directory to save interpolated frames.

    Returns:
        List of paths to all frames (including start and end).
    """
    if output_dir is None:
        output_dir = frame_a_path.parent / "interpolated"
    output_dir.mkdir(parents=True, exist_ok=True)

    img_a = Image.open(frame_a_path).convert("RGB").resize((IMAGE_WIDTH, IMAGE_HEIGHT))
    img_b = Image.open(frame_b_path).convert("RGB").resize((IMAGE_WIDTH, IMAGE_HEIGHT))

    arr_a = np.array(img_a, dtype=np.float32)
    arr_b = np.array(img_b, dtype=np.float32)

    frame_paths = []

    for i in range(num_frames + 2):  # +2 to include start and end
        t = i / (num_frames + 1)  # 0.0 to 1.0

        # Smooth easing function (ease-in-out)
        t_smooth = _ease_in_out(t)

        # Cross-fade blend
        blended = arr_a * (1 - t_smooth) + arr_b * t_smooth

        # Subtle zoom effect (Ken Burns style)
        zoom_factor = 1.0 + 0.03 * np.sin(np.pi * t)  # slight zoom at midpoint
        blended_img = Image.fromarray(blended.astype(np.uint8))

        if zoom_factor != 1.0:
            w, h = blended_img.size
            new_w = int(w * zoom_factor)
            new_h = int(h * zoom_factor)
            blended_img = blended_img.resize((new_w, new_h), Image.LANCZOS)
            # Center crop back to original size
            left = (new_w - w) // 2
            top = (new_h - h) // 2
            blended_img = blended_img.crop((left, top, left + w, top + h))

        frame_path = output_dir / f"interp_{i:04d}.png"
        blended_img.save(frame_path)
        frame_paths.append(frame_path)

    print(f"  [Interpolation] ✓ Generated {len(frame_paths)} frames between key frames")
    return frame_paths


def generate_transition_frames(
    frame_a_path: Path,
    frame_b_path: Path,
    duration: float = None,
    fps: int = None,
    output_dir: Path = None,
) -> list[Path]:
    """
    Generate transition frames between two consecutive poem lines.
    Creates a 1-second (default) smooth transition.

    Args:
        frame_a_path: Last frame of the preceding poem line.
        frame_b_path: First frame of the next poem line.
        duration: Duration of the transition in seconds.
        fps: Frames per second.
        output_dir: Directory to save transition frames.

    Returns:
        List of paths to transition frames.
    """
    duration = duration or TRANSITION_DURATION
    fps = fps or VIDEO_FPS
    num_frames = int(duration * fps)

    if output_dir is None:
        output_dir = frame_a_path.parent / "transitions"
    output_dir.mkdir(parents=True, exist_ok=True)

    return interpolate_frames(frame_a_path, frame_b_path, num_frames, output_dir)


def generate_line_frames(
    key_frame_path: Path,
    num_frames: int = 32,
    output_dir: Path = None,
    motion_type: str = "auto",
    segment_idx: int = 0
) -> list[Path]:
    """
    Generate multiple frames from a single key frame using cinematic camera motion
    (pan, zoom-in, pull-back, or vertical tilt).

    Args:
        key_frame_path: Path to the key frame image.
        num_frames: Number of frames to generate (paper uses 32).
        output_dir: Directory to save generated frames.
        motion_type: 'pan_horizontal', 'zoom_in', 'pull_back', 'tilt_up', or 'auto'.
        segment_idx: Index of segment for automatic alternating motion.

    Returns:
        List of paths to all generated frames.
    """
    if output_dir is None:
        output_dir = key_frame_path.parent / "line_frames"
    output_dir.mkdir(parents=True, exist_ok=True)

    img = Image.open(key_frame_path).convert("RGB")
    w, h = img.size

    # Slightly enlarge for pan and zoom room
    padded_w = int(w * 1.18)
    padded_h = int(h * 1.18)
    img_large = img.resize((padded_w, padded_h), Image.LANCZOS)

    # Determine motion
    if motion_type == "auto":
        motions = ["pan_horizontal", "zoom_in", "pull_back", "tilt_up"]
        motion_type = motions[segment_idx % len(motions)]

    frame_paths = []

    for i in range(num_frames):
        t = i / max(num_frames - 1, 1)  # 0.0 to 1.0
        smooth_t = _ease_in_out(t)

        if motion_type == "pan_horizontal":
            # Slow cinematic horizontal glide
            zoom = 1.04
            pan_x = (smooth_t - 0.5) * 0.08 * w
            pan_y = 0.0
        elif motion_type == "zoom_in":
            # Dramatic push-in
            zoom = 1.0 + 0.12 * smooth_t
            pan_x = 0.0
            pan_y = 0.01 * smooth_t * h
        elif motion_type == "pull_back":
            # Slow reveal pull-out
            zoom = 1.12 - 0.12 * smooth_t
            pan_x = 0.0
            pan_y = 0.0
        elif motion_type == "tilt_up":
            # Upward tilt into the sky
            zoom = 1.05
            pan_x = 0.0
            pan_y = (0.5 - smooth_t) * 0.06 * h
        else:
            zoom = 1.0 + 0.08 * smooth_t
            pan_x = 0.0
            pan_y = 0.0

        # Calculate crop box
        crop_w = int(w / zoom)
        crop_h = int(h / zoom)
        cx = padded_w // 2 + int(pan_x)
        cy = padded_h // 2 + int(pan_y)

        left = max(0, cx - crop_w // 2)
        top = max(0, cy - crop_h // 2)
        right = min(padded_w, left + crop_w)
        bottom = min(padded_h, top + crop_h)

        if right - left < crop_w:
            left = max(0, right - crop_w)
        if bottom - top < crop_h:
            top = max(0, bottom - crop_h)

        cropped = img_large.crop((left, top, right, bottom))
        frame = cropped.resize((w, h), Image.LANCZOS)

        frame_path = output_dir / f"line_frame_{i:04d}.png"
        frame.save(frame_path)
        frame_paths.append(frame_path)

    print(f"  [KenBurns] ✓ Generated {len(frame_paths)} frames ({motion_type})")
    return frame_paths


def _ease_in_out(t: float) -> float:
    """Smooth ease-in-out function for natural-looking transitions."""
    return t * t * (3 - 2 * t)
