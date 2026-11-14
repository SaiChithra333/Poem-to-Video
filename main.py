#!/usr/bin/env python3
"""
Poem-to-Video: Automatic Generation of Multimedia Teaching Materials
Enhanced Situational Video Generation System.

Based on: Chen & Wu, IEEE TLT 2024 with 5 Key Enhancements:
  1. Emotion + NER Semantic Segmentation
  2. Iterative LLM Prompt Refinement
  3. Parallel Asynchronous Image Generation
  4. Multi-Language Subtitle Overlay
  5. Multi-Language TTS Audio Narration

Usage:
    # Run with a sample poem
    python main.py --sample spring_dawn

    # English poem with French and Chinese subtitles
    python main.py --sample daffodils --languages en,zh,fr --style watercolor

    # Custom poem from text
    python main.py --text "Two roads diverged in a yellow wood, ..."

    # Run with placeholder images (offline/fast test mode)
    python main.py --sample spring_dawn --provider placeholder
"""

import argparse
import sys
from pathlib import Path

# Ensure project root is in the Python path
sys.path.insert(0, str(Path(__file__).parent))

# Ensure UTF-8 console output on Windows to prevent charmap UnicodeEncodeError
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

from src.config import STYLE_PRESETS, DEFAULT_STYLE, TARGET_LANGUAGES
from src.pipeline import run_pipeline


# ─── Sample Poems ────────────────────────────────────────────────────────────

