"""
Paraphrase Submodule — Module 1, Step 1 (Enhanced)

Takes a poem and uses an LLM to produce a rich, detailed interpretation.
Extended to extract:
  - Literal meaning of each line
  - Visual imagery & background context
  - Symbolism
  - Dominant emotion label (e.g. melancholy, tranquility, joy, awe, longing)
  - Named Entity Recognition (NER) tags: PERSON, PLACE, NATURE_OBJECT, TIME, ABSTRACT

Reference: Section III-A of the base paper and Section 4.1 of the Enhanced Architecture.
"""

from src.llm_client import chat_completion


PARAPHRASE_SYSTEM_PROMPT = """You are a masterful literary scholar and poet. Your task is to deeply analyze 
a poem and provide a rich, vivid interpretation of each line along with emotion and entity signals 
for semantic scene generation.

For EACH line of the poem, you must provide:
1. "original": The original line text
2. "literal_meaning": Plain language meaning
3. "imagery": Vivid visual description of the scene (colors, objects, lighting, atmosphere)
4. "emotion": Detailed description of feelings and mood
5. "dominant_emotion": A concise single-word or short dominant emotion label (e.g., "tranquility", "melancholy", "joy", "awe", "longing", "solitude", "surprise")
6. "ner_tags": A list of entities found in this line, formatted as strings with category prefix:
   - PERSON (e.g., "PERSON: poet", "PERSON: hermit")
   - PLACE (e.g., "PLACE: courtyard", "PLACE: riverbank", "PLACE: mountain")
   - NATURE_OBJECT (e.g., "NATURE_OBJECT: peach blossoms", "NATURE_OBJECT: birds", "NATURE_OBJECT: rain")
   - TIME (e.g., "TIME: dawn", "TIME: spring night", "TIME: twilight")
   - ABSTRACT (e.g., "ABSTRACT: impermanence", "ABSTRACT: peace")
7. "symbolism": Metaphorical or deeper meaning
8. "background": Historical or cultural context if relevant

Your interpretation should be VISUALLY RICH — describing scenes for a painter to illustrate.

Respond in valid JSON format with this structure:
{
    "title": "Poem title (if identifiable, otherwise 'Untitled')",
    "poet": "Poet name (if identifiable, otherwise 'Unknown')",
    "overall_mood": "The overall emotional tone of the poem",
    "overall_setting": "The general time period, location, and atmosphere",
    "lines": [
        {
            "original": "Line text",
            "literal_meaning": "Plain language meaning",
            "imagery": "Vivid visual description",
            "emotion": "Detailed emotional tone",
            "dominant_emotion": "tranquility",
            "ner_tags": ["PERSON: scholar", "PLACE: timber chamber", "TIME: dawn"],
            "symbolism": "Metaphorical meaning",
            "background": "Cultural context"
        }
    ]
}"""


def paraphrase_poem(poem_text: str, language: str = "auto") -> dict:
    """
    Analyze a poem and produce a structured, rich interpretation with emotion and NER tags.

    Args:
        poem_text: The full text of the poem.
        language: "chinese", "english", or "auto" (auto-detect).

    Returns:
        A dictionary with the structured paraphrase including per-line analysis.
    """
    lang_instruction = ""
    if language == "chinese":
        lang_instruction = (
            "\nThis is a Chinese Tang poem. Pay special attention to traditional Chinese literary "
            "techniques like metaphor, juxtaposition, synecdoche, and implicit connotations. "
            "Provide all analysis, imagery, and entity tags in English for use in image generation."
        )
    elif language == "english":
        lang_instruction = "\nThis is an English poem. Analyze its imagery, meter, and literary devices in English."
    else:
        lang_instruction = (
            "\nDetect the language of this poem. If Chinese, explain the cultural context. "
            "Provide all analysis, imagery, and entity tags in English."
        )

    user_prompt = f"""Analyze the following poem in thorough detail:

---
{poem_text}
---
{lang_instruction}

Remember: Your descriptions should be VISUALLY RICH — as if describing scenes for a painter to illustrate."""

    print("  [Paraphrase] Sending poem to LLM for deep analysis...")

    result = chat_completion(
        system_prompt=PARAPHRASE_SYSTEM_PROMPT,
        user_prompt=user_prompt,
        temperature=0.7,
        max_tokens=6000,
        json_mode=True,
    )

    print(f"  [Paraphrase] ✓ Analyzed {len(result.get('lines', []))} lines")
    return result
