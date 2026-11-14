"""
Single Frame Generator — Module 2, Step 1 (Enhanced)

Generates key-frame artwork for each poem segment using AI image models.

Supported Backends:
  - "pollinations": Fast, high-quality, free diffusion generation (FLUX / SDXL).
  - "huggingface": HuggingFace Inference API router.
  - "stability": Stability AI API.
  - "placeholder": Graceful artistic gradient generator with system font support.

Reference: Section III-B of the base paper.
"""

import io
import re
import math
import random
import time
import requests
import urllib.parse
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

from src.config import (
    IMAGE_PROVIDER, IMAGE_WIDTH, IMAGE_HEIGHT,
    STABILITY_API_KEY, HUGGINGFACE_API_TOKEN,
    HF_IMAGE_MODEL, TEMP_DIR, get_system_font,
    STYLE_PRESETS
)


def generate_single_frame(
    prompt_entry: dict,
    output_path: Path = None,
    provider: str = None,
) -> Path:
    """
    Generate a single image from an SD prompt.

    Args:
        prompt_entry: Dict with 'positive_prompt', 'negative_prompt', 'segment_id'.
        output_path: Where to save the image. Auto-generated if None.
        provider: Override image provider from config.

    Returns:
        Path to the generated image file.
    """
    provider = provider or IMAGE_PROVIDER
    seg_idx = prompt_entry.get("segment_id", prompt_entry.get("line_index", 0))

    if output_path is None:
        output_path = TEMP_DIR / f"frame_seg_{seg_idx:03d}.png"
    output_path.parent.mkdir(parents=True, exist_ok=True)

    if output_path.exists() and output_path.stat().st_size > 5000:
        print(f"  [ImageGen] ↺ Reusing existing frame {output_path.name}")
        return output_path

    print(f"  [ImageGen] Generating frame for segment {seg_idx+1} via '{provider}'...")

    if provider == "pollinations":
        return _generate_pollinations(prompt_entry, output_path)
    elif provider == "huggingface":
        return _generate_huggingface(prompt_entry, output_path)
    elif provider == "stability":
        return _generate_stability(prompt_entry, output_path)
    elif provider == "placeholder":
        return _generate_placeholder(prompt_entry, output_path)
    else:
        # Default to pollinations for reliability
        return _generate_pollinations(prompt_entry, output_path)


def generate_all_frames(
    prompts: list[dict],
    output_dir: Path = None,
    provider: str = None,
) -> list[Path]:
    """
    Generate key-frame images for all poem segments sequentially.

    Args:
        prompts: List of prompt entries.
        output_dir: Directory to save images.
        provider: Image generation provider.

    Returns:
        List of paths to generated images.
    """
    output_dir = output_dir or (TEMP_DIR / "frames")
    output_dir.mkdir(parents=True, exist_ok=True)

    paths = []
    for i, prompt_entry in enumerate(prompts):
        seg_idx = prompt_entry.get("segment_id", i)
        output_path = output_dir / f"frame_seg_{seg_idx:03d}.png"
        try:
            path = generate_single_frame(prompt_entry, output_path, provider)
            paths.append(path)
        except Exception as e:
            print(f"  [ImageGen] ✗ Failed segment {seg_idx+1}: {e}")
            path = _generate_placeholder(prompt_entry, output_path)
            paths.append(path)
        if i < len(prompts) - 1:
            time.sleep(2.0)

    print(f"  [ImageGen] ✓ Generated {len(paths)} frames")
    return paths


# ─── Provider Implementations ────────────────────────────────────────────────


