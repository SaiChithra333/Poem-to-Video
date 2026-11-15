"""
Subtitle Generator — Module 3, Step 2

Creates subtitle text clips synchronized with audio duration.
Positions subtitles with safe margins and script-aware font routing,
ensuring that descenders, ascenders, and outlines are never clipped.

Reference: Section III-C of the base paper.
"""

from pathlib import Path

from moviepy import TextClip, CompositeVideoClip, vfx

from src.config import IMAGE_WIDTH, IMAGE_HEIGHT, VIDEO_FPS, get_system_font


def create_subtitle_clip(
    text: str,
    duration: float,
    font_size: int = 30,
    font_color: str = "white",
    stroke_color: str = "black",
    stroke_width: int = 2,
    position: str = "bottom_center",
    font: str = None,
) -> TextClip:
    """
    Create a styled subtitle clip for a poem line with safe margins.

    Args:
        text: Subtitle text.
        duration: Duration in seconds.
        font_size: Font size in pixels.
        font_color: Text color.
        stroke_color: Text outline color.
        stroke_width: Outline width.
        position: Where to position the subtitle ("bottom_center", "right_center", "center").
        font: Font file path or font name (must be available on the system).

    Returns:
        A MoviePy TextClip with the subtitle.
    """
    if not font:
        font = get_system_font(prefer_cjk=False, text=text)

    # Wrap long text
    max_chars_per_line = 36 if any('\u4e00' <= c <= '\u9fff' for c in text) else 44
    if len(text) > max_chars_per_line:
        words = text.split()
        lines = []
        current_line = ""
        for word in words:
            if len(current_line) + len(word) + 1 > max_chars_per_line:
                lines.append(current_line.strip())
                current_line = word
            else:
                current_line += " " + word
        if current_line:
            lines.append(current_line.strip())
        wrapped_text = "\n".join(lines)
    else:
        wrapped_text = text

    box_width = int(IMAGE_WIDTH * 0.45) if position == "right_center" else int(IMAGE_WIDTH * 0.82)

    try:
        txt_clip = TextClip(
            text=wrapped_text,
            font_size=font_size,
            color=font_color,
            font=font,
            stroke_color=stroke_color,
            stroke_width=stroke_width,
            margin=(16, 12),
            interline=6,
            method="caption",
            size=(box_width, None),
            text_align="center",
        )
    except Exception:
        txt_clip = TextClip(
            text=wrapped_text,
            font_size=font_size,
            color=font_color,
            stroke_color=stroke_color,
            stroke_width=stroke_width,
            margin=(16, 12),
            interline=6,
            method="caption",
            size=(box_width, None),
            text_align="center",
        )

    txt_clip = txt_clip.with_duration(duration)

    # Safe positioning
    if position == "right_center":
        x_pos = int(IMAGE_WIDTH * 0.52)
        y_pos = max(24, (IMAGE_HEIGHT - txt_clip.size[1]) // 2)
        txt_clip = txt_clip.with_position((x_pos, y_pos))
    elif position == "bottom_center":
        x_pos = (IMAGE_WIDTH - txt_clip.size[0]) // 2
        y_pos = max(24, IMAGE_HEIGHT - txt_clip.size[1] - 28)
        txt_clip = txt_clip.with_position((x_pos, y_pos))
    elif position == "center":
        txt_clip = txt_clip.with_position("center")

    # Add fade in/out for elegance
    fade_duration = min(0.5, duration * 0.15)
    txt_clip = txt_clip.with_effects([vfx.FadeIn(fade_duration), vfx.FadeOut(fade_duration)])

    return txt_clip


def create_title_clip(
    title: str,
    poet: str = "",
    duration: float = 4.0,
    font_size_title: int = 42,
    font_size_poet: int = 26,
) -> TextClip:
    """
    Create a title card clip showing the poem's title and author with safe margins.
    """
    display_text = title
    if poet:
        display_text += f"\n\n— {poet}"

    font_file = get_system_font(prefer_cjk=False, text=display_text)
    box_width = int(IMAGE_WIDTH * 0.82)
    try:
        txt_clip = TextClip(
            text=display_text,
            font_size=font_size_title,
            color="white",
            font=font_file,
            stroke_color="black",
            stroke_width=2,
            margin=(20, 16),
            interline=8,
            method="caption",
            size=(box_width, None),
            text_align="center",
        )
    except Exception:
        txt_clip = TextClip(
            text=display_text,
            font_size=font_size_title,
            color="white",
            stroke_color="black",
            stroke_width=2,
            margin=(20, 16),
            interline=8,
            method="caption",
            size=(box_width, None),
            text_align="center",
        )

    txt_clip = txt_clip.with_duration(duration)
    txt_clip = txt_clip.with_position("center")
    txt_clip = txt_clip.with_effects([vfx.FadeIn(1.0), vfx.FadeOut(1.0)])

    return txt_clip
