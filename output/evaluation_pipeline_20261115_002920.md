# Multi-Modal Validation & Accuracy Report
> **Poem:** Agnipath (The Path of Fire) — *Harivansh Rai Bachchan*  
> **Run ID:** `pipeline_20261115_002920`  
> **Overall Multimodal Quality Index (MQI):** **89.6 / 100** (A (High Fidelity))

---

## 1. Executive Summary

| Evaluation Dimension | Score | Status |
| :--- | :---: | :---: |
| **Literary Grounding & Paraphrase** | `100.0%` | Verified |
| **12-Dimensional Visual Completeness** | `100.0%` | Verified |
| **Text-to-Image Semantic Alignment (VLM)** | `86.0%` | High Fidelity |
| **Artistic Style Adherence** | `87.2%` | High Fidelity |
| **Entity Visual Recall** | `81.0%` | Grounded |
| **Color Script Palette Adherence** | `81.9%` | Locked Palette |
| **Cross-Scene Visual Coherence** | `82.5%` | Smooth |

---

## 2. Text Accuracy & Literary Understanding

- **Scholar Appraisal:** *"Structured heuristic evaluation"*
- **Average Active Dimensions:** `11.0 / 12`
- **Emotion Granularity:** `100.0%`
- **NER Density:** `56.0%`
- **Segmentation Cohesion:** `90.0%`

---

## 3. Image Accuracy & Multi-Modal Alignment

| Scene | Frame | Text Alignment | Style Adherence | Palette Match | Detected Visual Entities |
| :---: | :--- | :---: | :---: | :---: | :--- |
| 1 | `frame_seg_000.png` | **92.0%** | **88.0%** | 85.1% | massive ancient ironwood tree, foreground tree trunks, forest canopy, glowing opening, misty ground |
| 2 | `frame_seg_001.png` | **92.0%** | **90.0%** | 82.6% | trees, volcanic cliffs, stone plateau, sky, ground |
| 3 | `frame_seg_002.png` | **82.0%** | **85.0%** | 80.0% | trees, ironwood trees, barren landscape, sky, sun |
| 4 | `frame_seg_003.png` | **82.0%** | **85.0%** | 81.8% | human silhouette, trees, fog, forest |
| 5 | `frame_seg_004.png` | **82.0%** | **88.0%** | 80.2% | obsidian rock, volcanic landscape, ground, smoke |

---

## 4. Visual Coherence & Continuity

- **Average Cross-Scene Cosine Similarity:** `82.5%`
- **Pairwise Scene Transition Similarities:** `86.6% → 79.4% → 81.4% → 82.5%`