SAMPLE_POEMS = {
    # ── Chinese Classics ──
    "spring_dawn": {
        "title": "Spring Dawn (春晓)",
        "poet": "Meng Haoran (孟浩然)",
        "text": """春眠不觉晓，
处处闻啼鸟。
夜来风雨声，
花落知多少。""",
        "language": "chinese",
        "default_style": "chinese_ink",
        "default_languages": "zh,en",
        "description": "Meng Haoran's classic about waking to birdsong and fallen blossoms"
    },
    "quiet_night": {
        "title": "Quiet Night Thought (静夜思)",
        "poet": "Li Bai (李白)",
        "text": """床前明月光，
疑是地上霜。
举头望明月，
低头思故乡。""",
        "language": "chinese",
        "default_style": "chinese_ink",
        "default_languages": "zh,en",
        "description": "Li Bai's timeless poem about moonlit solitude and homesickness"
    },
    "drinking_alone": {
        "title": "Drinking Alone Under the Moon (月下独酌)",
        "poet": "Li Bai (李白)",
        "text": """花间一壶酒，
独酌无相亲。
举杯邀明月，
对影成三人。
月既不解饮，
影徒随我身。
暂伴月将影，
行乐须及春。
我歌月徘徊，
我舞影零乱。
醒时同交欢，
醉后各分散。
永结无情游，
相期邈云汉。""",
        "language": "chinese",
        "default_style": "chinese_ink",
        "default_languages": "zh,en,ja",
        "description": "Li Bai's 14-line lyrical masterpiece on solitude, wine, moonlight, and shadows (~1 min)"
    },
    "deer_park": {
        "title": "Deer Park (鹿柴)",
        "poet": "Wang Wei (王维)",
        "text": """空山不见人，
但闻人语响。
返景入深林，
复照青苔上。""",
        "language": "chinese",
        "default_style": "chinese_ink",
        "default_languages": "zh,en",
        "description": "Wang Wei's Zen masterpiece of solitude, deep woods, and green moss"
    },

    # ── English Classics ──
    "daffodils": {
        "title": "I Wandered Lonely as a Cloud",
        "poet": "William Wordsworth",
        "text": """I wandered lonely as a cloud
That floats on high o'er vales and hills,
When all at once I saw a crowd,
A host, of golden daffodils;
Beside the lake, beneath the trees,
Fluttering and dancing in the breeze.""",
        "language": "english",
        "default_style": "watercolor",
        "default_languages": "en,zh",
        "description": "Wordsworth's Romantic ode to the dancing golden daffodils beside the lake"
    },
    "boy_singing": {
        "title": "A Boy Singing in the Rain",
        "poet": "Unknown",
        "text": """A boy singing in the rain,
Walking through the ancient forest,
His voice echoing among the tall trees,
Raindrops glistening on green leaves,
Joyful tunes filling the misty air.""",
        "language": "english",
        "default_style": "watercolor",
        "default_languages": "en,zh",
        "description": "A lyrical ode to childhood exuberance and harmony with ancient forests"
    },
    "road_not_taken": {
        "title": "The Road Not Taken",
        "poet": "Robert Frost",
        "text": """Two roads diverged in a yellow wood,
And sorry I could not travel both
And be one traveler, long I stood
And looked down one as far as I could
To where it bent in the undergrowth.""",
        "language": "english",
        "default_style": "oil_painting",
        "default_languages": "en,zh",
        "description": "Robert Frost's iconic contemplation on choices and destiny in autumn woods"
    },
    "stopping_by_woods": {
        "title": "Stopping by Woods on a Snowy Evening",
        "poet": "Robert Frost",
        "text": """Whose woods these are I think I know.
His house is in the village though;
He will not see me stopping here
To watch his woods fill up with snow.
My little horse must think it queer
To stop without a farmhouse near
Between the woods and frozen lake
The darkest evening of the year.
He gives his harness bells a shake
To ask if there is some mistake.
The only other sound’s the sweep
Of easy wind and downy flake.
The woods are lovely, dark and deep,
But I have promises to keep,
And miles to go before I sleep,
And miles to go before I sleep.""",
        "language": "english",
        "default_style": "watercolor",
        "default_languages": "en,zh,ja",
        "description": "Robert Frost's 16-line winter masterpiece on quiet contemplation and the journey ahead (~1 min)"
    },
    "hope_feathers": {
        "title": "“Hope” is the thing with feathers",
        "poet": "Emily Dickinson",
        "text": """“Hope” is the thing with feathers -
That perches in the soul -
And sings the tune without the words -
And never stops - at all -""",
        "language": "english",
        "default_style": "watercolor",
        "default_languages": "en,zh",
        "description": "Emily Dickinson's sublime allegory of eternal spiritual endurance"
    },
    "ozymandias": {
        "title": "Ozymandias",
        "poet": "Percy Bysshe Shelley",
        "text": """I met a traveller from an antique land,
Who said: Two vast and trunkless legs of stone
Stand in the desert. Near them, on the sand,
Half sunk a shattered visage lies, whose frown,
And wrinkled lip, and sneer of cold command,
Tell that its sculptor well those passions read.""",
        "language": "english",
        "default_style": "oil_painting",
        "default_languages": "en,zh",
        "description": "Shelley's meditation on the impermanence of power in desert sands"
    },

    # ── Japanese Zen Haiku ──
    "basho_old_pond": {
        "title": "The Old Pond (古池や)",
        "poet": "Matsuo Bashō (松尾芭蕉)",
        "text": """古池や
蛙飛びこむ
水の音""",
        "language": "japanese",
        "default_style": "anime",
        "default_languages": "ja,en",
        "description": "Matsuo Basho's quintessential Zen haiku on silence and water ripple"
    },

    # ── French Classic ──
    "demain_des_laube": {
        "title": "Demain, dès l'aube (Tomorrow at Dawn)",
        "poet": "Victor Hugo",
        "text": """Demain, dès l'aube, à l'heure où blanchit la campagne,
Je partirai. Vois-tu, je sais que tu m'attends.
J'irai par la forêt, j'irai par la montagne.
Je ne puis demeurer loin de toi plus longtemps.""",
        "language": "french",
        "default_style": "oil_painting",
        "default_languages": "fr,en",
        "description": "Victor Hugo's moving pilgrimage of enduring love across misty dawn mountains"
    },

    # ── Spanish Lyrical ──
    "lorca_paisaje": {
        "title": "Paisaje (Landscape)",
        "poet": "Federico García Lorca",
        "text": """La tarde equivocada
se vistió de frío.
Detrás de los cristales,
turbios, todos los niños
ven convertirse en pájaros
un árbol amarillo.""",
        "language": "spanish",
        "default_style": "watercolor",
        "default_languages": "es,en",
        "description": "Federico Garcia Lorca's surrealist twilight vision of autumn transformation"
    },

    # ── Hindi Masterpiece ──
    "agneepath": {
        "title": "Agneepath (अग्निपथ - Path of Fire)",
        "poet": "Harivansh Rai Bachchan (हरिवंश राय बच्चन)",
        "text": """वृक्ष हों भले खड़े,
हों घने हों बड़े,
एक पत्र छाँह भी,
माँग मत, माँग मत, माँग मत,
अग्निपथ अग्निपथ अग्निपथ।""",
        "language": "hindi",
        "default_style": "oil_painting",
        "default_languages": "hi,en",
        "description": "Harivansh Rai Bachchan's stirring anthem of indomitable courage and resolve"
    },

    # ── German Romantic ──
    "goethe_wanderer": {
        "title": "Wanderers Nachtlied (Wanderer's Nightsong)",
        "poet": "Johann Wolfgang von Goethe",
        "text": """Über allen Gipfeln
Ist Ruh,
In allen Wipfeln
Spürest du
Kaum einen Hauch;
Die Vögelein schweigen im Walde.
Warte nur, balde
Ruhest du auch.""",
        "language": "german",
        "default_style": "oil_painting",
        "default_languages": "de,en",
        "description": "Goethe's serene lyrical reflection on twilight falling over mountain peaks"
    },
}


