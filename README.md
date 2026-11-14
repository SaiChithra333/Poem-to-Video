# Poem-to-Video: Situational Multimedia Video Generation System

> **Automatic Generation of Multimedia Teaching Materials Based on Generative AI**  
> Based on the IEEE TLT 2024 Research Paper (*Chen & Wu*) with the **5 Enhanced Architecture Modules**.

---

## 📖 Overview

The **Poem-to-Video** system automatically transforms classical and modern poetry into cinematic teaching videos. Rather than merely creating literal or static illustrations, the system creates **situational videos** that visually encapsulate the artistic conception (*意境*), emotional connotations, historical setting, and aesthetic style of each poem.

### 🌟 Key Enhancements Implemented
1. **Emotion + NER Semantic Segmentation:** Automatically groups adjacent lines sharing emotion and scene entities into unified visual scenes instead of rigid 1-image-per-line cuts.
2. **Iterative LLM Prompt Refinement:** Uses an LLM prompt self-critique loop to resolve contradictions, add spatial anchors (foreground, midground, background), and polish Stable Diffusion prompts.
3. **Parallel Asynchronous Image Generation:** Dispatches image generation requests concurrently with rate-limiting backoff, dramatically speeding up wall-clock render times.
4. **Stacked Multilingual Subtitles:** Automatically translates poem segments and renders stacked, high-contrast subtitles (Original language on top, translated language below) using native system CJK fonts across Windows, macOS, and Linux (eliminating broken glyphs / `??`).
5. **Multilingual Speech Narration (Mode A & Mode B):** Integrates Microsoft Edge TTS (with automatic Google TTS fallback) for expressive voice recitation, supporting both primary bilingual videos and exporting localized video files per language (e.g. `_en.mp4`, `_zh.mp4`, `_hi.mp4`).
6. **Multi-Modal Validation & Accuracy Metrics Suite (MQI):** An automated evaluation benchmark measuring both textual accuracy (literary grounding, 12-D completeness, translation fidelity) and visual accuracy (text-to-image VLM semantic alignment, entity recall, style adherence, color script palette match, and cross-scene visual coherence).

---

## 📁 Project File Structure

```
Poem-to-Video/
├── main.py                                      # CLI entry point
├── evaluate.py                                  # Multi-modal accuracy validation CLI
├── requirements.txt                             # Python dependencies
├── .env                                         # Environment variables & API keys
├── README.md                                    # Project documentation & run guide
│
├── src/                                         # Source Code
│   ├── config.py                                # Settings, styles, cross-platform font detection, voices
│   ├── llm_client.py                            # Gemini & OpenAI LLM client with fallback
│   ├── pipeline.py                              # Master end-to-end pipeline orchestrator
│   │
│   ├── comprehension/                           # MODULE 1: Textual Situational Comprehension
│   │   ├── paraphrase.py                        # Step 1.1: Literary analysis & Emotion/NER tagging
│   │   ├── semantic_segmentor.py                # Step 1.1b: Emotion + NER dynamic segmentation
│   │   ├── visual_blueprint.py                  # Step 1.1c: Global color script & location consistency
│   │   ├── sample_cache.py                      # Offline pre-computed sample poem cache
│   │   ├── key_element_extraction.py            # Step 1.2: 12-Dimensional visual keyword extraction
│   │   ├── prompt_refiner.py                    # Step 1.3a: LLM prompt self-critique loop
│   │   └── prompt_generator.py                  # Step 1.3b: Positive & negative prompt builder
│   │
│   ├── image_creation/                          # MODULE 2: Situational Image Creation
│   │   ├── single_frame_generator.py            # Step 2.1: Key frame artwork generation
│   │   ├── parallel_generator.py                # Step 2.1b: Concurrent parallel image generation
│   │   └── rife_interpolation.py                # Steps 2.2 & 2.3: Ken Burns animation & cross-fades
│   │
│   ├── video_synthesis/                         # MODULE 3: Situational Video Synthesis
│   │   ├── translator.py                        # Multilingual poetic translation engine
│   │   ├── tts_engine.py                        # Microsoft Edge TTS & gTTS audio narration
│   │   ├── multi_tts_engine.py                  # Parallel multilingual speech synthesis
│   │   ├── ambient_soundscapes.py               # Procedural acoustic soundscapes (Guqin, Tanpura, Harp)
│   │   ├── multi_subtitle_generator.py          # Stacked subtitle overlay with native system fonts
│   │   └── video_assembler.py                   # MoviePy final video composition & MP4 export
│   │
│   └── evaluation/                              # Multi-Modal Validation & Metrics Engine
│       ├── metrics.py                           # Text, image, palette, and VLM evaluation metrics
│       └── report_generator.py                  # Terminal dashboard & Markdown report generator
│
├── output/                                      # Rendered final MP4 videos & evaluation reports
│   ├── Agneepath_TIMESTAMP.mp4
│   ├── The_Old_Pond_TIMESTAMP.mp4
│   └── evaluation_pipeline_TIMESTAMP.md
│
└── temp/                                        # Intermediate pipeline run artifacts
    └── pipeline_YYYYMMDD_HHMMSS/
        ├── 01_paraphrase.json                   # Literary analysis output
        ├── 01b_segments.json                    # Semantic visual segments
        ├── 01c_visual_blueprint.json            # Locked 4-color palette & location anchor
        ├── 02_key_elements.json                 # 12-dimensional extracted keywords
        ├── 03_prompts.json                      # Refined SD prompts & critique rationales
        ├── 03_translations.json                 # Multilingual translation texts
        ├── key_frames/                          # AI artwork key frame PNGs
        ├── segment_frames/                      # Ken Burns animated sequence frames
        ├── transitions/                         # Ease-in-out cross-fade frames
        ├── tts/                                 # Synthesized voice narration MP3 files
        ├── ambient_bgm.wav                      # Synthesized background soundscape
        └── evaluation_report.json               # Full quantitative accuracy audit
```

