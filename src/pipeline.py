"""
Pipeline Orchestrator (Enhanced Architecture)

End-to-end orchestrator that chains all three enhanced modules:
  Module 1: Textual Situational Comprehension
            (Extended Paraphrase → Semantic Segmentation → 12-D Keyword Extraction → Prompt Refinement)
  Module 2: Situational Image Creation
            (Parallel Image Generation → Ken Burns Animation → Smooth Cross-Fade Transitions)
  Module 3: Situational Video Synthesis
            (Multilingual Translation → Multi-TTS Narration → Stacked Subtitles → Final Assembly)

Reference: IEEE TLT 2024 paper and Progress.docx.
"""

import json
import sys
from pathlib import Path
from datetime import datetime

# Ensure UTF-8 console output on Windows
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

from src.config import (
    OUTPUT_DIR, TEMP_DIR, DEFAULT_STYLE,
    TARGET_LANGUAGES, PROMPT_REFINE, PARALLEL_IMAGE_GEN,
    ENABLE_SEMANTIC_SEGMENTATION, TRANSITION_DURATION,
    IMAGE_WIDTH, IMAGE_HEIGHT
)

# Module 1: Comprehension & Segmentation
from src.comprehension.paraphrase import paraphrase_poem
from src.comprehension.semantic_segmentor import segment_poem
from src.comprehension.visual_blueprint import generate_visual_blueprint
from src.comprehension.key_element_extraction import extract_key_elements
from src.comprehension.prompt_generator import generate_prompts, format_prompt_for_display

# Module 2: Image Creation & Animation
from src.image_creation.parallel_generator import generate_all_frames_parallel
from src.image_creation.rife_interpolation import (
    generate_line_frames,
    generate_transition_frames,
)

# Module 3: Video Synthesis, Translation & Audio
from src.video_synthesis.translator import translate_segments
from src.video_synthesis.tts_engine import synthesize_poem
from src.video_synthesis.multi_tts_engine import synthesize_multilingual_audio
from src.video_synthesis.ambient_soundscapes import generate_ambient_soundscape
from src.video_synthesis.video_assembler import (
    assemble_segment_clip,
    assemble_full_video,
    _sanitize_filename
)


