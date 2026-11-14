"""
Visual Blueprint Generator — Module 1, Step 1c (Global Consistency Architecture)

Solves cross-scene visual inconsistency by establishing a unified "Color Script"
and "Persistent World Anchor" before generating individual prompts:
  1. Persistent Location Anchor — Single physical stage where the poem unfolds.
  2. Locked 4-Color Palette (Color Script) — Strict palette inherited by all frames.
  3. Unified Lighting & Time-of-Day — Prevents jarring temporal/exposure shifts.
  4. Cinematographic Shot Progression — Wide Establishing -> Medium Focus -> Macro Detail.
  5. Poetic Metaphor-to-Visual Rules — Translates figurative speech into physical continuity.
"""

from dataclasses import dataclass, asdict
from src.llm_client import chat_completion
from src.config import STYLE_PRESETS, DEFAULT_STYLE


@dataclass
class VisualBlueprint:
    persistent_location: str
    color_script: str
    unified_lighting: str
    artist_influences: str
    overall_atmosphere: str
    shot_progression: list[dict]
    base_seed: int

    def to_dict(self) -> dict:
        return asdict(self)


BLUEPRINT_SYSTEM_PROMPT = """You are an elite cinematic art director and visual stylist for multimedia poetry adaptations.
Your mission is to establish a unified "Global Visual Blueprint" for a poem so that when AI diffusion models generate images for each scene, they feel like frames from the EXACT SAME coherent film, sharing the same location, lighting, and 4-color palette.

Poetic Director Rules:
1. "Single World Anchor": All scenes must take place in the SAME persistent environment (e.g., a specific courtyard veranda, a lakeside meadow, a mountain pavilion), observed from different camera perspectives.
2. "Temporal Consistency": If the poem is set at dawn, ALL scenes must be at dawn. If a line mentions "sound of rain last night", depict the MORNING AFTERMATH in the garden (damp flagstones, dewy petals, mist), NOT a midnight hurricane.
3. "No Modern / Literal Clutter": Avoid literal mundane objects that break poetic genre (e.g. no modern beds or cartoon figures). Use classical landscape, architecture, and nature framing.
4. "Cinematic Shot Progression":
   - Segment 1: Wide establishing shot (the whole world / landscape).
   - Segment 2: Medium shot (focal interaction / living subjects like birds, swaying trees, rippling water).
   - Segment 3: Macro close-up / atmospheric culmination (dew on petals, leaf details, reflections).

Respond in valid JSON format:
{
    "persistent_location": "Detailed description of the single shared environment",
    "color_script": "4-color palette with names and hex codes (e.g. Ivory rice paper #F4EFE6, charcoal ink #2B2B2B, celadon green #9BB7A5, cinnabar accent #D97A7A)",
    "unified_lighting": "Single locked lighting condition across all scenes",
    "artist_influences": "Specific master artists matching the art style",
    "overall_atmosphere": "Emotional and sensory mood",
    "shot_progression": [
        {
            "segment_id": 0,
            "shot_type": "wide_establishing",
            "camera_motion": "pan_horizontal",
            "visual_focus": "Description of what the camera frames in the shared location",
            "metaphor_guidance": "How to translate poetic meaning into this physical space"
        }
    ]
}"""