---

## ⚙️ Environment Setup

### 1. Activate Virtual Environment
```bash
# macOS / Linux
source venv/bin/activate

# Windows (PowerShell)
.\venv\Scripts\Activate.ps1

# Windows (Command Prompt)
.\venv\Scripts\activate.bat
```

### 2. Configure `.env`
Ensure a `.env` file exists in the root folder with your API keys:
```ini
# Google Gemini API Key (for Module 1 LLM comprehension & translation)
GEMINI_API_KEY=your_gemini_api_key_here
LLM_MODEL=gemini-3.5-flash-lite

# Image Generation Backend: pollinations (free, fast), huggingface, or placeholder
IMAGE_PROVIDER=pollinations

# Enhanced Pipeline Flags
PROMPT_REFINE=True
PARALLEL_IMAGE_GEN=True
ENABLE_SEMANTIC_SEGMENTATION=True
TARGET_LANGUAGES=en,zh
```

---

## 🚀 How to Run

### 1. Run Built-In Sample Poems

#### Classical Chinese Tang Poem (*Spring Dawn / 春晓* by Meng Haoran):
```powershell
.\venv\Scripts\python.exe main.py --sample spring_dawn --style chinese_ink --languages zh,en
```
* Generates traditional Chinese ink wash paintings.
* Recites poem using Chinese voice (`zh-CN-YunxiNeural`).
* Displays stacked Chinese (original) and English (translated) subtitles.

#### Romantic English Poem (*I Wandered Lonely as a Cloud* by William Wordsworth):
```powershell
.\venv\Scripts\python.exe main.py --sample daffodils --style watercolor --languages en,zh
```
* Generates watercolor landscape paintings.
* Recites poem using English voice (`en-US-AriaNeural`).
* Displays stacked English (original) and Chinese (translated) subtitles.

---

### 2. Export Localized Videos for Each Language (Mode B)
To automatically generate separate localized video files for each target language (e.g., one English video and one Chinese video with native audio):
```powershell
.\venv\Scripts\python.exe main.py --sample daffodils --style watercolor --languages en,zh --all-languages
```
This produces:
* `output/I_wandered_lonely_as_a_cloud_TIMESTAMP.mp4` (Primary bilingual video)
* `output/I_wandered_lonely_as_a_cloud_TIMESTAMP_en.mp4` (English narrated)
* `output/I_wandered_lonely_as_a_cloud_TIMESTAMP_zh.mp4` (Chinese narrated)