def _generate_pollinations(prompt_entry: dict, output_path: Path) -> Path:
    """Generate image using Pollinations AI (FLUX / SANA backend)."""
    if output_path.exists() and output_path.stat().st_size > 5000:
        print(f"  [ImageGen] ↺ Reusing existing frame: {output_path.name}")
        return output_path

    # Extract unified dimensions for global visual coherence
    subject = prompt_entry.get("dimensions", {}).get("Subject", "")
    action = prompt_entry.get("dimensions", {}).get("Action", "")
    lighting = prompt_entry.get("dimensions", {}).get("Lighting", "")
    color_script = prompt_entry.get("color_script", "") or prompt_entry.get("dimensions", {}).get("Color Scheme", "")
    style_key = prompt_entry.get("style", "chinese_ink")
    style_preset = STYLE_PRESETS.get(style_key, {}).get("style_prompt", style_key)

    prompt_tokens = []
    if subject and str(subject).lower() != "none":
        prompt_tokens.append(str(subject).strip()[:70])
    if action and str(action).lower() != "none":
        prompt_tokens.append(str(action).strip()[:50])
    if color_script and str(color_script).lower() != "none":
        # Extract concise color tokens for URL
        cs_clean = color_script.split("(")[0].strip() if "(" in color_script else color_script
        prompt_tokens.append(f"palette: {cs_clean[:45]}")
    if lighting and str(lighting).lower() != "none":
        prompt_tokens.append(str(lighting).strip()[:35])
    prompt_tokens.append(style_preset)
    prompt_tokens.append("masterpiece, 8k uhd")

    focused_prompt = ", ".join(prompt_tokens)
    if len(focused_prompt) > 230:
        focused_prompt = focused_prompt[:225].rsplit(" ", 1)[0]

    # Shared seed family ensures correlated generative latents
    seg_idx = prompt_entry.get("segment_id", 0)
    base_seed = prompt_entry.get("base_seed", 2024)
    seed = (base_seed + seg_idx * 17) % 100000

    encoded_prompt = urllib.parse.quote(focused_prompt.strip())

    url_primary = (
        f"https://image.pollinations.ai/prompt/{encoded_prompt}"
        f"?width={IMAGE_WIDTH}&height={IMAGE_HEIGHT}&nologo=true&seed={seed}&model=sana"
    )
    url_fallback = (
        f"https://image.pollinations.ai/prompt/{encoded_prompt}"
        f"?width={IMAGE_WIDTH}&height={IMAGE_HEIGHT}&nologo=true&seed={seed}"
    )

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    }

    max_retries = 4
    for attempt in range(max_retries):
        url = url_primary if attempt < 2 else url_fallback
        try:
            response = requests.get(url, headers=headers, timeout=60)
            if response.status_code == 200 and len(response.content) > 5000:
                image = Image.open(io.BytesIO(response.content)).convert("RGB")
                if image.size != (IMAGE_WIDTH, IMAGE_HEIGHT):
                    image = image.resize((IMAGE_WIDTH, IMAGE_HEIGHT), Image.LANCZOS)
                image.save(output_path)
                print(f"  [ImageGen] ✓ Saved via Pollinations: {output_path.name}")
                return output_path
            elif response.status_code in (402, 429):
                match = re.search(r"Retry after (\d+)s", response.text)
                if match:
                    wait_s = int(match.group(1)) + 2
                else:
                    wait_s = 15 + attempt * 10
                print(f"  [ImageGen] ⏳ Rate limited ({response.status_code}): waiting {wait_s}s cooldown before retry {attempt+1}/{max_retries}...")
                time.sleep(wait_s)
            else:
                print(f"  [ImageGen] ⚠ Status {response.status_code}, retrying in 4s...")
                time.sleep(4)
        except Exception as e:
            print(f"  [ImageGen] ⚠ Attempt {attempt+1} error ({e}), retrying in 4s...")
            time.sleep(4)

    print("  [ImageGen] ⚠ Pollinations exhausted, falling back to procedural artistic generator")
    return _generate_placeholder(prompt_entry, output_path)


def _generate_huggingface(prompt_entry: dict, output_path: Path) -> Path:
    """Generate image using HuggingFace Inference API router."""
    if not HUGGINGFACE_API_TOKEN:
        print("  [ImageGen] ⚠ No HuggingFace token, falling back to Pollinations")
        return _generate_pollinations(prompt_entry, output_path)

    API_URL = f"https://router.huggingface.co/hf-inference/models/{HF_IMAGE_MODEL}"
    headers = {"Authorization": f"Bearer {HUGGINGFACE_API_TOKEN}"}

    payload = {
        "inputs": prompt_entry["positive_prompt"],
        "parameters": {
            "negative_prompt": prompt_entry.get("negative_prompt", ""),
            "num_inference_steps": 28,
            "guidance_scale": 7.0,
        }
    }

    max_retries = 2
    for attempt in range(max_retries):
        try:
            response = requests.post(API_URL, headers=headers, json=payload, timeout=60)
            if response.status_code == 200:
                image = Image.open(io.BytesIO(response.content)).convert("RGB")
                image = image.resize((IMAGE_WIDTH, IMAGE_HEIGHT), Image.LANCZOS)
                image.save(output_path)
                print(f"  [ImageGen] ✓ Saved via HF: {output_path.name}")
                return output_path
        except Exception as e:
            print(f"  [ImageGen] ⚠ HF error: {e}")
            time.sleep(3)

    print("  [ImageGen] ⚠ HuggingFace unavailable, falling back to Pollinations")
    return _generate_pollinations(prompt_entry, output_path)


