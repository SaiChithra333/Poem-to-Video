"""
Video Assembler — Module 3, Step 3 (Enhanced)

Combines:
  - Generated visual frames (Ken Burns zoom/pan sequences)
  - TTS audio narration (Edge TTS / gTTS)
  - Multi-language stacked subtitles (MoviePy TextClip with Windows CJK fonts)
  - Seamless cross-fade transitions between visual segments

Produces the final situational video in H.264 MP4 format.

Reference: Section III-C of the base paper and Section 8.2 of Progress.docx.
"""

import re
from pathlib import Path
from moviepy import (
    ImageClip, AudioFileClip, CompositeVideoClip,
    concatenate_videoclips, ColorClip, CompositeAudioClip
)

from src.config import VIDEO_FPS, VIDEO_CODEC, IMAGE_WIDTH, IMAGE_HEIGHT, OUTPUT_DIR
from src.video_synthesis.multi_subtitle_generator import create_stacked_subtitle_clip, create_title_clip


def assemble_segment_clip(
    frame_paths: list[Path],
    audio_path: Path,
    primary_text: str,
    translated_texts: list[str] = None,
    fps: int = None,
) -> CompositeVideoClip:
    """
    Assemble a video clip for a single poem visual segment.

    Combines image frames, audio narration, and stacked multi-language subtitles.

    Args:
        frame_paths: Paths to image frames for this segment.
        audio_path: Path to TTS audio file.
        primary_text: Original poem segment text.
        translated_texts: Translated texts for multi-language overlay.
        fps: Frames per second.

    Returns:
        CompositeVideoClip for this segment.
    """
    fps = fps or VIDEO_FPS
    translated_texts = translated_texts or []

    # 1. Determine duration from audio
    if audio_path and Path(audio_path).exists():
        audio = AudioFileClip(str(audio_path))
        duration = audio.duration
    else:
        audio = None
        # Default ~0.4s per character/word, minimum 3.5s
        duration = max(3.5, len(primary_text) * 0.35)

    # 2. Build visual sequence from Ken Burns frames
    if len(frame_paths) > 1:
        frame_duration = duration / len(frame_paths)
        clips = []
        for fp in frame_paths:
            clip = ImageClip(str(fp)).with_duration(frame_duration)
            clips.append(clip)
        video = concatenate_videoclips(clips, method="compose")
    elif frame_paths:
        video = ImageClip(str(frame_paths[0])).with_duration(duration)
    else:
        # Fallback dark clip
        video = ColorClip(size=(IMAGE_WIDTH, IMAGE_HEIGHT), color=(20, 20, 30)).with_duration(duration)

    video = video.resized((IMAGE_WIDTH, IMAGE_HEIGHT))

    # 3. Create multi-language stacked subtitle overlay
    subtitle_clip = create_stacked_subtitle_clip(
        primary_text=primary_text,
        translated_texts=translated_texts,
        duration=duration,
        position="right_center"
    )

    # 4. Composite video + subtitles
    composite = CompositeVideoClip(
        [video, subtitle_clip],
        size=(IMAGE_WIDTH, IMAGE_HEIGHT)
    ).with_duration(duration)

    # 5. Attach audio track
    if audio is not None:
        composite = composite.with_audio(audio)

    return composite


def assemble_title_card(
    title: str,
    poet: str = "",
    duration: float = 3.5,
    background_color: tuple = (12, 14, 25),
) -> CompositeVideoClip:
    """
    Create a title card clip with a deep cinematic background.
    """
    bg = ColorClip(
        size=(IMAGE_WIDTH, IMAGE_HEIGHT),
        color=background_color
    ).with_duration(duration)

    title_text = create_title_clip(title, poet, duration)

    composite = CompositeVideoClip(
        [bg, title_text],
        size=(IMAGE_WIDTH, IMAGE_HEIGHT)
    ).with_duration(duration)

    return composite


def assemble_full_video(
    segment_clips: list[CompositeVideoClip],
    transition_clips: list = None,
    title: str = "Untitled Poem",
    poet: str = "",
    output_path: Path = None,
    fps: int = None,
    include_title_card: bool = True,
    bgm_path: Path = None,
) -> Path:
    """
    Assemble the complete situational video from all segment clips and transitions.

    Args:
        segment_clips: List of CompositeVideoClips for each segment.
        transition_clips: Optional transition clips between segments.
        title: Poem title.
        poet: Poet name.
        output_path: Destination MP4 file path.
        fps: Frames per second.
        include_title_card: Whether to prepend title card.
        bgm_path: Optional path to ambient background audio bed.

    Returns:
        Path to the saved MP4 video.
    """
    fps = fps or VIDEO_FPS
    output_path = output_path or (OUTPUT_DIR / f"{_sanitize_filename(title)}.mp4")
    output_path.parent.mkdir(parents=True, exist_ok=True)

    all_clips = []

    # 1. Title card
    if include_title_card:
        title_card = assemble_title_card(title, poet)
        all_clips.append(title_card)

    # 2. Interleave segments and transitions
    for i, clip in enumerate(segment_clips):
        all_clips.append(clip)
        if transition_clips and i < len(transition_clips) and i < len(segment_clips) - 1:
            all_clips.append(transition_clips[i])

    # 3. Concatenate all clips
    print(f"  [VideoAssembly] Concatenating {len(all_clips)} sequence elements...")
    final = concatenate_videoclips(all_clips, method="compose")

    # 3b. Mix ambient background music / soundscape if provided
    if bgm_path and Path(bgm_path).exists():
        try:
            import numpy as np
            from moviepy import concatenate_audioclips
            bgm_clip = AudioFileClip(str(bgm_path))
            if bgm_clip.duration < final.duration:
                n_loops = int(np.ceil(final.duration / max(bgm_clip.duration, 0.1))) + 1
                bgm_clip = concatenate_audioclips([bgm_clip] * n_loops)
            bgm_clip = bgm_clip.subclipped(0, final.duration)
            if final.audio is not None:
                final = final.with_audio(CompositeAudioClip([final.audio, bgm_clip]))
            else:
                final = final.with_audio(bgm_clip)
            print(f"  [VideoAssembly] ✓ Mixed ambient background soundscape ({Path(bgm_path).name})")
        except Exception as e:
            print(f"  [VideoAssembly] ⚠ BGM mixing notice ({e}), proceeding with primary audio")

    # 4. Render final MP4
    print(f"  [VideoAssembly] Rendering video to: {output_path.name}...")
    final.write_videofile(
        str(output_path),
        fps=fps,
        codec=VIDEO_CODEC,
        audio_codec="aac",
        threads=4,
        logger=None,
    )

    # Clean up handles
    final.close()
    for clip in all_clips:
        try:
            clip.close()
        except Exception:
            pass

    print(f"  [VideoAssembly] ✓ Situational video successfully created: {output_path}")
    return output_path


def _sanitize_filename(name: str) -> str:
    """Convert string to a safe, clean Windows filename."""
    # If the title contains English before parenthesis, prefer the clean Latin part
    clean = re.sub(r'[\(（][^)）]*[\)）]', '', name).strip()
    target = clean if clean else name
    safe = re.sub(r'[^\w\s-]', '', target)
    safe = re.sub(r'[\s]+', '_', safe).strip('_')
    return safe[:60] or "Poem_Video"