---

### 2. Run Built-In World Poetry Samples

You can generate videos from any of the built-in classical and world poetry samples across **7 languages** (Chinese, English, Japanese, French, Spanish, Hindi, German):

```powershell
# 1. Japanese Zen Haiku (Matsuo Basho) with anime aesthetic, Japanese voice + English subtitles
.\venv\Scripts\python.exe main.py --sample basho_old_pond --all-languages

# 2. Hindi Heroic Ode (Harivansh Rai Bachchan) with oil painting style, Hindi voice + English subtitles
.\venv\Scripts\python.exe main.py --sample agneepath --all-languages

# 3. French Classic (Victor Hugo) with oil painting style, French voice + English subtitles
.\venv\Scripts\python.exe main.py --sample demain_des_laube --all-languages

# 4. Spanish Surrealist Landscape (Federico Garcia Lorca) with watercolor style, Spanish voice + English subtitles
.\venv\Scripts\python.exe main.py --sample lorca_paisaje --all-languages

# 5. German Twilight Meditation (Goethe) with oil painting style, German voice + English subtitles
.\venv\Scripts\python.exe main.py --sample goethe_wanderer --all-languages

# 6. Chinese Classical Tang Masterpiece (Li Bai) with traditional ink wash style, Chinese voice + English subtitles
.\venv\Scripts\python.exe main.py --sample quiet_night --all-languages

# 7. English Romantic Ode (Wordsworth) with watercolor style, English voice + Chinese subtitles
.\venv\Scripts\python.exe main.py --sample daffodils --all-languages

# 8. English Autumn Contemplation (Robert Frost) with oil painting style
.\venv\Scripts\python.exe main.py --sample road_not_taken --all-languages
```

View all built-in poems anytime:
```powershell
.\venv\Scripts\python.exe main.py --list-samples
```

---

### 3. Run Custom Poems

#### From Direct Text:
```powershell
.\venv\Scripts\python.exe main.py --text "Two roads diverged in a yellow wood, And sorry I could not travel both" --style oil_painting
```

