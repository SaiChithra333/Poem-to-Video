"""
Key Element Extraction Submodule — Module 1, Step 2 (Enhanced)

Takes the segmented poem and extracts keywords across the 12-dimensional
framework defined in the base paper:
  1. Subject        — people, animals, landscapes, buildings
  2. Action         — running, jumping, swimming, falling, blossoming
  3. Context        — scene composition, spatial relationships
  4. Environment    — indoor/outdoor, season, weather
  5. Lighting       — natural, golden hour, moonlight, foggy
  6. Artist         — reference artist style (Baishi Qi, Monet, Constable, etc.)
  7. Style          — Chinese ink, watercolor, oil painting
  8. Medium         — oil on canvas, ink on rice paper, digital painting
  9. Type           — landscape, still life, panoramic
  10. Color Scheme  — pastel, vibrant, muted, specific colors
  11. Computer Graphics — 3D, octane render, cycles, or none
  12. Quality       — HD, 4K, 8K, masterpiece

Processes per Segment, integrating multi-line visual context.
Reference: Section III-A of the base paper and Section 8.2 of Progress.docx.
"""

from src.llm_client import chat_completion
from src.config import TWELVE_DIMENSIONS, STYLE_PRESETS, DEFAULT_STYLE
from src.comprehension.semantic_segmentor import Segment


EXTRACTION_SYSTEM_PROMPT = """You are an expert at converting poetic imagery into structured visual descriptions 
for AI image generation. You will receive a detailed analysis of a poem segment and must extract 
keywords across exactly 12 dimensions.

Your output MUST be a JSON object with exactly these 12 keys. For each key, provide 
a concise, comma-separated list of relevant keywords. If a dimension is not applicable, 
write "none".

The 12 dimensions:
1. "Subject" — The main subjects/objects in the scene (people, animals, landscapes, buildings, flowers, etc.)
2. "Action" — What the subjects are doing (standing, flowing, blooming, falling, flying, etc.)
3. "Context" — Scene composition and spatial relationships (foreground, background, distant mountains, close-up, etc.)
4. "Environment" — Setting details (outdoor, spring morning, misty, riverbank, mountain path, etc.)
5. "Lighting" — Light conditions (golden hour, moonlight, soft dawn light, diffused, overcast, etc.)
6. "Artist" — Artist style reference (e.g. Baishi Qi, Ziqian Zhan, Sixun Li, Constable, Turner, Monet)
7. "Style" — Art style (traditional Chinese ink wash, impressionist, romantic landscape, etc.)
8. "Medium" — Material/technique (Chinese ink painting with rice paper texture, watercolor on paper, oil on canvas)
9. "Type" — Image type (landscape, portrait, still life, panoramic, etc.)
10. "Color Scheme" — Color palette (muted earth tones, vibrant greens and blues, monochrome with red accents, pastel)
11. "Computer Graphics" — CG keywords if applicable (8K render, octane render, or "none")
12. "Quality" — Quality keywords (masterpiece, best quality, highly detailed, superior quality, 8K UHD)

Output ONLY a valid JSON object, nothing else."""


