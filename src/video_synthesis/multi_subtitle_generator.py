"""
Multi-Language Subtitle Generator — Module 3, Enhancement 4

Generates stacked, dual-track / multi-language subtitle clips.
Positions:
  - Original text at top, font size ~26-28pt with black stroke.
  - Translated text below, font size ~20-22pt with subtle outline.
Uses script-aware system font routing (Segoe UI / YaHei / MS Gothic / Nirmala)
with explicit margins and dynamic vertical centering to ensure NO characters
or descenders are ever clipped or cut off by screen boundaries.

Reference: Section 4.4 and Section 8.1 of Progress.docx.
"""

from moviepy import TextClip, CompositeVideoClip, vfx
from src.config import IMAGE_WIDTH, IMAGE_HEIGHT, get_system_font


def _wrap_text(text: str, max_chars: int = 40) -> str:
    """Wrap text to prevent horizontal overflow while respecting natural word boundaries."""
    if not text:
        return ""
    # If text already contains explicit newlines from couplets, wrap each line individually
    input_lines = text.split("\n")
    all_wrapped = []
    for line in input_lines:
        line = line.strip()
        if not line:
            continue
        if len(line) <= max_chars:
            all_wrapped.append(line)
            continue
        # CJK text wrapping
        if any(('\u4e00' <= c <= '\u9fff') or ('\u3040' <= c <= '\u30ff') for c in line):
            cjk_limit = min(max_chars, 24)
            chunks = [line[i:i + cjk_limit] for i in range(0, len(line), cjk_limit)]
            all_wrapped.extend(chunks)
        else:
            # Western / Latin word wrapping on space
            words = line.split()
            curr = ""
            for w in words:
                if len(curr) + len(w) + 1 > max_chars:
                    if curr:
                        all_wrapped.append(curr.strip())
                    curr = w
                else:
                    curr = (curr + " " + w).strip()
            if curr:
                all_wrapped.append(curr.strip())
    return "\n".join(all_wrapped)


def create_stacked_subtitle_clip(
    primary_text: str,
    translated_texts: list[str],
    duration: float,
    position: str = "right_center"
) -> CompositeVideoClip:
    """
    Create a composite clip containing primary + translated subtitles stacked vertically.
    Dynamically measures all text blocks and centers/anchors the stack to ensure
    zero descender clipping and zero screen boundary overflow.

    Args:
        primary_text: The original poem line or segment text.
        translated_texts: List of translated texts (e.g. English, French, Chinese).
        duration: Duration of subtitle in seconds.
        position: Placement zone ("right_center" from paper, or "bottom_center").

    Returns:
        CompositeVideoClip with transparent background holding stacked subtitles.
    """
    fade_dur = min(0.4, duration * 0.15)

    if position == "right_center":
        box_width = int(IMAGE_WIDTH * 0.45)
        x_pos = int(IMAGE_WIDTH * 0.52)
        max_c = 28
    else:
        box_width = int(IMAGE_WIDTH * 0.82)
        x_pos = (IMAGE_WIDTH - box_width) // 2
        max_c = 44

    unpositioned_clips = []

    # 1. Primary Text Clip (Original Language)
    wrapped_primary = _wrap_text(primary_text, max_chars=max_c)
    font_primary = get_system_font(prefer_cjk=False, text=primary_text)
    clip_primary = TextClip(
        text=wrapped_primary,
        font=font_primary,
        font_size=26,
        color="white",
        stroke_color="black",
        stroke_width=2,
        margin=(16, 12),
        interline=6,
        method="caption",
        size=(box_width, None),
        text_align="center"
    ).with_duration(duration)
    unpositioned_clips.append(clip_primary)

    # 2. Translated Text Clip(s) stacked beneath
    for trans_txt in translated_texts:
        if not trans_txt or trans_txt.strip() == primary_text.strip():
            continue

        wrapped_trans = _wrap_text(trans_txt, max_chars=int(max_c * 1.15))
        font_trans = get_system_font(prefer_cjk=False, text=trans_txt)
        clip_trans = TextClip(
            text=wrapped_trans,
            font=font_trans,
            font_size=20,
            color="#E2E8F0",  # Soft luminous light-grey
            stroke_color="black",
            stroke_width=2,
            margin=(14, 10),
            interline=5,
            method="caption",
            size=(box_width, None),
            text_align="center"
        ).with_duration(duration)
        unpositioned_clips.append(clip_trans)

    # 3. Dynamic Vertical Anchoring to prevent clipping
    spacing = 6
    total_stack_height = sum(c.size[1] for c in unpositioned_clips) + spacing * (len(unpositioned_clips) - 1)

    if position == "right_center":
        # Centered vertically in the right portion of the frame
        ideal_y = (IMAGE_HEIGHT - total_stack_height) // 2
        # Clamp strictly between 24px from top and 24px from bottom
        start_y = max(24, min(ideal_y, IMAGE_HEIGHT - total_stack_height - 24))
    else:
        # Anchored to the lower third with 24px safe bottom margin
        start_y = max(24, IMAGE_HEIGHT - total_stack_height - 24)

    # 4. Position each clip and apply smooth fade transitions
    positioned_clips = []
    curr_y = start_y
    for clip in unpositioned_clips:
        c = clip.with_position((x_pos, curr_y))
        c = c.with_effects([vfx.FadeIn(fade_dur), vfx.FadeOut(fade_dur)])
        positioned_clips.append(c)
        curr_y += clip.size[1] + spacing

    composite = CompositeVideoClip(positioned_clips, size=(IMAGE_WIDTH, IMAGE_HEIGHT)).with_duration(duration)
    return composite


def create_title_clip(
    title: str,
    poet: str = "",
    duration: float = 4.0
) -> CompositeVideoClip:
    """
    Create a title card displaying the poem's title and author with safe margins.
    """
    display_text = title
    if poet:
        display_text += f"\n\n— {poet}"

    font_file = get_system_font(prefer_cjk=False, text=display_text)
    box_width = int(IMAGE_WIDTH * 0.82)

    txt_clip = TextClip(
        text=display_text,
        font=font_file,
        font_size=40,
        color="white",
        stroke_color="black",
        stroke_width=2,
        margin=(20, 16),
        interline=8,
        method="caption",
        size=(box_width, None),
        text_align="center"
    ).with_duration(duration)

    txt_clip = txt_clip.with_position("center")
    txt_clip = txt_clip.with_effects([vfx.FadeIn(0.8), vfx.FadeOut(0.8)])

    return txt_clip