def list_styles():
    """Print all available artistic style presets."""
    print("\n Available Artistic Styles:")
    print("=" * 55)
    for key, info in STYLE_PRESETS.items():
        marker = " (default)" if key == DEFAULT_STYLE else ""
        print(f"\n  {key}{marker}")
        print(f"    Name:   {info['name']}")
        print(f"    Prompt: {info['style_prompt'][:80]}...")
    print()


def list_samples():
    """Print all available sample poems across multiple world languages."""
    print("\n Available Sample Poems Across Languages:")
    print("=" * 70)
    for key, info in SAMPLE_POEMS.items():
        print(f"\n  • {key}")
        print(f"    Title:       {info['title']}")
        print(f"    Poet:        {info.get('poet', 'Unknown')}")
        print(f"    Language:    {info['language'].capitalize()} (Subtitles: {info.get('default_languages', 'en,zh')})")
        print(f"    Art Style:   {info.get('default_style', DEFAULT_STYLE)}")
        print(f"    Description: {info['description']}")
    print("\n" + "=" * 70)
    print(" Run with: python main.py --sample <name> --all-languages\n")


def main():
    parser = argparse.ArgumentParser(
        description="Poem-to-Video: Enhanced Situational Video Generation System",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py --sample spring_dawn --style chinese_ink --languages zh,en
  python main.py --sample daffodils --style watercolor --languages en,zh
  python main.py --text "Shall I compare thee to a summer's day?" --style oil_painting
  python main.py --sample quiet_night --provider placeholder
  python main.py --list-styles
  python main.py --list-samples
        """
    )

    # Input source
    input_group = parser.add_mutually_exclusive_group()
    input_group.add_argument(
        "--sample", type=str, choices=list(SAMPLE_POEMS.keys()),
        help="Use a built-in sample poem"
    )
    input_group.add_argument(
        "--text", type=str,
        help="Provide poem text directly"
    )
    input_group.add_argument(
        "--file", type=str,
        help="Path to a text file containing the poem"
    )

    # Visual & Language Options
    parser.add_argument(
        "--style", type=str, default=None,
        choices=list(STYLE_PRESETS.keys()),
        help=f"Artistic style preset (default: by poem or {DEFAULT_STYLE})"
    )
    parser.add_argument(
        "--language", type=str, default="auto",
        help="Poem source language (e.g. 'auto', 'chinese', 'english', 'japanese', 'french', 'spanish', 'hindi', 'german')"
    )
    parser.add_argument(
        "--languages", type=str, default=None,
        help="Comma-separated target languages for subtitles and narration (e.g. 'en,zh', 'ja,en', 'hi,en', 'fr,en')"
    )
    parser.add_argument(
        "--all-languages", action="store_true",
        help="Render separate localized video files for each target language (Mode B)"
    )
    parser.add_argument(
        "--provider", type=str, default=None,
        choices=["pollinations", "huggingface", "stability", "placeholder"],
        help="Image generation provider (default: from config)"
    )
    parser.add_argument(
        "--frames", type=int, default=24,
        help="Number of animation frames per visual segment (default: 24)"
    )
    parser.add_argument(
        "--output", type=str, default=None,
        help="Output video filename (without extension)"
    )

    # Enhanced Architecture Toggles
    parser.add_argument(
        "--no-segmentation", action="store_true",
        help="Disable semantic segmentation (use rigid 1 image per line)"
    )
    parser.add_argument(
        "--no-refine", action="store_true",
        help="Disable LLM prompt self-critique refinement"
    )
    parser.add_argument(
        "--no-parallel", action="store_true",
        help="Disable parallel asynchronous image generation"
    )
    parser.add_argument(
        "--quiet", action="store_true",
        help="Suppress verbose prompt output"
    )

    # Info commands
    parser.add_argument("--list-styles", action="store_true", help="List available styles")
    parser.add_argument("--list-samples", action="store_true", help="List sample poems")

    args = parser.parse_args()

    if args.list_styles:
        list_styles()
        return
    if args.list_samples:
        list_samples()
        return

    # Resolve poem text and metadata
    poem_text = None
    language = args.language
    style = args.style
    sample_title = None
    sample_poet = None
    target_langs_str = args.languages

    if args.sample:
        sample = SAMPLE_POEMS[args.sample]
        poem_text = sample["text"]
        sample_title = sample["title"]
        sample_poet = sample.get("poet", "")
        if language == "auto":
            language = sample["language"]
        if style is None:
            style = sample.get("default_style", DEFAULT_STYLE)
        if target_langs_str is None:
            target_langs_str = sample.get("default_languages", "en,zh")
        print(f"\n  Using sample poem: {sample['title']}")
        if sample_poet:
            print(f"  Poet: {sample_poet}")
        print(f"  ({sample['description']})\n")

    elif args.text:
        poem_text = args.text

    elif args.file:
        file_path = Path(args.file)
        if not file_path.exists():
            print(f"Error: File not found: {args.file}")
            sys.exit(1)
        poem_text = file_path.read_text(encoding="utf-8")

    else:
        print("Error: Please provide a poem using --sample, --text, or --file")
        print("Run 'python main.py --help' for usage information")
        sys.exit(1)

    style = style or DEFAULT_STYLE

    # Verify LLM provider
    from src.llm_client import LLM_PROVIDER
    if not LLM_PROVIDER:
        print("⚠ Warning: No LLM API key configured in .env file.")
        print("  GEMINI_API_KEY or OPENAI_API_KEY is required for Module 1.")
        sys.exit(1)

    target_langs = None
    if target_langs_str:
        target_langs = [l.strip() for l in target_langs_str.split(",") if l.strip()]

    # Run the pipeline
    try:
        output_path = run_pipeline(
            poem_text=poem_text,
            language=language,
            style=style,
            image_provider=args.provider,
            frames_per_line=args.frames,
            target_languages=target_langs,
            enable_segmentation=not args.no_segmentation,
            enable_refinement=not args.no_refine,
            parallel_images=not args.no_parallel,
            render_all_languages=args.all_languages,
            output_name=args.output,
            title_override=sample_title,
            poet_override=sample_poet,
            verbose=not args.quiet,
        )
        print(f"\n  🎬 Video rendered successfully at:\n     {output_path}\n")

    except KeyboardInterrupt:
        print("\n\n  Pipeline interrupted by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\n  ✗ Pipeline failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