def extract_key_elements(
    segments_or_data: list[Segment] | dict,
    style: str = None,
    visual_blueprint = None
) -> list[dict]:
    """
    Extract 12-dimensional keywords for each segment (or line).

    Args:
        segments_or_data: Either a list of Segment objects, or the legacy paraphrase dict.
        style: Artistic style preset name (from config.STYLE_PRESETS).
        visual_blueprint: Optional VisualBlueprint ensuring cross-scene visual coherence.

    Returns:
        A list of dicts, one per segment, each containing the 12-dimensional keywords.
    """
    style = style or DEFAULT_STYLE
    style_info = STYLE_PRESETS.get(style, STYLE_PRESETS[DEFAULT_STYLE])

    # Handle input type (list of Segment objects vs legacy paraphrase dict)
    items = []
    if isinstance(segments_or_data, list):
        items = segments_or_data
    elif isinstance(segments_or_data, dict):
        lines = segments_or_data.get("lines", [])
        for i, ld in enumerate(lines):
            items.append(Segment(
                segment_id=i,
                line_indices=[i],
                lines=[ld.get("original", "")],
                merged_text=ld.get("original", ""),
                dominant_emotion=ld.get("dominant_emotion", ld.get("emotion", "")),
                ner_tags=ld.get("ner_tags", []),
                literal_meaning=ld.get("literal_meaning", ""),
                imagery=ld.get("imagery", ""),
                symbolism=ld.get("symbolism", ""),
                background=ld.get("background", "")
            ))

    all_elements = []

    for i, seg in enumerate(items):
        seg_desc = f"Segment {seg.segment_id+1} (lines {seg.line_indices}): \"{seg.merged_text[:40]}\""
        print(f"  [KeyExtract] Processing {seg_desc}...")

        # Extract shot info and metaphor guidance from blueprint if available
        bp_context = ""
        if visual_blueprint:
            bp_shots = getattr(visual_blueprint, "shot_progression", [])
            shot_info = next((s for s in bp_shots if s.get("segment_id") == seg.segment_id), {})
            shot_type = shot_info.get("shot_type", "cinematic shot")
            cam_motion = shot_info.get("camera_motion", "pan_horizontal")
            metaphor = shot_info.get("metaphor_guidance", "")
            focus = shot_info.get("visual_focus", "")

            bp_context = f"""
**GLOBAL VISUAL BLUEPRINT (MANDATORY CONTINUITY)**:
- Persistent World Location: {getattr(visual_blueprint, 'persistent_location', '')}
- Locked 4-Color Palette: {getattr(visual_blueprint, 'color_script', '')}
- Unified Lighting: {getattr(visual_blueprint, 'unified_lighting', '')}
- Artist Influences: {getattr(visual_blueprint, 'artist_influences', '')}
- Cinematographic Shot Role: {shot_type} (Framing focus: {focus})
- Poetic Metaphor Guidance: {metaphor}
"""

        user_prompt = f"""Extract 12-dimensional visual keywords for this poem scene:

**Poem Lines**: {seg.merged_text}
**Literal Meaning**: {seg.literal_meaning}
**Imagery**: {seg.imagery}
**Dominant Emotion**: {seg.dominant_emotion}
**Key Entities**: {', '.join(seg.ner_tags) if seg.ner_tags else 'none'}
**Symbolism / Background**: {seg.symbolism} | {seg.background}

**Preferred Artistic Style**: {style_info['name']}
**Style Prompt Keywords**: {style_info['style_prompt']}{bp_context}

IMPORTANT COHERENCE RULES:
1. Ground this scene within the Persistent World Location. Do NOT invent unrelated modern rooms or random separate environments.
2. In 'Color Scheme', strictly align with the Locked 4-Color Palette.
3. In 'Lighting', strictly align with the Unified Lighting.
4. If the line describes past sounds or internal thoughts, depict the physical atmospheric aftermath in the garden/setting rather than literal disjointed events.
5. In 'Subject' and 'Action', make the descriptions visually concrete matching the shot role."""

        try:
            elements = chat_completion(
                system_prompt=EXTRACTION_SYSTEM_PROMPT,
                user_prompt=user_prompt,
                temperature=0.5,
                max_tokens=2000,
                json_mode=True,
            )

            # Validate all 12 dimensions are present
            for dim in TWELVE_DIMENSIONS:
                if dim not in elements or not elements[dim]:
                    elements[dim] = "none"

            elements["_segment_id"] = seg.segment_id
            elements["_line_indices"] = seg.line_indices
            elements["_lines"] = seg.lines
            elements["_merged_text"] = seg.merged_text
            elements["_dominant_emotion"] = seg.dominant_emotion
            all_elements.append(elements)

            active_dims = sum(1 for k, v in elements.items() if not k.startswith("_") and str(v).lower() != "none")
            print(f"  [KeyExtract] ✓ Extracted {active_dims}/12 active dimensions")

        except Exception as e:
            print(f"  [KeyExtract] ✗ Error on segment {i+1}: {e}")
            # Create robust fallback elements
            fallback = {dim: "none" for dim in TWELVE_DIMENSIONS}
            fallback["Subject"] = seg.literal_meaning or seg.merged_text
            fallback["Action"] = "in peaceful setting"
            fallback["Style"] = style_info["style_prompt"]
            fallback["Medium"] = "artistic painting"
            fallback["Lighting"] = "soft natural lighting"
            fallback["Quality"] = "masterpiece, best quality, 8K UHD"
            fallback["_segment_id"] = seg.segment_id
            fallback["_line_indices"] = seg.line_indices
            fallback["_lines"] = seg.lines
            fallback["_merged_text"] = seg.merged_text
            fallback["_dominant_emotion"] = seg.dominant_emotion
            all_elements.append(fallback)

    print(f"  [KeyExtract] ✓ Complete — {len(all_elements)} segments processed")
    return all_elements
