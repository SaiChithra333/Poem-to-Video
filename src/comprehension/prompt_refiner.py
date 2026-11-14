"""
Prompt Refiner Submodule — Module 1, Enhancement 2

Implements the LLM Self-Critique & Refinement loop.
Accepts a draft Stable Diffusion prompt generated from the 12 dimensions,
sends it to an LLM prompt expert to review and polish:
  (a) Resolves contradictory descriptors (e.g., bright daylight vs. night storm).
  (b) Adds clear spatial anchors (foreground, midground, background).
  (c) Balances concept density to prevent subject overlap.
  (d) Ensures optimal quality and art-style tokens.

Reference: Section 4.2 and Section 8.1 of Progress.docx.
"""

from src.llm_client import chat_completion
from src.config import PROMPT_REFINE, NEGATIVE_PROMPTS


PROMPT_CRITIC_SYSTEM_PROMPT = """You are an elite Stable Diffusion prompt engineering expert specializing in artistic situational visualizations.

Review the provided draft prompt and its context for:
1. Contradictory descriptors (e.g. "bright noon sun" combined with "foggy midnight").
2. Missing spatial anchors (specify clearly what is in the foreground, middle ground, background, perspective).
3. Overcrowded or conflicting subjects.
4. Optimal placement of quality and style tokens.

Respond with a JSON object:
{
    "refined_positive_prompt": "Polished, highly coherent positive prompt adhering to the artistic style",
    "refined_negative_prompt": "Refined negative prompt avoiding unwanted artifacts",
    "rationale": "Short explanation of improvements made"
}"""


def refine_prompt(
    draft_positive: str,
    draft_negative: str = None,
    scene_context: str = "",
    style_name: str = "",
    skip_refine: bool = False,
    visual_blueprint = None
) -> dict:
    """
    Perform LLM self-critique and refinement on a draft SD prompt.

    Args:
        draft_positive: Draft positive prompt string.
        draft_negative: Draft negative prompt string.
        scene_context: Background meaning/context of the scene.
        style_name: Name of target artistic style.
        skip_refine: If True or PROMPT_REFINE is False, skips LLM call.
        visual_blueprint: Optional VisualBlueprint to enforce global continuity.

    Returns:
        Dict with 'refined_positive_prompt', 'refined_negative_prompt', and 'rationale'.
    """
    draft_negative = draft_negative or NEGATIVE_PROMPTS

    if skip_refine or not PROMPT_REFINE:
        return {
            "refined_positive_prompt": draft_positive,
            "refined_negative_prompt": draft_negative,
            "rationale": "Prompt refinement skipped (PROMPT_REFINE=False)"
        }

    bp_info = ""
    if visual_blueprint:
        bp_info = f"""
**Global Continuity Constraints**:
- Persistent Location: {getattr(visual_blueprint, 'persistent_location', '')}
- Locked Color Palette: {getattr(visual_blueprint, 'color_script', '')}
- Unified Lighting: {getattr(visual_blueprint, 'unified_lighting', '')}
Keep this scene firmly anchored in the persistent location and locked color palette!"""

    user_prompt = f"""Review and optimize this Stable Diffusion prompt for a poetry situational artwork:

**Target Artistic Style**: {style_name}
**Scene Context**: {scene_context}
**Draft Positive Prompt**: {draft_positive}
**Draft Negative Prompt**: {draft_negative}{bp_info}

Refine the prompt into an elegant, coherent Stable Diffusion description. Retain key artistic, lighting, and locked color modifiers to maintain strict visual continuity with other scenes."""

    try:
        result = chat_completion(
            system_prompt=PROMPT_CRITIC_SYSTEM_PROMPT,
            user_prompt=user_prompt,
            temperature=0.4,
            max_tokens=1000,
            json_mode=True,
        )

        refined_pos = result.get("refined_positive_prompt", "").strip() or draft_positive
        refined_neg = result.get("refined_negative_prompt", "").strip() or draft_negative
        rationale = result.get("rationale", "Refined via LLM self-critique loop")

        return {
            "refined_positive_prompt": refined_pos,
            "refined_negative_prompt": refined_neg,
            "rationale": rationale
        }

    except Exception as e:
        print(f"  [PromptRefine] ⚠ Critique failed ({e}), using draft prompt")
        return {
            "refined_positive_prompt": draft_positive,
            "refined_negative_prompt": draft_negative,
            "rationale": f"Fallback to draft due to error: {e}"
        }