#### From a Text File in `examples/`:
The repository provides ready-to-run text files in [`examples/`](file:///d:/Desktop/sem-7/RM%20Project/examples/):
```powershell
.\venv\Scripts\python.exe main.py --file examples/basho_old_pond.txt --style anime --languages ja,en --all-languages
.\venv\Scripts\python.exe main.py --file examples/agneepath.txt --style oil_painting --languages hi,en --all-languages
.\venv\Scripts\python.exe main.py --file examples/demain_des_laube.txt --style oil_painting --languages fr,en --all-languages
.\venv\Scripts\python.exe main.py --file examples/lorca_paisaje.txt --style watercolor --languages es,en --all-languages
.\venv\Scripts\python.exe main.py --file examples/goethe_wanderer.txt --style oil_painting --languages de,en --all-languages
```

---

### 4. Fast Testing Mode (No Image API Calls)
If you want to test the entire pipeline without calling image generation APIs, use the built-in placeholder generator:
```powershell
.\venv\Scripts\python.exe main.py --sample quiet_night --provider placeholder
```

---

## 🌍 World Poetry Catalog (7 Languages)

| Sample Key | Poem Title & Author | Language | Audio Voice | Suggested Style |
| :--- | :--- | :--- | :--- | :--- |
| `spring_dawn` | **Spring Dawn (春晓)** — Meng Haoran | Chinese | `zh-CN-YunxiNeural` | `chinese_ink` |
| `quiet_night` | **Quiet Night Thought (静夜思)** — Li Bai | Chinese | `zh-CN-YunxiNeural` | `chinese_ink` |
| `deer_park` | **Deer Park (鹿柴)** — Wang Wei | Chinese | `zh-CN-YunxiNeural` | `chinese_ink` |
| `daffodils` | **I Wandered Lonely as a Cloud** — William Wordsworth | English | `en-US-AriaNeural` | `watercolor` |
| `boy_singing` | **A Boy Singing in the Rain** — Lyrical | English | `en-US-AriaNeural` | `watercolor` |
| `road_not_taken` | **The Road Not Taken** — Robert Frost | English | `en-US-AriaNeural` | `oil_painting` |
| `hope_feathers` | **“Hope” is the thing with feathers** — Emily Dickinson | English | `en-US-AriaNeural` | `watercolor` |
| `ozymandias` | **Ozymandias** — Percy Bysshe Shelley | English | `en-US-AriaNeural` | `oil_painting` |
| `basho_old_pond` | **The Old Pond (古池や)** — Matsuo Bashō | Japanese | `ja-JP-NanamiNeural` | `anime` |
| `demain_des_laube` | **Demain, dès l'aube** — Victor Hugo | French | `fr-FR-DeniseNeural` | `oil_painting` |
| `lorca_paisaje` | **Paisaje** — Federico García Lorca | Spanish | `es-ES-ElviraNeural` | `watercolor` |
| `agneepath` | **Agneepath (अग्निपथ)** — Harivansh Rai Bachchan | Hindi | `hi-IN-SwaraNeural` | `oil_painting` |
| `goethe_wanderer` | **Wanderers Nachtlied** — J.W. von Goethe | German | `de-DE-KatjaNeural` | `oil_painting` |

---

## 🎨 Available Artistic Styles

You can choose any artistic style using `--style <name>`:

| Style Key | Visual Appearance |
| :--- | :--- |
| `chinese_ink` *(Default)* | Traditional Chinese ink wash (*shanshui*), rice paper texture, sumi-e brushwork |
| `watercolor` | Soft washes, delicate blending, luminous transparency, wet-on-wet |
| `oil_painting` | Rich textures, classical museum quality, impasto technique |
| `digital_art` | Concept art, cinematic lighting, ArtStation trending, 4K |
| `anime` | Studio Ghibli inspired scenery, vibrant colors, detailed backgrounds |

List all styles:
```powershell
.\venv\Scripts\python.exe main.py --list-styles
```

---

## 🛠️ CLI Options Reference

| Argument | Description | Default |
| :--- | :--- | :--- |
| `--sample <name>` | Select built-in poem: `spring_dawn`, `quiet_night`, `daffodils`, `road_not_taken`, `agneepath`, etc. | None |
| `--text "..."` | Provide custom poem text directly | None |
| `--file <path>` | Path to text file containing a poem | None |
| `--style <style>` | Artistic style preset (`chinese_ink`, `watercolor`, `oil_painting`, `anime`, `digital_art`) | `chinese_ink` |
| `--languages <codes>` | Target subtitle languages, comma-separated (e.g. `en,zh`, `hi,en`, `ja,en`) | From `.env` (`en,zh`) |
| `--all-languages` | Render separate localized MP4 files for each target language (Mode B) | False |
| `--provider <prov>` | Image generation provider: `pollinations`, `huggingface`, `placeholder` | `pollinations` |
| `--frames <int>` | Number of animation frames per visual segment | `24` |
| `--output <name>` | Custom output video filename (without `.mp4`) | Auto-generated |
| `--evaluate` | Automatically run Multi-Modal Validation Suite after rendering | False |
| `--no-segmentation` | Disable semantic segmentation (forces rigid 1 image per line) | False |
| `--no-refine` | Disable LLM prompt self-critique loop | False |
| `--no-parallel` | Disable concurrent parallel image generation | False |
| `--quiet` | Suppress detailed prompt output in terminal | False |

---

## 📊 Multi-Modal Validation & Accuracy Metrics Suite

The system includes a scientific evaluation benchmark ([`evaluate.py`](file:///Users/shree/RM/Poem-to-Video/evaluate.py) & [`src/evaluation/metrics.py`](file:///Users/shree/RM/Poem-to-Video/src/evaluation/metrics.py)) that measures the accuracy of both the generated text and visuals, producing an overall **Multimodal Quality Index (MQI, 0–100)**:

### 1. The 9 Evaluated Metrics
1. **Literary Grounding & Fidelity (0–100):** Audits paraphrase accuracy, literal meaning fidelity, and lack of literary hallucination.
2. **12-Dimensional Visual Coverage (0–100):** Evaluates completeness across all 12 visual dimensions from IEEE TLT 2024.
3. **Translation Quality & Subtitle Fitness (0–100):** Assesses semantic preservation across target languages and subtitle brevity.
4. **Segmentation Cohesion (0–100):** Verifies that merged lines share emotional valence and spatial setting.
5. **Text-to-Image Semantic Alignment (0–100):** Multimodal VLM inspection (Gemini Vision) measuring how faithfully each image depicts the poetic scenario.
6. **Entity Visual Recall (0–100%):** Object detection evaluating whether extracted poetic entities are visibly present in the frame.
7. **Artistic Style Adherence (0–100):** VLM audit verifying brushwork, medium, and texture against the chosen art preset.
8. **Color Script Palette Adherence (0–100):** Computer vision pixel-sampling measuring Euclidean RGB distance to the locked 4-color palette in `visual_blueprint`.
9. **Cross-Scene Visual Coherence (0–100%):** 3D color histogram cosine similarity across consecutive scenes ($\cos(\mathbf{h}_i, \mathbf{h}_{i+1})$).

### 2. How to Run Validation

```bash
# Evaluate the most recent pipeline run:
python evaluate.py --latest

# Evaluate a specific timestamped run:
python evaluate.py --dir temp/pipeline_20261115_002920

# Pure local evaluation (fast CV & text metrics, skipping VLM):
python evaluate.py --latest --quick

# Render a video and automatically run the validation suite in one command:
python main.py --sample agneepath --evaluate
```

### 3. Sample Benchmark Results (*Agneepath - Path of Fire*)

```
════════════════════════════════════════════════════════════════════════
        🏆 POEM-TO-VIDEO MULTI-MODAL ACCURACY BENCHMARK REPORT
════════════════════════════════════════════════════════════════════════
  Poem Title:        Agneepath (अग्निपथ - Path of Fire)
  Poet:              Harivansh Rai Bachchan
  Overall MQI Score: 89.6/100   [██████████████████░░]   Grade: A (High Fidelity)
────────────────────────────────────────────────────────────────────────

  📝 MODULE 1: TEXT ACCURACY & LITERARY FIDELITY
  ────────────────────────────────────────────────────────────────────
    • Literary Grounding      100.0%  [████████████████]
    • 12-D Visual Coverage    100.0%  [████████████████]
    • Emotion Tag Coverage    100.0%  [████████████████]
    • NER Entity Density       56.0%  [█████████░░░░░░░]
    • Segmentation Cohesion    90.0%  [██████████████░░]
    • Translation Fidelity    100.0%  [████████████████]

  🎨 MODULE 2: IMAGE ACCURACY & MULTIMODAL ALIGNMENT
  ────────────────────────────────────────────────────────────────────
    • Text-to-Image Alignment     86.0%  [██████████████░░]
    • Artistic Style Adherence    87.2%  [██████████████░░]
    • Entity Visual Recall        81.0%  [█████████████░░░]
    • Color Script Palette Match  81.9%  [█████████████░░░]
    • Cross-Scene Coherence       82.5%  [█████████████░░░]
════════════════════════════════════════════════════════════════════════
```

---

## 📂 Where to See the Generated Files

### 1. Final Videos
All rendered situational videos are stored directly in the **`output/`** folder:
* Location: `D:\Desktop\sem-7\RM Project\output\`
* Format: H.264 video with AAC audio in standard `.mp4` format, compatible with all video players.

### 2. Intermediate Pipeline Files
Every run creates a timestamped folder inside **`temp/`** (e.g. `temp/pipeline_20261114_023315/`):
* `01_paraphrase.json`: Literary analysis with emotion and NER tags.
* `01b_segments.json`: Semantic segments grouped by scene continuity.
* `02_key_elements.json`: 12-dimensional keyword extractions.
* `03_prompts.json`: The refined Stable Diffusion prompts and critique rationales.
* `key_frames/`: High-resolution (1024×576) key frame artwork.
* `segment_frames/`: Ken Burns animation frames for each segment.
* `transitions/`: Cross-fade blend frames between visual scenes.
* `tts/`: Spoken audio MP3 files for narration.