def run_pipeline(
    poem_text: str,
    language: str = "auto",
    style: str = None,
    image_provider: str = None,
    frames_per_line: int = 24,
    target_languages: list[str] = None,
    enable_segmentation: bool = None,
    enable_refinement: bool = None,
    parallel_images: bool = None,
    render_all_languages: bool = False,
    output_name: str = None,
    title_override: str = None,
    poet_override: str = None,
    verbose: bool = True,
) -> Path:
    """
    Run the complete enhanced poem-to-video pipeline.
    """
    style = style or DEFAULT_STYLE
    target_langs = target_languages if target_languages is not None else TARGET_LANGUAGES
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    work_dir = TEMP_DIR / f"pipeline_{timestamp}"
    work_dir.mkdir(parents=True, exist_ok=True)

    print("=" * 65)
    print("  POEM-TO-VIDEO GENERATION SYSTEM (ENHANCED ARCHITECTURE)")
    print("=" * 65)
    print(f"  Art Style:          {style}")
    print(f"  Language:           {language}")
    print(f"  Target Subtitles:   {target_langs}")
    print(f"  Work Directory:     {work_dir}")
    print("=" * 65)

    # ─────────────────────────────────────────────────────────────
    # MODULE 1: Textual Situational Comprehension
    # ─────────────────────────────────────────────────────────────
    print("\n▶ MODULE 1: Textual Situational Comprehension")
    print("-" * 55)

    # Check for pre-computed sample cache if LLM_PROVIDER is not set
    from src.llm_client import LLM_PROVIDER
    from src.comprehension.sample_cache import find_sample_key, get_cached_sample

    cached_data = None
    if not LLM_PROVIDER:
        sample_key = find_sample_key(title_override) or find_sample_key(poem_text)
        if sample_key:
            cached_data = get_cached_sample(sample_key)
            if cached_data:
                print(f"  [Offline Demo Mode] Loaded pre-computed literary analysis for '{sample_key}'")

    # Step 1.1: Extended Paraphrase (with Emotion & NER tags)
    print("\n  Step 1.1: Literary Paraphrase & Emotion/NER Tagging...")
    if cached_data and "paraphrase" in cached_data:
        paraphrase_data = cached_data["paraphrase"]
        print("  → Using pre-computed literary analysis from sample cache")
    else:
        paraphrase_data = paraphrase_poem(poem_text, language)

    with open(work_dir / "01_paraphrase.json", "w", encoding="utf-8") as f:
        json.dump(paraphrase_data, f, indent=2, ensure_ascii=False)

    title = title_override or paraphrase_data.get("title", "Untitled")
    if (not title or title == "Untitled") and title_override:
        title = title_override
    poet = poet_override or paraphrase_data.get("poet", "Unknown")
    if (not poet or poet == "Unknown") and poet_override:
        poet = poet_override
    lines_data = paraphrase_data.get("lines", [])

    print(f"  → Poem Title: {title}")
    print(f"  → Poet:       {poet}")
    print(f"  → Lines:      {len(lines_data)}")

    # Step 1.1b: Emotion + NER Semantic Segmentation
    print("\n  Step 1.1b: Semantic Segmentation (Emotion + Entity grouping)...")
    segments = segment_poem(paraphrase_data, enable_segmentation=enable_segmentation)

    with open(work_dir / "01b_segments.json", "w", encoding="utf-8") as f:
        json.dump([s.to_dict() for s in segments], f, indent=2, ensure_ascii=False)

    # Step 1.1c: Global Visual Blueprint & Color Script (Coherence Architecture)
    print("\n  Step 1.1c: Global Visual Blueprint & Color Script...")
    if cached_data and "blueprint" in cached_data:
        visual_blueprint = cached_data["blueprint"]
        print("  → Using pre-computed visual blueprint from sample cache")
    else:
        visual_blueprint = generate_visual_blueprint(paraphrase_data, segments, style=style)

    with open(work_dir / "01c_visual_blueprint.json", "w", encoding="utf-8") as f:
        json.dump(visual_blueprint.to_dict(), f, indent=2, ensure_ascii=False)

    # Step 1.2: 12-Dimensional Visual Keyword Extraction
    print(f"\n  Step 1.2: 12-Dimensional Keyword Extraction for {len(segments)} segments...")
    if cached_data and "key_elements" in cached_data and len(cached_data["key_elements"]) == len(segments):
        key_elements = cached_data["key_elements"]
        print("  → Using pre-computed 12-dimensional keywords from sample cache")
    else:
        key_elements = extract_key_elements(segments, style, visual_blueprint=visual_blueprint)

    with open(work_dir / "02_key_elements.json", "w", encoding="utf-8") as f:
        json.dump(key_elements, f, indent=2, ensure_ascii=False)

    # Step 1.3: Prompt Generation & Iterative Refinement
    print("\n  Step 1.3: Prompt Generation & LLM Self-Critique Refinement...")
    refine_flag = False if cached_data else enable_refinement
    prompts = generate_prompts(key_elements, style, enable_refinement=refine_flag, visual_blueprint=visual_blueprint)

    with open(work_dir / "03_prompts.json", "w", encoding="utf-8") as f:
        json.dump(prompts, f, indent=2, ensure_ascii=False)

    if verbose:
        print("\n  Refined Prompts:")
        for p in prompts:
            print(format_prompt_for_display(p))
            print()

    # ─────────────────────────────────────────────────────────────
    # MODULE 2: Situational Image Creation & Animation
    # ─────────────────────────────────────────────────────────────
    print("\n▶ MODULE 2: Situational Image Creation")
    print("-" * 55)

    # Step 2.1: Parallel Image Generation
    provider_name = image_provider or "pollinations"
    workers = 1 if provider_name == "pollinations" else 4
    print(f"\n  Step 2.1: Generating {len(prompts)} key frames (provider={provider_name}, workers={workers})...")
    key_frames_dir = work_dir / "key_frames"
    key_frames = generate_all_frames_parallel(
        prompts=prompts,
        output_dir=key_frames_dir,
        provider=provider_name,
        max_workers=workers
    )

    # Step 2.2: Ken Burns Camera Animation per segment (Cinematic Shot Dynamics)
    print("\n  Step 2.2: Generating Ken Burns animation sequences with alternating cinematic motions...")
    all_segment_frames = []
    for i, key_frame in enumerate(key_frames):
        seg_frames_dir = work_dir / "segment_frames" / f"seg_{i:03d}"
        shot_motion = prompts[i].get("camera_motion", "auto") if i < len(prompts) else "auto"
        frames = generate_line_frames(
            key_frame,
            num_frames=frames_per_line,
            output_dir=seg_frames_dir,
            motion_type=shot_motion,
            segment_idx=i
        )
        all_segment_frames.append(frames)

    # Step 2.3: Ease-in-Out Cross-Fade Transitions between segments
    print("\n  Step 2.3: Generating transition frames between visual scenes...")
    transition_frame_lists = []
    for i in range(len(key_frames) - 1):
        trans_dir = work_dir / "transitions" / f"trans_{i:03d}"
        trans_frames = generate_transition_frames(
            key_frames[i], key_frames[i + 1],
            output_dir=trans_dir
        )
        transition_frame_lists.append(trans_frames)

    # ─────────────────────────────────────────────────────────────
    # MODULE 3: Situational Video Synthesis & Multilingual Subtitles
    # ─────────────────────────────────────────────────────────────
    print("\n▶ MODULE 3: Situational Video Synthesis")
    print("-" * 55)

    segment_primary_texts = [s.merged_text for s in segments]

    # Step 3.1a: Multi-Language Translation for Subtitles
    translations = {}
    if target_langs:
        print("\n  Step 3.1a: Translating segment texts for multi-language subtitles...")
        if cached_data and "translations" in cached_data:
            for l_code in target_langs:
                if l_code in cached_data["translations"]:
                    translations[l_code] = cached_data["translations"][l_code]
        if not translations:
            translations = translate_segments(segment_primary_texts, target_langs)

        with open(work_dir / "03_translations.json", "w", encoding="utf-8") as f:
            json.dump(translations, f, indent=2, ensure_ascii=False)

    # Step 3.1b: TTS Speech Synthesis
    print("\n  Step 3.1b: Synthesizing narration audio...")
    tts_dir = work_dir / "tts"
    # Primary narration audio matching original language
    primary_audio_paths = synthesize_poem(segment_primary_texts, tts_dir, language=language)

    # Step 3.2: Assemble individual segment clips
    print("\n  Step 3.2: Assembling visual clips with stacked subtitles & narration...")
    segment_clips = []
    for i, seg in enumerate(segments):
        frames = all_segment_frames[i] if i < len(all_segment_frames) else [key_frames[i]]
        audio = primary_audio_paths[i] if i < len(primary_audio_paths) else None
        primary_txt = seg.merged_text

        # Collect translations for this segment
        seg_translations = []
        for l_code, l_texts in translations.items():
            if i < len(l_texts) and l_texts[i] != primary_txt:
                seg_translations.append(l_texts[i])

        clip = assemble_segment_clip(
            frame_paths=frames,
            audio_path=audio,
            primary_text=primary_txt,
            translated_texts=seg_translations
        )
        segment_clips.append(clip)
        print(f"  [Assembly] ✓ Segment {i+1} clip ready: {clip.duration:.1f}s")

    # Step 3.3: Assemble transition clips
    print("\n  Step 3.3: Assembling transition clips...")
    transition_clips = []
    for i, trans_frames in enumerate(transition_frame_lists):
        from moviepy import ImageClip, concatenate_videoclips
        frame_dur = TRANSITION_DURATION / max(len(trans_frames), 1)
        trans_clip_list = [ImageClip(str(fp)).with_duration(frame_dur) for fp in trans_frames]
        trans_clip = concatenate_videoclips(trans_clip_list, method="compose")
        trans_clip = trans_clip.resized((IMAGE_WIDTH, IMAGE_HEIGHT))
        transition_clips.append(trans_clip)

    # Step 3.3b: Synthesize ambient acoustic soundscape
    total_est_dur = max(sum(c.duration for c in segment_clips) * 1.5, 45.0) + len(transition_clips) * TRANSITION_DURATION + 10.0
    bgm_path = work_dir / "ambient_bgm.wav"
    try:
        generate_ambient_soundscape(
            duration=total_est_dur,
            output_path=bgm_path,
            style=style,
            language=language
        )
        print(f"  [Soundscape] ✓ Synthesized ambient acoustic soundscape ({style}, {language})")
    except Exception as e:
        print(f"  [Soundscape] ⚠ Could not generate soundscape ({e})")
        bgm_path = None

    # Step 3.4: Final Assembly & Render
    print("\n  Step 3.4: Rendering final situational video...")
    output_filename = output_name or f"{_sanitize_filename(title)}_{timestamp}"
    output_path = OUTPUT_DIR / f"{output_filename}.mp4"

    final_path = assemble_full_video(
        segment_clips=segment_clips,
        transition_clips=transition_clips,
        title=title,
        poet=poet,
        output_path=output_path,
        bgm_path=bgm_path,
    )

    # Mode B: Render localized video per language if requested
    if render_all_languages and len(target_langs) > 1:
        print("\n  [Mode B] Rendering localized video variants for each target language...")
        # Prepare multilingual audio dict
        segments_by_lang = {}
        for l_code in target_langs:
            if l_code in translations:
                segments_by_lang[l_code] = translations[l_code]
            else:
                segments_by_lang[l_code] = segment_primary_texts

        multi_audio = synthesize_multilingual_audio(segments_by_lang, work_dir / "multi_tts")

        for l_code in target_langs:
            lang_audio_list = multi_audio.get(l_code, [])
            lang_clips = []
            for i, seg in enumerate(segments):
                frames = all_segment_frames[i] if i < len(all_segment_frames) else [key_frames[i]]
                audio = lang_audio_list[i] if i < len(lang_audio_list) else None
                primary_txt = segments_by_lang[l_code][i] if i < len(segments_by_lang[l_code]) else seg.merged_text

                # Stack original text if different
                trans_stack = [seg.merged_text] if seg.merged_text != primary_txt else []

                clip = assemble_segment_clip(
                    frame_paths=frames,
                    audio_path=audio,
                    primary_text=primary_txt,
                    translated_texts=trans_stack
                )
                lang_clips.append(clip)

            lang_out_path = OUTPUT_DIR / f"{output_filename}_{l_code}.mp4"
            print(f"  [Mode B] Assembling {l_code.upper()} video: {lang_out_path.name}...")
            assemble_full_video(
                segment_clips=lang_clips,
                transition_clips=transition_clips,
                title=title,
                poet=poet,
                output_path=lang_out_path,
                bgm_path=bgm_path,
            )
            print(f"  [Mode B] ✓ Localized {l_code.upper()} video rendered: {lang_out_path.name}")

    total_duration = sum(c.duration for c in segment_clips) + (len(transition_clips) * TRANSITION_DURATION) + 3.5
    print("\n" + "=" * 65)
    print("  ✓ PIPELINE COMPLETED SUCCESSFULLY!")
    print("=" * 65)
    print(f"  Output Video:     {final_path}")
    print(f"  Poem Title:       {title}")
    print(f"  Poet:             {poet}")
    print(f"  Visual Segments:  {len(segments)} (from {len(lines_data)} lines)")
    print(f"  Subtitles:        Original + {len(translations)} translation tracks")
    print(f"  Estimated Length: {total_duration:.1f}s")
    print("=" * 65)

    return final_path
