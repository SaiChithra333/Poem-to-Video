"""
Prompt Generator Submodule — Module 1, Step 3 (Enhanced)

Takes the 12-dimensional keywords from Step 1.2, constructs structured draft prompts,
and applies Iterative Prompt Refinement (Step R1 -> Step R2 -> Step R3).

Reference: Section III-A of the base paper and Section 4.2 of Progress.docx.
"""

from src.config import NEGATIVE_PROMPTS, STYLE_PRESETS, DEFAULT_STYLE, PROMPT_REFINE
from src.comprehension.prompt_refiner import refine_prompt


def generate_prompts(
    key_elements: list[dict],
    style: str = None,
    enable_refinement: bool = None,
    visual_blueprint = None
) -> list[dict]:
    """
    Generate and refine Stable Diffusion prompts from 12-dimensional keyword extractions.

    Args:
        key_elements: List of 12-dim keyword dicts (from key_element_extraction).
        style: Artistic style preset name.
        enable_refinement: Override flag for prompt refinement.
        visual_blueprint: Optional VisualBlueprint ensuring cross-scene visual coherence.

    Returns:
        List of dicts with 'positive_prompt', 'negative_prompt', 'rationale', and metadata.
    """
    style = style or DEFAULT_STYLE
    style_info = STYLE_PRESETS.get(style, STYLE_PRESETS[DEFAULT_STYLE])
    do_refine = PROMPT_REFINE if enable_refinement is None else enable_refinement

    prompts = []

    # Optimal ordering for SD prompts from the paper:
    PROMPT_ORDER = [
        "Quality",
        "Style",
        "Medium",
        "Type",
        "Subject",
        "Action",
        "Context",
        "Environment",
        "Lighting",
        "Color Scheme",
        "Artist",
        "Computer Graphics",
    ]

    bp_shots = getattr(visual_blueprint, "shot_progression", []) if visual_blueprint else []

    for i, elements in enumerate(key_elements):
        prompt_parts = []

        for dimension in PROMPT_ORDER:
            value = elements.get(dimension, "none")
            if value and str(value).strip().lower() != "none":
                prompt_parts.append(str(value).strip())

        # Add the style preset keywords
        if style_info.get("style_prompt"):
            prompt_parts.append(style_info["style_prompt"])

        draft_positive = ", ".join(prompt_parts)
        draft_positive = draft_positive.replace(",,", ",").replace("  ", " ").strip(", ")
        draft_negative = NEGATIVE_PROMPTS

        seg_id = elements.get("_segment_id", i)
        merged_text = elements.get("_merged_text", elements.get("_original_line", f"Line {i+1}"))
        line_indices = elements.get("_line_indices", [elements.get("_line_index", i)])
        lines = elements.get("_lines", [merged_text])

        shot_info = next((s for s in bp_shots if s.get("segment_id") == seg_id), {})

        # Step R2 & R3: Refine prompt with self-critique loop
        if do_refine:
            print(f"  [PromptGen] Refining prompt for segment {seg_id+1} via LLM self-critique...")
            refine_res = refine_prompt(
                draft_positive=draft_positive,
                draft_negative=draft_negative,
                scene_context=merged_text,
                style_name=style_info["name"],
                skip_refine=False,
                visual_blueprint=visual_blueprint
            )
            final_positive = refine_res["refined_positive_prompt"]
            final_negative = refine_res["refined_negative_prompt"]
            rationale = refine_res["rationale"]
        else:
            final_positive = draft_positive
            final_negative = draft_negative
            rationale = "Direct draft prompt"

        prompt_entry = {
            "positive_prompt": final_positive,
            "negative_prompt": final_negative,
            "draft_positive": draft_positive,
            "rationale": rationale,
            "segment_id": seg_id,
            "line_indices": line_indices,
            "lines": lines,
            "merged_text": merged_text,
            "dominant_emotion": elements.get("_dominant_emotion", "serenity"),
            "style": style,
            "dimensions": {k: v for k, v in elements.items() if not k.startswith("_")},
            "base_seed": getattr(visual_blueprint, "base_seed", 2024) if visual_blueprint else 2024,
            "color_script": getattr(visual_blueprint, "color_script", "") if visual_blueprint else "",
            "shot_type": shot_info.get("shot_type", "medium_focus"),
            "camera_motion": shot_info.get("camera_motion", "zoom_in")
        }

        prompts.append(prompt_entry)
        print(f"  [PromptGen] ✓ Segment {seg_id+1} prompt: {len(final_positive)} chars")

    print(f"  [PromptGen] ✓ Generated & refined {len(prompts)} prompt sets")
    return prompts


def format_prompt_for_display(prompt_entry: dict) -> str:
    """Pretty-print a prompt entry for debugging/logging."""
    seg_id = prompt_entry.get("segment_id", 0) + 1
    lines_text = " / ".join(prompt_entry.get("lines", []))
    output_lines = [
        f"═══ Segment {seg_id}: \"{lines_text}\" ═══",
        f"EMOTION: {prompt_entry.get('dominant_emotion', 'none')}",
        f"POSITIVE PROMPT:",
        f"  {prompt_entry['positive_prompt']}",
        f"NEGATIVE PROMPT:",
        f"  {prompt_entry['negative_prompt'][:120]}...",
        f"RATIONALE: {prompt_entry.get('rationale', '')}",
        f"DIMENSIONS:",
    ]
    for dim, val in prompt_entry.get("dimensions", {}).items():
        if str(val).lower() != "none":
            output_lines.append(f"  • {dim}: {val}")
    return "\n".join(output_lines)