def _generate_stability(prompt_entry: dict, output_path: Path) -> Path:
    """Generate image using Stability AI API."""
    if not STABILITY_API_KEY:
        return _generate_pollinations(prompt_entry, output_path)

    API_URL = "https://api.stability.ai/v1/generation/stable-diffusion-xl-1024-v1-0/text-to-image"
    headers = {
        "Authorization": f"Bearer {STABILITY_API_KEY}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    payload = {
        "text_prompts": [
            {"text": prompt_entry["positive_prompt"], "weight": 1.0},
            {"text": prompt_entry["negative_prompt"], "weight": -1.0}
        ],
        "cfg_scale": 7,
        "width": IMAGE_WIDTH,
        "height": IMAGE_HEIGHT,
        "steps": 30,
        "samples": 1,
    }

    try:
        response = requests.post(API_URL, headers=headers, json=payload, timeout=120)
        if response.status_code == 200:
            import base64
            data = response.json()
            image_data = base64.b64decode(data["artifacts"][0]["base64"])
            image = Image.open(io.BytesIO(image_data)).convert("RGB")
            image.save(output_path)
            print(f"  [ImageGen] ✓ Saved via Stability: {output_path.name}")
            return output_path
    except Exception as e:
        print(f"  [ImageGen] ✗ Stability error: {e}")

    return _generate_pollinations(prompt_entry, output_path)


def _generate_placeholder(prompt_entry: dict, output_path: Path) -> Path:
    """
    Generate an authentic, high-resolution procedural artistic painting matching
    the poem's aesthetic style without any placeholder text or debug placards.
    """
    seg_idx = prompt_entry.get("segment_id", 0)
    style = str(prompt_entry.get("style", "")).lower()
    seed = (seg_idx + 1) * 777

    if "ink" in style or "chinese" in style:
        img = _procedural_chinese_ink(IMAGE_WIDTH, IMAGE_HEIGHT, seed)
    elif "watercolor" in style:
        img = _procedural_watercolor(IMAGE_WIDTH, IMAGE_HEIGHT, seed)
    elif "oil" in style:
        img = _procedural_oil_painting(IMAGE_WIDTH, IMAGE_HEIGHT, seed)
    else:
        img = _procedural_atmospheric_landscape(IMAGE_WIDTH, IMAGE_HEIGHT, seed)

    img.save(output_path)
    print(f"  [ImageGen] ✓ Procedural artistic frame saved: {output_path.name}")
    return output_path


def _procedural_chinese_ink(width: int, height: int, seed: int) -> Image.Image:
    """Procedural Chinese ink wash painting with rice paper tones, misty mountain ridges, and birds."""
    random.seed(seed)
    base_color = (242, 239, 231)
    img = Image.new("RGB", (width, height), base_color)
    draw = ImageDraw.Draw(img)

    for y in range(height):
        t = y / height
        r = int(242 - t * 45)
        g = int(239 - t * 45)
        b = int(231 - t * 42)
        draw.line([(0, y), (width, y)], fill=(r, g, b))

    layers = [
        {"y_base": int(height * 0.46), "color": (165, 170, 172), "blur": 4, "amp": 45, "freq": 0.005},
        {"y_base": int(height * 0.58), "color": (115, 122, 125), "blur": 2, "amp": 55, "freq": 0.008},
        {"y_base": int(height * 0.72), "color": (55, 60, 64),    "blur": 1, "amp": 65, "freq": 0.012},
        {"y_base": int(height * 0.88), "color": (28, 30, 32),    "blur": 0, "amp": 45, "freq": 0.016},
    ]

    for layer in layers:
        layer_img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        ldraw = ImageDraw.Draw(layer_img)
        points = [(0, height)]
        y_base = layer["y_base"]
        amp = layer["amp"]
        freq = layer["freq"]
        phase = random.uniform(0, 10)
        for x in range(0, width + 5, 4):
            wave = (
                math.sin(x * freq + phase) * amp +
                math.sin(x * freq * 2.3 + phase * 1.5) * (amp * 0.4) +
                math.sin(x * freq * 5.1) * (amp * 0.15)
            )
            y = min(height, max(0, int(y_base + wave)))
            points.append((x, y))
        points.append((width, height))
        c = layer["color"]
        ldraw.polygon(points, fill=(c[0], c[1], c[2], 230))
        if layer["blur"] > 0:
            layer_img = layer_img.filter(ImageFilter.GaussianBlur(layer["blur"]))
        img.paste(layer_img, (0, 0), layer_img)

    draw = ImageDraw.Draw(img)
    bx_base = int(width * random.uniform(0.55, 0.75))
    by_base = int(height * random.uniform(0.18, 0.28))
    for i in range(5):
        bx = bx_base + i * 22 + random.randint(-4, 4)
        by = by_base + int(math.sin(i) * 12) + random.randint(-3, 3)
        bird_points = [
            (bx - 8, by + 3),
            (bx - 4, by - 2),
            (bx, by),
            (bx + 4, by - 2),
            (bx + 8, by + 3)
        ]
        draw.line(bird_points[:3], fill=(45, 48, 50), width=2)
        draw.line(bird_points[2:], fill=(45, 48, 50), width=2)

    seal_x = width - 60
    seal_y = height - 68
    draw.rectangle([seal_x, seal_y, seal_x + 28, seal_y + 28], outline=(170, 45, 40), width=2)
    draw.rectangle([seal_x + 3, seal_y + 3, seal_x + 25, seal_y + 25], fill=(170, 45, 40))
    draw.line([(seal_x + 7, seal_y + 14), (seal_x + 21, seal_y + 14)], fill=(245, 235, 225), width=2)
    draw.line([(seal_x + 14, seal_y + 7), (seal_x + 14, seal_y + 21)], fill=(245, 235, 225), width=2)
    return img


