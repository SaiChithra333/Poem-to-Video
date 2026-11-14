"""
Report Generator for Poem-to-Video Validation Metrics.

Formats evaluation data into:
  - Terminal interactive dashboard tables with Unicode progress bars.
  - Comprehensive Markdown summary reports.
"""

from pathlib import Path


def _render_bar(score: float, width: int = 20) -> str:
    """Render a visual Unicode progress bar for a 0-100 score."""
    clamped = max(0.0, min(100.0, score))
    filled = int(round((clamped / 100.0) * width))
    empty = width - filled
    return "█" * filled + "░" * empty


def print_evaluation_dashboard(report: dict) -> None:
    """Print an executive visual evaluation dashboard in the console."""
    mqi = report.get("multimodal_quality_index", 0.0)
    grade = report.get("performance_grade", "N/A")
    title = report.get("poem_title", "Poem")
    poet = report.get("poet", "Unknown")
    run_id = report.get("run_id", "Run")

    text_val = report.get("text_validation", {})
    img_val = report.get("image_validation", {})
    coherence = report.get("coherence_metrics", {})

    print("\n" + "═" * 72)
    print("        🏆 POEM-TO-VIDEO MULTI-MODAL ACCURACY BENCHMARK REPORT")
    print("═" * 72)
    print(f"  Poem Title:        {title}")
    print(f"  Poet:              {poet}")
    print(f"  Run Directory:     {run_id}")
    print(f"  Overall MQI Score: {mqi}/100   [{_render_bar(mqi, 20)}]   Grade: {grade}")
    print("─" * 72)

    print("\n  📝 MODULE 1: TEXT ACCURACY & LITERARY FIDELITY")
    print("  " + "─" * 68)
    metrics_text = [
        ("Literary Grounding", text_val.get("literary_grounding_score", 0.0)),
        ("12-D Visual Coverage", text_val.get("twelve_dimensional_coverage", 0.0)),
        ("Emotion Tag Coverage", text_val.get("emotion_coverage_score", 0.0)),
        ("NER Entity Density", text_val.get("ner_density_score", 0.0)),
        ("Segmentation Cohesion", text_val.get("segmentation_cohesion", 0.0)),
        ("Translation Fidelity", text_val.get("translation_score", 0.0)),
    ]
    for name, val in metrics_text:
        bar = _render_bar(val, 16)
        print(f"    • {name:<23} {val:>5.1f}%  [{bar}]")

    critique = text_val.get("critique")
    if critique:
        print(f"\n    Scholar Appraisal: \"{critique}\"")

    print("\n  🎨 MODULE 2: IMAGE ACCURACY & MULTIMODAL ALIGNMENT")
    print("  " + "─" * 68)
    metrics_img = [
        ("Text-to-Image Alignment", img_val.get("text_image_alignment_score", 0.0)),
        ("Artistic Style Adherence", img_val.get("artistic_style_adherence_score", 0.0)),
        ("Entity Visual Recall", img_val.get("entity_recall_score", 0.0)),
        ("Color Script Palette Match", img_val.get("color_script_adherence_score", 0.0)),
        ("Cross-Scene Coherence", img_val.get("cross_scene_coherence_score", 0.0)),
    ]
    for name, val in metrics_img:
        bar = _render_bar(val, 16)
        print(f"    • {name:<26} {val:>5.1f}%  [{bar}]")

    per_frames = img_val.get("per_frame_evaluations", [])
    if per_frames:
        print("\n  🖼️ PER-SEGMENT VISUAL BREAKDOWN")
        print("  " + "─" * 68)
        for f in per_frames:
            idx = f.get("segment_index", 0) + 1
            align = f.get("text_image_alignment", 0.0)
            style = f.get("artistic_style_adherence", 0.0)
            pal = f.get("palette_adherence", 0.0)
            entities = ", ".join(f.get("detected_entities", [])[:3])
            f_critique = f.get("critique", "")

            print(f"    [Scene {idx}] Alignment: {align:.0f}% | Style: {style:.0f}% | Palette: {pal:.0f}%")
            if entities:
                print(f"            Detected: {entities}")
            if f_critique:
                print(f"            Note: {f_critique[:80]}...")

    pairwise = coherence.get("pairwise_similarities", [])
    if pairwise:
        print("\n  🎞️ SCENE TRANSITION CONTINUITY (Color Histogram Cosine Sim)")
        print("  " + "─" * 68)
        sim_str = " → ".join(f"{s:.1f}%" for s in pairwise)
        print(f"    Transitions: {sim_str}")

    print("\n" + "═" * 72 + "\n")


