"""
Subtitle Generator — Module 3, Step 2

Creates subtitle text clips synchronized with audio duration.
The paper positions subtitles centrally at the video's right portion.

Uses MoviePy's TextClip for rendering styled subtitles.

Reference: Section III-C of the paper.
"""

from pathlib import Path

from moviepy import TextClip, CompositeVideoClip, vfx

from src.config import IMAGE_WIDTH, IMAGE_HEIGHT, VIDEO_FPS, get_system_font


def create_subtitle_clip(
    text: str,
    duration: float,
    font_size: int = 36,
    font_color: str = "white",
    stroke_color: str = "black",
    stroke_width: int = 2,
    position: str = "right_center",
    font: str = "DejaVu-Sans",
) -> TextClip:
    """
    Create a styled subtitle clip for a poem line.

    Args:
        text: Subtitle text.
        duration: Duration in seconds.
        font_size: Font size in pixels.
        font_color: Text color.
        stroke_color: Text outline color.
        stroke_width: Outline width.
        position: Where to position the subtitle.
        font: Font name (must be available on the system).

    Returns:
        A MoviePy TextClip with the subtitle.
    """
    # Wrap long text
    max_chars_per_line = 25
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

    try:
        txt_clip = TextClip(
            text=wrapped_text,
            font_size=font_size,
            color=font_color,
            font=font,
            stroke_color=stroke_color,
            stroke_width=stroke_width,
            method="caption",
            size=(IMAGE_WIDTH // 3, None),
            text_align="center",
        )
    except Exception:
        # Fallback if the font is not available
        txt_clip = TextClip(
            text=wrapped_text,
            font_size=font_size,
            color=font_color,
            stroke_color=stroke_color,
            stroke_width=stroke_width,
            method="caption",
            size=(IMAGE_WIDTH // 3, None),
            text_align="center",
        )

    txt_clip = txt_clip.with_duration(duration)

    # Position: right-center as specified in the paper
    if position == "right_center":
        x_pos = int(IMAGE_WIDTH * 0.65)
        y_pos = int(IMAGE_HEIGHT * 0.4)
        txt_clip = txt_clip.with_position((x_pos, y_pos))
    elif position == "bottom_center":
        txt_clip = txt_clip.with_position(("center", "bottom"))
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
    font_size_title: int = 48,
    font_size_poet: int = 28,
) -> TextClip:
    """
    Create a title card clip showing the poem's title and author.

    Args:
        title: Poem title.
        poet: Poet's name.
        duration: Duration of the title card.

    Returns:
        A MoviePy TextClip for the title card.
    """
    display_text = title
    if poet:
        display_text += f"\n\n— {poet}"

    font_file = get_system_font(prefer_cjk=True, text=display_text)
    try:
        txt_clip = TextClip(
            text=display_text,
            font_size=font_size_title,
            color="white",
            font=font_file,
            stroke_color="black",
            stroke_width=2,
            method="caption",
            size=(int(IMAGE_WIDTH * 0.8), None),
            text_align="center",
        )
    except Exception:
        txt_clip = TextClip(
            text=display_text,
            font_size=font_size_title,
            color="white",
            stroke_color="black",
            stroke_width=2,
            method="caption",
            size=(int(IMAGE_WIDTH * 0.8), None),
            text_align="center",
        )

    txt_clip = txt_clip.with_duration(duration)
    txt_clip = txt_clip.with_position("center")
    txt_clip = txt_clip.with_effects([vfx.FadeIn(1.0), vfx.FadeOut(1.0)])

    return txt_clip
