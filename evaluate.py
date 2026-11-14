#!/usr/bin/env python3
"""
Poem-to-Video Multi-Modal Validation CLI.

Measures the accuracy of the generated text (comprehension, 12-D keywords, translation)
and images (text-image alignment, style adherence, color script, cross-scene coherence).

Usage:
    # Evaluate the most recent pipeline run:
    python evaluate.py --latest

    # Evaluate a specific run directory:
    python evaluate.py --dir temp/pipeline_20261115_002920

    # Fast offline evaluation (pure CV & heuristic metrics, no VLM calls):
    python evaluate.py --latest --quick
"""

import argparse
import sys
from pathlib import Path

# Ensure project root in python path
sys.path.insert(0, str(Path(__file__).parent))

from src.config import TEMP_DIR, OUTPUT_DIR
from src.evaluation.metrics import evaluate_pipeline_run
from src.evaluation.report_generator import print_evaluation_dashboard, generate_markdown_report


def get_latest_pipeline_dir() -> Path | None:
    """Find the most recently modified pipeline run directory in temp/."""
    if not TEMP_DIR.exists():
        return None
    dirs = [d for d in TEMP_DIR.iterdir() if d.is_dir() and d.name.startswith("pipeline_")]
    if not dirs:
        return None
    dirs.sort(key=lambda d: d.stat().st_mtime, reverse=True)
    return dirs[0]


def main():
    parser = argparse.ArgumentParser(
        description="Poem-to-Video Validation & Accuracy Metrics Suite",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "--latest", action="store_true", default=True,
        help="Evaluate the most recent pipeline run in temp/ (default)"
    )
    group.add_argument(
        "--dir", type=str,
        help="Path to a specific pipeline run folder (e.g. temp/pipeline_20261115_002920)"
    )
    group.add_argument(
        "--sample", type=str,
        help="Find and evaluate the latest run for a specific sample name"
    )

    parser.add_argument(
        "--quick", action="store_true",
        help="Bypass multimodal VLM API calls and compute pure local CV/text metrics"
    )
    parser.add_argument(
        "--save", action="store_true", default=True,
        help="Save markdown report to output/ (default: True)"
    )

    args = parser.parse_args()

    # Resolve target directory
    target_dir = None
    if args.dir:
        target_dir = Path(args.dir)
    elif args.sample:
        # Search for runs matching sample name
        candidates = []
        for d in TEMP_DIR.iterdir():
            if d.is_dir() and d.name.startswith("pipeline_"):
                para_file = d / "01_paraphrase.json"
                if para_file.exists():
                    txt = para_file.read_text(encoding="utf-8").lower()
                    if args.sample.lower() in txt:
                        candidates.append(d)
        if candidates:
            candidates.sort(key=lambda d: d.stat().st_mtime, reverse=True)
            target_dir = candidates[0]
        else:
            print(f"Error: No past run found matching sample '{args.sample}'")
            sys.exit(1)
    else:
        target_dir = get_latest_pipeline_dir()

    if not target_dir or not target_dir.exists():
        print("Error: No pipeline runs found in temp/ directory to evaluate.")
        print("Run a poem first, e.g.: python main.py --sample agneepath")
        sys.exit(1)

    print(f"Selected pipeline run: {target_dir}")

    # Run evaluation
    report = evaluate_pipeline_run(
        work_dir=target_dir,
        skip_vlm=args.quick
    )

    # Print terminal dashboard
    print_evaluation_dashboard(report)

    # Save Markdown report
    if args.save:
        md_path = OUTPUT_DIR / f"evaluation_{target_dir.name}.md"
        generate_markdown_report(report, md_path)
        print(f"📄 Detailed Markdown report saved to: {md_path}\n")


if __name__ == "__main__":
    main()