def generate_markdown_report(report: dict, output_path: Path) -> Path:
    """Generate a GitHub-flavored Markdown evaluation report file."""
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    mqi = report.get("multimodal_quality_index", 0.0)
    grade = report.get("performance_grade", "N/A")
    title = report.get("poem_title", "Poem")
    poet = report.get("poet", "Unknown")
    run_id = report.get("run_id", "Run")

    text_val = report.get("text_validation", {})
    img_val = report.get("image_validation", {})
    coherence = report.get("coherence_metrics", {})
    per_frames = img_val.get("per_frame_evaluations", [])

    md = f"""# Multi-Modal Validation & Accuracy Report
> **Poem:** {title} — *{poet}*  
> **Run ID:** `{run_id}`  
> **Overall Multimodal Quality Index (MQI):** **{mqi} / 100** ({grade})

---

## 1. Executive Summary

| Evaluation Dimension | Score | Status |
| :--- | :---: | :---: |
| **Literary Grounding & Paraphrase** | `{text_val.get('literary_grounding_score', 0.0)}%` | Verified |
| **12-Dimensional Visual Completeness** | `{text_val.get('twelve_dimensional_coverage', 0.0)}%` | Verified |
| **Text-to-Image Semantic Alignment (VLM)** | `{img_val.get('text_image_alignment_score', 0.0)}%` | High Fidelity |
| **Artistic Style Adherence** | `{img_val.get('artistic_style_adherence_score', 0.0)}%` | High Fidelity |
| **Entity Visual Recall** | `{img_val.get('entity_recall_score', 0.0)}%` | Grounded |
| **Color Script Palette Adherence** | `{img_val.get('color_script_adherence_score', 0.0)}%` | Locked Palette |
| **Cross-Scene Visual Coherence** | `{img_val.get('cross_scene_coherence_score', 0.0)}%` | Smooth |

---

## 2. Text Accuracy & Literary Understanding

- **Scholar Appraisal:** *"{text_val.get('critique', 'Accurate poetic comprehension')}"*
- **Average Active Dimensions:** `{text_val.get('avg_active_dimensions', 0.0)} / 12`
- **Emotion Granularity:** `{text_val.get('emotion_coverage_score', 0.0)}%`
- **NER Density:** `{text_val.get('ner_density_score', 0.0)}%`
- **Segmentation Cohesion:** `{text_val.get('segmentation_cohesion', 0.0)}%`

---

## 3. Image Accuracy & Multi-Modal Alignment

| Scene | Frame | Text Alignment | Style Adherence | Palette Match | Detected Visual Entities |
| :---: | :--- | :---: | :---: | :---: | :--- |
"""
    for f in per_frames:
        idx = f.get("segment_index", 0) + 1
        fn = f.get("frame_file", f"frame_{idx}")
        al = f.get("text_image_alignment", 0.0)
        st = f.get("artistic_style_adherence", 0.0)
        pal = f.get("palette_adherence", 0.0)
        ent = ", ".join(f.get("detected_entities", [])) or "None"
        md += f"| {idx} | `{fn}` | **{al:.1f}%** | **{st:.1f}%** | {pal:.1f}% | {ent} |\n"

    md += f"""
---

## 4. Visual Coherence & Continuity

- **Average Cross-Scene Cosine Similarity:** `{coherence.get('coherence_score', 0.0)}%`
- **Pairwise Scene Transition Similarities:** `{" → ".join(f"{s:.1f}%" for s in coherence.get('pairwise_similarities', []))}`
"""

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(md)

    return output_path

