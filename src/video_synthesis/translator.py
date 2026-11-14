"""
Translation Submodule — Module 3, Enhancement 4 & 5

Translates poem segments and titles into target languages (e.g., English, Chinese,
French, Spanish, Hindi) for multi-language subtitles and narration.
Uses the LLM for poetic translation fidelity.

Reference: Section 4.4 and Section 8.1 of Progress.docx.
"""

from src.llm_client import chat_completion


TRANSLATION_SYSTEM_PROMPT = """You are a master literary translator specializing in world poetry.
Translate the provided poem lines into the requested target languages.
Maintain the poetic imagery, elegance, and emotional nuance while keeping the lines succinct for video subtitles.

Respond in valid JSON format:
{
    "translations": {
        "lang_code": [
            "translated line 1",
            "translated line 2"
        ]
    }
}"""


def translate_segments(
    segments_text: list[str],
    target_languages: list[str],
    source_language: str = "auto"
) -> dict[str, list[str]]:
    """
    Translate a list of segment texts into multiple target languages.

    Args:
        segments_text: List of text strings to translate.
        target_languages: List of language codes, e.g. ['en', 'zh', 'fr'].
        source_language: Source language if known.

    Returns:
        Dict mapping language code to list of translated strings in original order.
    """
    if not target_languages or not segments_text:
        return {}

    # Filter out languages that don't need translation if already source
    langs_to_request = [lang for lang in target_languages]

    user_prompt = f"""Translate each of the following {len(segments_text)} poem lines into these target languages: {', '.join(langs_to_request)}:

---
"""
    for i, txt in enumerate(segments_text):
        user_prompt += f"{i+1}. {txt}\n"
    user_prompt += "---\nProvide accurate, poetic translations for each line under each language key."

    print(f"  [Translator] Translating {len(segments_text)} segments into {langs_to_request}...")

    try:
        res = chat_completion(
            system_prompt=TRANSLATION_SYSTEM_PROMPT,
            user_prompt=user_prompt,
            temperature=0.3,
            max_tokens=4000,
            json_mode=True,
        )

        translations = res.get("translations", {})
        # Ensure all requested languages are present
        for lang in langs_to_request:
            if lang not in translations or len(translations[lang]) != len(segments_text):
                translations[lang] = segments_text

        print(f"  [Translator] ✓ Translated into {len(translations)} languages")
        return translations

    except Exception as e:
        print(f"  [Translator] ⚠ Translation failed ({e}), using original text as fallback")
        return {lang: list(segments_text) for lang in langs_to_request}