def generate_visual_blueprint(
    paraphrase_data: dict,
    segments: list,
    style: str = None
) -> VisualBlueprint:
    """
    Generate a unified visual blueprint and color script for the poem.
    """
    style = style or DEFAULT_STYLE
    style_info = STYLE_PRESETS.get(style, STYLE_PRESETS[DEFAULT_STYLE])

    title = paraphrase_data.get("title", "Poem")
    poet = paraphrase_data.get("poet", "Unknown")
    overall_mood = paraphrase_data.get("overall_mood", "peaceful")
    overall_setting = paraphrase_data.get("overall_setting", "natural landscape")

    import hashlib
    base_seed = int(hashlib.md5(f"{title}_{style}_{poet}".encode()).hexdigest()[:6], 16) % 100000

    segment_summaries = []
    for s in segments:
        seg_id = getattr(s, "segment_id", s.get("segment_id", 0) if isinstance(s, dict) else 0)
        text = getattr(s, "merged_text", s.get("merged_text", "") if isinstance(s, dict) else "")
        emotion = getattr(s, "dominant_emotion", s.get("dominant_emotion", "") if isinstance(s, dict) else "")
        lit = getattr(s, "literal_meaning", s.get("literal_meaning", "") if isinstance(s, dict) else "")
        segment_summaries.append(f"Segment {seg_id+1}: \"{text}\" | Emotion: {emotion} | Meaning: {lit}")

    user_prompt = f"""Create a cohesive Visual Blueprint & Color Script for this poem:

**Title**: {title}
**Poet**: {poet}
**Art Style**: {style_info['name']} ({style})
**Overall Mood**: {overall_mood}
**Overall Setting**: {overall_setting}

**Poem Segments**:
{chr(10).join(segment_summaries)}

Ensure every segment is assigned a clear cinematographic shot role (wide, medium, or macro) within the SAME physical location, sharing the exact same color script and lighting."""

    try:
        print("  [VisualBlueprint] Generating global color script and spatial continuity blueprint...")
        data = chat_completion(
            system_prompt=BLUEPRINT_SYSTEM_PROMPT,
            user_prompt=user_prompt,
            temperature=0.4,
            max_tokens=2500,
            json_mode=True
        )

        shots = data.get("shot_progression", [])
        # Ensure every segment has a shot mapping
        while len(shots) < len(segments):
            idx = len(shots)
            shots.append({
                "segment_id": idx,
                "shot_type": "medium_focus" if idx % 2 == 1 else "macro_detail",
                "camera_motion": "zoom_in" if idx % 2 == 1 else "pan_horizontal",
                "visual_focus": f"Continuing the scene in {data.get('persistent_location', overall_setting)}",
                "metaphor_guidance": "Maintain visual continuity with surrounding scenes"
            })

        blueprint = VisualBlueprint(
            persistent_location=data.get("persistent_location", overall_setting),
            color_script=data.get("color_script", "harmonious natural palette, balanced tones"),
            unified_lighting=data.get("unified_lighting", "soft diffused natural daylight"),
            artist_influences=data.get("artist_influences", style_info.get("lora_keywords", "")),
            overall_atmosphere=data.get("overall_atmosphere", overall_mood),
            shot_progression=shots,
            base_seed=base_seed
        )
        print(f"  [VisualBlueprint] ✓ Location Anchor: \"{blueprint.persistent_location[:55]}...\"")
        print(f"  [VisualBlueprint] ✓ Color Script:    \"{blueprint.color_script[:55]}...\"")
        print(f"  [VisualBlueprint] ✓ Base Seed:        {blueprint.base_seed}")
        return blueprint

    except Exception as e:
        print(f"  [VisualBlueprint] ⚠ LLM Blueprint generation error ({e}), using default aesthetic blueprint")
        # Deterministic aesthetic blueprint fallback
        default_colors = {
            "chinese_ink": "Ivory rice paper (#F4EFE6), deep charcoal ink (#2B2B2B), misty celadon green (#9BB7A5), subtle cinnabar red (#D97A7A)",
            "watercolor": "Cold-press paper white (#FAF8F5), cerulean sky (#5D8AA8), amber gold (#FFBF00), sap green (#507D2A)",
            "oil_painting": "Warm titanium buff (#EBE1CE), burnt umber (#8A3324), cobalt twilight blue (#0047AB), golden ochre (#CC7722)",
        }.get(style, "balanced harmonious tones, ivory paper, rich charcoal, soft atmospheric wash")

        default_lighting = {
            "chinese_ink": "Soft luminous early dawn light, misty atmospheric glow, gentle diffused morning illumination",
            "watercolor": "Crisp clear morning sunlight, luminous airy atmosphere, translucent natural daylight",
            "oil_painting": "Golden hour twilight, warm glowing horizon, rich atmospheric chiaroscuro",
        }.get(style, "soft natural daylight, diffused atmospheric mist")

        shots = []
        motions = ["pan_horizontal", "zoom_in", "pull_back", "tilt_up"]
        types = ["wide_establishing", "medium_focus", "macro_detail", "atmospheric_wide"]
        for idx in range(len(segments)):
            shots.append({
                "segment_id": idx,
                "shot_type": types[min(idx, len(types) - 1)],
                "camera_motion": motions[min(idx, len(motions) - 1)],
                "visual_focus": f"Scene within {overall_setting}",
                "metaphor_guidance": "Preserve classical poetic metaphor and physical continuity"
            })

        return VisualBlueprint(
            persistent_location=overall_setting,
            color_script=default_colors,
            unified_lighting=default_lighting,
            artist_influences=style_info.get("lora_keywords", ""),
            overall_atmosphere=overall_mood,
            shot_progression=shots,
            base_seed=base_seed
        )