def _procedural_watercolor(width: int, height: int, seed: int) -> Image.Image:
    """Procedural soft watercolor wash with delicate blooming pigments."""
    random.seed(seed)
    palettes = [
        ((250, 235, 235), (220, 230, 245), (195, 220, 225)),
        ((245, 240, 225), (230, 240, 230), (200, 225, 220)),
        ((235, 230, 250), (220, 235, 245), (250, 230, 220)),
    ]
    p = palettes[seed % len(palettes)]
    img = Image.new("RGB", (width, height), p[0])
    draw = ImageDraw.Draw(img)
    for y in range(height):
        t = y / height
        r = int(p[0][0] * (1 - t) + p[1][0] * t)
        g = int(p[0][1] * (1 - t) + p[1][1] * t)
        b = int(p[0][2] * (1 - t) + p[1][2] * t)
        draw.line([(0, y), (width, y)], fill=(r, g, b))

    bloom_layer = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    bdraw = ImageDraw.Draw(bloom_layer)
    for _ in range(8):
        cx = random.randint(0, width)
        cy = random.randint(int(height * 0.3), height)
        rx = random.randint(int(width * 0.15), int(width * 0.35))
        ry = random.randint(int(height * 0.1), int(height * 0.25))
        color = p[2]
        bdraw.ellipse([cx - rx, cy - ry, cx + rx, cy + ry], fill=(color[0], color[1], color[2], 65))
    bloom_layer = bloom_layer.filter(ImageFilter.GaussianBlur(25))
    img.paste(bloom_layer, (0, 0), bloom_layer)
    return img


def _procedural_oil_painting(width: int, height: int, seed: int) -> Image.Image:
    """Procedural oil painting with rich twilight sky and layered hills."""
    random.seed(seed)
    palettes = [
        ((25, 35, 70), (180, 80, 50), (245, 180, 80)),
        ((40, 20, 55), (140, 60, 95), (230, 160, 120)),
    ]
    p = palettes[seed % len(palettes)]
    img = Image.new("RGB", (width, height))
    draw = ImageDraw.Draw(img)
    for y in range(height):
        t = y / height
        if t < 0.6:
            st = t / 0.6
            r = int(p[0][0] * (1 - st) + p[1][0] * st)
            g = int(p[0][1] * (1 - st) + p[1][1] * st)
            b = int(p[0][2] * (1 - st) + p[1][2] * st)
        else:
            st = (t - 0.6) / 0.4
            r = int(p[1][0] * (1 - st) + p[2][0] * st)
            g = int(p[1][1] * (1 - st) + p[2][1] * st)
            b = int(p[1][2] * (1 - st) + p[2][2] * st)
        draw.line([(0, y), (width, y)], fill=(r, g, b))

    hill_layer = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    hdraw = ImageDraw.Draw(hill_layer)
    points = [(0, height)]
    for x in range(0, width + 5, 5):
        y = int(height * 0.68 + math.sin(x * 0.007) * 40 + math.cos(x * 0.015) * 20)
        points.append((x, y))
    points.append((width, height))
    hdraw.polygon(points, fill=(20, 22, 28, 235))
    hill_layer = hill_layer.filter(ImageFilter.GaussianBlur(1))
    img.paste(hill_layer, (0, 0), hill_layer)
    return img


def _procedural_atmospheric_landscape(width: int, height: int, seed: int) -> Image.Image:
    """Procedural atmospheric gradient canvas with ambient lighting."""
    random.seed(seed)
    img = Image.new("RGB", (width, height))
    draw = ImageDraw.Draw(img)
    top_c = (20, 28, 48)
    mid_c = (65, 80, 115)
    bot_c = (140, 155, 185)
    for y in range(height):
        t = y / height
        if t < 0.5:
            st = t * 2
            r = int(top_c[0] * (1 - st) + mid_c[0] * st)
            g = int(top_c[1] * (1 - st) + mid_c[1] * st)
            b = int(top_c[2] * (1 - st) + mid_c[2] * st)
        else:
            st = (t - 0.5) * 2
            r = int(mid_c[0] * (1 - st) + bot_c[0] * st)
            g = int(mid_c[1] * (1 - st) + bot_c[1] * st)
            b = int(mid_c[2] * (1 - st) + bot_c[2] * st)
        draw.line([(0, y), (width, y)], fill=(r, g, b))
    return img
