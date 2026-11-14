"""
Multi-Language Subtitle Generator — Module 3, Enhancement 4

Generates stacked, dual-track / multi-language subtitle clips.
Positions:
  - Original text at top (65% left, 35% top), font size ~26-30pt with black stroke.
  - Translated text below (65% left, 50% top), font size ~20-22pt with subtle outline.
Uses detected Windows system fonts (e.g. Microsoft YaHei / SimSun / Arial)
so Chinese characters and Western alphabets render with high visual clarity.

Reference: Section 4.4 and Section 8.1 of Progress.docx.
"""

from moviepy import TextClip, CompositeVideoClip, vfx
from src.config import IMAGE_WIDTH, IMAGE_HEIGHT, get_system_font


def _wrap_text(text: str, max_chars: int = 24) -> str:
    """Wrap text to prevent overflow."""
    if len(text) <= max_chars:
        return text
    # Chinese text wrapping
    if any('\u4e00' <= c <= '\u9fff' for c in text):
        chunks = [text[i:i+max_chars] for i in range(0, len(text), max_chars)]
        return "\n".join(chunks)
    # Western text wrapping on spaces
    words = text.split()
    lines = []
    curr = ""
    for w in words:
        if len(curr) + len(w) + 1 > max_chars:
            lines.append(curr.strip())
            curr = w
        else:
            curr += " " + w
    if curr:
        lines.append(curr.strip())
    return "\n".join(lines)


def create_stacked_subtitle_clip(
    primary_text: str,
    translated_texts: list[str],
    duration: float,
    position: str = "right_center"
) -> CompositeVideoClip:
    """
    Create a composite clip containing primary + translated subtitles stacked vertically.

    Args:
        primary_text: The original poem line or segment text.
        translated_texts: List of translated texts (e.g. English, French, Chinese).
        duration: Duration of subtitle in seconds.
        position: Placement zone ("right_center" from paper, or "bottom_center").

    Returns:
        CompositeVideoClip with transparent background holding stacked subtitles.
    """
    font_primary = get_system_font(prefer_cjk=True, text=primary_text)
    sub_clips = []

    fade_dur = min(0.4, duration * 0.15)
    box_width = int(IMAGE_WIDTH * 0.45)

    # 1. Primary Text Clip (Original Language)
    wrapped_primary = _wrap_text(primary_text, max_chars=22)
    clip_primary = TextClip(
        text=wrapped_primary,
        font=font_primary,
        font_size=28,
        color="white",
        stroke_color="black",
        stroke_width=2,
        method="caption",
        size=(box_width, None),
        text_align="center"
    ).with_duration(duration)

    if position == "right_center":
        x_pos = int(IMAGE_WIDTH * 0.52)
        y_pos = int(IMAGE_HEIGHT * 0.35)
    else:
        x_pos = int((IMAGE_WIDTH - box_width) // 2)
        y_pos = int(IMAGE_HEIGHT * 0.65)

    clip_primary = clip_primary.with_position((x_pos, y_pos))
    clip_primary = clip_primary.with_effects([vfx.FadeIn(fade_dur), vfx.FadeOut(fade_dur)])
    sub_clips.append(clip_primary)

    # 2. Translated Text Clip(s) stacked beneath
    curr_y = y_pos + clip_primary.size[1] + 10

    for i, trans_txt in enumerate(translated_texts):
        if not trans_txt or trans_txt.strip() == primary_text.strip():
            continue

        wrapped_trans = _wrap_text(trans_txt, max_chars=28)
        font_trans = get_system_font(prefer_cjk=True, text=trans_txt)
        clip_trans = TextClip(
            text=wrapped_trans,
            font=font_trans,
            font_size=20,
            color="#E0E6ED",  # Soft luminous light-grey
            stroke_color="black",
            stroke_width=2,
            method="caption",
            size=(box_width, None),
            text_align="center"
        ).with_duration(duration)

        clip_trans = clip_trans.with_position((x_pos, curr_y))
        clip_trans = clip_trans.with_effects([vfx.FadeIn(fade_dur), vfx.FadeOut(fade_dur)])
        sub_clips.append(clip_trans)
        curr_y += clip_trans.size[1] + 8

    composite = CompositeVideoClip(sub_clips, size=(IMAGE_WIDTH, IMAGE_HEIGHT)).with_duration(duration)
    return composite


def create_title_clip(
    title: str,
    poet: str = "",
    duration: float = 4.0
) -> CompositeVideoClip:
    """
    Create a title card displaying the poem's title and author.
    """
    display_text = title
    if poet:
        display_text += f"\n\n— {poet}"

    font_file = get_system_font(prefer_cjk=True, text=display_text)
    box_width = int(IMAGE_WIDTH * 0.8)

    txt_clip = TextClip(
        text=display_text,
        font=font_file,
        font_size=42,
        color="white",
        stroke_color="black",
        stroke_width=2,
        method="caption",
        size=(box_width, None),
        text_align="center"
    ).with_duration(duration)

    txt_clip = txt_clip.with_position("center")
    txt_clip = txt_clip.with_effects([vfx.FadeIn(0.8), vfx.FadeOut(0.8)])

    return txt_clip
