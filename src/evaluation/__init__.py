"""
Evaluation and Validation Metrics Module for Poem-to-Video.

Provides quantitative and qualitative metrics to validate:
  1. Text Accuracy: Literary analysis fidelity, 12-D keyword coverage,
     translation accuracy, and semantic segmentation cohesion.
  2. Image Accuracy: Multimodal text-to-image semantic alignment (VLM),
     artistic style adherence, entity recall, color script adherence,
     and cross-scene visual coherence.
  3. Overall Benchmark: Composite Multimodal Quality Index (MQI).
"""

from src.evaluation.metrics import evaluate_pipeline_run
from src.evaluation.report_generator import print_evaluation_dashboard, generate_markdown_report

__all__ = [
    "evaluate_pipeline_run",
    "print_evaluation_dashboard",
    "generate_markdown_report",
]

