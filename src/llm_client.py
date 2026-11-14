"""
LLM Client — Unified interface for LLM providers.

Supports:
  - Google Gemini (free, recommended) with automatic model fallback
  - OpenAI / Groq / any OpenAI-compatible API
"""

import json
import os
import re
from src.config import GEMINI_API_KEY, OPENAI_API_KEY, OPENAI_BASE_URL, LLM_MODEL, GEMINI_MODEL_FALLBACKS

# Auto-detect provider
_gemini_val = GEMINI_API_KEY.strip() if GEMINI_API_KEY else ""
_openai_val = OPENAI_API_KEY.strip() if OPENAI_API_KEY else ""

if _gemini_val and not _gemini_val.startswith("your_"):
    LLM_PROVIDER = "gemini"
elif _openai_val and not _openai_val.startswith("your_"):
    LLM_PROVIDER = "openai"
else:
    LLM_PROVIDER = None


def chat_completion(
    system_prompt: str,
    user_prompt: str,
    temperature: float = 0.7,
    max_tokens: int = 2000,
    json_mode: bool = True,
) -> dict | str:
    """
    Send a chat completion request to the configured LLM.

    Args:
        system_prompt: System-level instruction.
        user_prompt: User message.
        temperature: Sampling temperature.
        max_tokens: Max output tokens.
        json_mode: If True, parse response as JSON.

    Returns:
        Parsed JSON dict if json_mode=True, else raw string.
    """
    if LLM_PROVIDER == "gemini":
        return _gemini_completion(system_prompt, user_prompt, temperature, max_tokens, json_mode)
    elif LLM_PROVIDER == "openai":
        return _openai_completion(system_prompt, user_prompt, temperature, max_tokens, json_mode)
    else:
        raise ValueError(
            "No LLM API key configured! Set GEMINI_API_KEY or OPENAI_API_KEY in .env"
        )


def _gemini_completion(
    system_prompt: str,
    user_prompt: str,
    temperature: float,
    max_tokens: int,
    json_mode: bool,
) -> dict | str:
    """Use Google Gemini API with fallback over supported active models."""
    from google import genai
    from google.genai import types

    client = genai.Client(api_key=GEMINI_API_KEY)
    
    # Try preferred model first, then fallbacks
    models_to_try = [LLM_MODEL] + [m for m in GEMINI_MODEL_FALLBACKS if m != LLM_MODEL]
    
    last_error = None
    for model_name in models_to_try:
        try:
            config = types.GenerateContentConfig(
                system_instruction=system_prompt,
                temperature=temperature,
                max_output_tokens=max_tokens,
            )
            if json_mode:
                config.response_mime_type = "application/json"

            response = client.models.generate_content(
                model=model_name,
                contents=user_prompt,
                config=config,
            )

            result_text = response.text.strip() if response.text else ""
            if not result_text:
                raise ValueError("Empty response from Gemini API")

            if json_mode:
                return _parse_json(result_text)
            return result_text

        except Exception as e:
            last_error = e
            # Try next model if 404 or 503
            err_msg = str(e).lower()
            if "not_found" in err_msg or "unavailable" in err_msg or "resource_exhausted" in err_msg:
                continue
            raise

    raise last_error or RuntimeError("All Gemini models failed")


def _openai_completion(
    system_prompt: str,
    user_prompt: str,
    temperature: float,
    max_tokens: int,
    json_mode: bool,
) -> dict | str:
    """Use OpenAI-compatible API (OpenAI, Groq, Together, etc.)."""
    from openai import OpenAI

    client = OpenAI(api_key=OPENAI_API_KEY, base_url=OPENAI_BASE_URL)
    model = LLM_MODEL or "gpt-3.5-turbo"

    kwargs = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        "temperature": temperature,
        "max_tokens": max_tokens,
    }

    if json_mode:
        kwargs["response_format"] = {"type": "json_object"}

    response = client.chat.completions.create(**kwargs)
    result_text = response.choices[0].message.content.strip()

    if json_mode:
        return _parse_json(result_text)
    return result_text


def _parse_json(text: str) -> dict:
    """Robustly parse JSON from LLM output with auto-recovery for truncated streams."""
    clean = text.strip()
    # Strip markdown block if present
    json_match = re.search(r'```(?:json)?\s*\n?(.*?)\n?```', clean, re.DOTALL)
    if json_match:
        clean = json_match.group(1).strip()

    try:
        return json.loads(clean)
    except json.JSONDecodeError:
        pass

    # Try finding outermost braces
    brace_match = re.search(r'\{.*\}', clean, re.DOTALL)
    if brace_match:
        try:
            return json.loads(brace_match.group())
        except Exception:
            pass

    # Attempt recovery: trim to last '}'
    last_brace = clean.rfind('}')
    if last_brace != -1:
        try:
            return json.loads(clean[:last_brace + 1])
        except Exception:
            pass

    # Balance unclosed brackets/braces
    stack = []
    in_string = False
    escape = False
    for ch in clean:
        if ch == '"' and not escape:
            in_string = not in_string
        elif not in_string:
            if ch in '{[':
                stack.append('}' if ch == '{' else ']')
            elif ch in '}]':
                if stack and stack[-1] == ch:
                    stack.pop()
        escape = (ch == '\\' and not escape)

    if stack:
        repaired = clean.rstrip().rstrip(',') + "".join(reversed(stack))
        try:
            return json.loads(repaired)
        except Exception:
            pass

    raise ValueError(f"Could not parse JSON from LLM response: {text[:200]}")
