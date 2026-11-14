"""
Ambient Soundscape Generator — Module 3, Enhancement 6

Generates subtle, atmospheric acoustic background beds tailored to the poem's
artistic style and emotional atmosphere:
  - 'chinese_ink': Ancient pentatonic singing bowl / guqin resonance with gentle wind.
  - 'watercolor': Luminous airy acoustic harp & flute harmonic bed.
  - 'oil_painting': Rich warm cello & atmospheric strings drone.
"""

import wave
from pathlib import Path
import numpy as np


def generate_ambient_soundscape(
    duration: float,
    output_path: Path,
    style: str = "chinese_ink",
    language: str = "auto",
    sample_rate: int = 44100,
    volume: float = 0.12
) -> Path:
    """
    Synthesize a continuous ambient acoustic texture for background mixing.

    Args:
        duration: Total audio length in seconds.
        output_path: Path to save the resulting WAV file.
        style: Target artistic style ('chinese_ink', 'watercolor', 'oil_painting', 'anime').
        language: Language of poem ('chinese', 'japanese', 'hindi', 'french', 'spanish', etc.).
        sample_rate: Audio sampling rate (default 44.1kHz).
        volume: Mixing volume scaling (0.0 to 1.0, default 0.12 for subtle bed).

    Returns:
        Path to the generated WAV audio file.
    """
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    signal = np.zeros_like(t)

    style_lower = str(style).lower() if style else ""
    lang_lower = str(language).lower() if language else ""

    # 1. Japanese Zen / Haiku (Hirajoshi / In-sen scale: D4, Eb4, G4, A4, Bb4)
    if "japanese" in lang_lower or "ja" in lang_lower or "anime" in style_lower:
        pitches = [293.66, 311.13, 392.00, 440.00, 466.16]
        for idx, f in enumerate(pitches):
            harmonic = (
                np.sin(2 * np.pi * f * t) * 0.45 +
                np.sin(2 * np.pi * f * 2 * t) * 0.20 +
                np.sin(2 * np.pi * f * 3 * t) * 0.08
            )
            cycle_rate = 0.06 + idx * 0.02
            mod = 0.35 + 0.65 * np.sin(2 * np.pi * cycle_rate * t + idx * 1.5)
            signal += harmonic * mod

    # 2. Indian / Hindi Meditative Tanpura (Sa-Pa: C3, G3, C4, E4)
    elif "hindi" in lang_lower or "hi" in lang_lower or "indian" in lang_lower:
        pitches = [130.81, 196.00, 261.63, 329.63]
        for idx, f in enumerate(pitches):
            harmonic = (
                np.sin(2 * np.pi * f * t) * 0.50 +
                np.sin(2 * np.pi * f * 2 * t) * 0.25 +
                np.sin(2 * np.pi * f * 3 * t) * 0.15 +
                np.sin(2 * np.pi * f * 4 * t) * 0.05
            )
            cycle_rate = 0.05 + idx * 0.015
            mod = 0.4 + 0.6 * np.sin(2 * np.pi * cycle_rate * t + idx * 0.8)
            signal += harmonic * mod

    # 3. Chinese Classical Ink Wash (Pentatonic: Gong, Shang, Jiao, Zhi, Yu)
    elif "ink" in style_lower or "chinese" in style_lower or "zh" in lang_lower:
        pitches = [261.63, 293.66, 329.63, 392.00, 440.00]
        for idx, f in enumerate(pitches):
            harmonic = (
                np.sin(2 * np.pi * f * t) * 0.40 +
                np.sin(2 * np.pi * f * 2 * t) * 0.15 +
                np.sin(2 * np.pi * f * 3 * t) * 0.05
            )
            cycle_rate = 0.08 + idx * 0.02
            mod = 0.4 + 0.6 * np.sin(2 * np.pi * cycle_rate * t + idx * 1.2)
            signal += harmonic * mod

    # 4. Luminous Watercolor (Major-seventh / Harp & Flute texture)
    elif "watercolor" in style_lower:
        pitches = [174.61, 220.00, 261.63, 329.63, 392.00]
        for idx, f in enumerate(pitches):
            harmonic = (
                np.sin(2 * np.pi * f * t) * 0.50 +
                np.sin(2 * np.pi * f * 2 * t) * 0.20 +
                np.sin(2 * np.pi * f * 4 * t) * 0.08
            )
            mod = 0.5 + 0.5 * np.sin(2 * np.pi * (0.1 + idx * 0.03) * t + idx * 0.9)
            signal += harmonic * mod

    # 5. Oil Painting / Romantic Strings & Cello drone (A2, E3, A3, C#4)
    else:
        pitches = [110.00, 164.81, 220.00, 277.18]
        for idx, f in enumerate(pitches):
            harmonic = (
                np.sin(2 * np.pi * f * t) * 0.45 +
                np.sin(2 * np.pi * f * 2 * t) * 0.25 +
                np.sin(2 * np.pi * f * 3 * t) * 0.10
            )
            mod = 0.5 + 0.5 * np.sin(2 * np.pi * (0.07 + idx * 0.02) * t)
            signal += harmonic * mod

    # Soft breeze / pink noise shimmer
    noise = np.random.normal(0, 0.04, len(t))
    # Smooth noise
    kernel_size = 500
    kernel = np.ones(kernel_size) / kernel_size
    smoothed_noise = np.convolve(noise, kernel, mode="same")
    signal += smoothed_noise

    # Fade-in and fade-out envelope to avoid clicks
    fade_len = int(sample_rate * min(2.0, duration * 0.2))
    if fade_len > 0:
        envelope = np.ones_like(signal)
        envelope[:fade_len] = np.linspace(0, 1, fade_len)
        envelope[-fade_len:] = np.linspace(1, 0, fade_len)
        signal *= envelope

    # Normalize and scale to target background volume
    max_val = np.max(np.abs(signal))
    if max_val > 1e-5:
        signal = signal / max_val * volume

    int_data = (np.clip(signal, -1.0, 1.0) * 32767).astype(np.int16)

    with wave.open(str(output_path), "w") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        wf.writeframes(int_data.tobytes())

    return output_path
