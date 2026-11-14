"""
Semantic Segmentation Engine — Module 1, Step 1.5

Implements Emotion + NER-Driven Semantic Segmentation.
Instead of rigidly splitting images line-by-line, it evaluates adjacent lines
using two signals:
  1. Dominant Emotion: emotion continuity vs. emotion shift.
  2. Named Entity Recognition (NER): entity continuity vs. location/subject change.

Lines that describe the same ongoing scene and emotion are grouped into a
single visual Segment, improving visual continuity and eliminating jarring transitions.

Reference: Section 4.1 of the Enhanced Architecture document.
"""

from dataclasses import dataclass, field
from src.config import ENABLE_SEMANTIC_SEGMENTATION


@dataclass
class Segment:
    """Represents a coherent visual scene composed of one or more poem lines."""
    segment_id: int
    line_indices: list[int]
    lines: list[str]
    merged_text: str
    dominant_emotion: str
    ner_tags: list[str]
    literal_meaning: str
    imagery: str
    symbolism: str
    background: str

    def to_dict(self) -> dict:
        return {
            "segment_id": self.segment_id,
            "line_indices": self.line_indices,
            "lines": self.lines,
            "merged_text": self.merged_text,
            "dominant_emotion": self.dominant_emotion,
            "ner_tags": self.ner_tags,
            "literal_meaning": self.literal_meaning,
            "imagery": self.imagery,
            "symbolism": self.symbolism,
            "background": self.background,
        }


# Emotion clusters for valence-arousal compatibility
EMOTION_CLUSTERS = [
    {"tranquility", "peaceful", "calm", "serene", "solitude", "contemplation", "cozy", "lazy"},
    {"melancholy", "sadness", "longing", "nostalgia", "bittersweet", "wistful", "grief"},
    {"joy", "cheerful", "vibrant", "lively", "awakening", "playful", "delight"},
    {"awe", "wonder", "reverence", "grandeur", "sublime"},
    {"fear", "terror", "stormy", "uneasy", "darkness", "dread"}
]


def _are_emotions_compatible(emo_a: str, emo_b: str) -> bool:
    """Check if two emotion labels belong to the same emotional valence/cluster."""
    a = emo_a.strip().lower()
    b = emo_b.strip().lower()
    if a == b:
        return True
    for cluster in EMOTION_CLUSTERS:
        if any(c in a for c in cluster) and any(c in b for c in cluster):
            return True
    return False


def _get_entity_categories(ner_tags: list[str]) -> set[str]:
    """Extract distinct entity category prefixes from NER tags."""
    categories = set()
    for tag in ner_tags:
        if ":" in tag:
            cat, val = tag.split(":", 1)
            categories.add(f"{cat.strip().upper()}:{val.strip().lower()}")
    return categories


def _has_drastic_entity_shift(tags_a: list[str], tags_b: list[str]) -> bool:
    """
    Detect if there is a primary scene transition (e.g. PLACE shifts from courtyard to mountain).
    """
    places_a = [t.split(":", 1)[1].strip().lower() for t in tags_a if t.upper().startswith("PLACE:")]
    places_b = [t.split(":", 1)[1].strip().lower() for t in tags_b if t.upper().startswith("PLACE:")]

    if places_a and places_b:
        # If both specify places and have zero overlap, it's a scene shift
        if not set(places_a).intersection(set(places_b)):
            return True
    return False


def segment_poem(paraphrase_data: dict, enable_segmentation: bool = None) -> list[Segment]:
    """
    Group poem lines into coherent visual segments based on Emotion and NER signals.

    Args:
        paraphrase_data: Output dictionary from paraphrase_poem.
        enable_segmentation: Override flag for semantic segmentation.

    Returns:
        List of Segment objects.
    """
    if enable_segmentation is None:
        enable_segmentation = ENABLE_SEMANTIC_SEGMENTATION

    lines = paraphrase_data.get("lines", [])
    if not lines:
        return []

    # If segmentation is disabled, create 1 segment per line (base paper behavior)
    if not enable_segmentation:
        print("  [Segmentation] Using base mode: 1 segment per line")
        segments = []
        for i, ld in enumerate(lines):
            seg = Segment(
                segment_id=i,
                line_indices=[i],
                lines=[ld.get("original", "")],
                merged_text=ld.get("original", ""),
                dominant_emotion=ld.get("dominant_emotion", ld.get("emotion", "")),
                ner_tags=ld.get("ner_tags", []),
                literal_meaning=ld.get("literal_meaning", ""),
                imagery=ld.get("imagery", ""),
                symbolism=ld.get("symbolism", ""),
                background=ld.get("background", "")
            )
            segments.append(seg)
        return segments

    print("  [Segmentation] Applying Emotion + NER-Driven Semantic Segmentation...")
    segments: list[Segment] = []

    current_indices = [0]
    current_lines = [lines[0].get("original", "")]
    current_emotion = lines[0].get("dominant_emotion", "serenity")
    current_ner = list(lines[0].get("ner_tags", []))
    current_meanings = [lines[0].get("literal_meaning", "")]
    current_imageries = [lines[0].get("imagery", "")]
    current_symbolisms = [lines[0].get("symbolism", "")]
    current_backgrounds = [lines[0].get("background", "")]

    for i in range(1, len(lines)):
        prev_line = lines[i - 1]
        curr_line = lines[i]

        curr_emotion = curr_line.get("dominant_emotion", "serenity")
        curr_ner = curr_line.get("ner_tags", [])

        emotion_match = _are_emotions_compatible(current_emotion, curr_emotion)
        entity_shift = _has_drastic_entity_shift(current_ner, curr_ner)

        # Merge rule: compatible emotion AND no drastic entity shift (max 2 lines per segment for rhythmic cuts)
        if emotion_match and not entity_shift and len(current_indices) < 2:
            # Merge into current segment
            current_indices.append(i)
            current_lines.append(curr_line.get("original", ""))
            current_ner.extend([t for t in curr_ner if t not in current_ner])
            current_meanings.append(curr_line.get("literal_meaning", ""))
            current_imageries.append(curr_line.get("imagery", ""))
            if curr_line.get("symbolism"):
                current_symbolisms.append(curr_line.get("symbolism"))
            if curr_line.get("background"):
                current_backgrounds.append(curr_line.get("background"))
        else:
            # Finalize current segment
            seg_id = len(segments)
            segments.append(Segment(
                segment_id=seg_id,
                line_indices=current_indices,
                lines=current_lines,
                merged_text=" / ".join(current_lines),
                dominant_emotion=current_emotion,
                ner_tags=current_ner,
                literal_meaning="; ".join(current_meanings),
                imagery=" ".join(current_imageries),
                symbolism="; ".join(current_symbolisms),
                background="; ".join(set(current_backgrounds))
            ))
            # Start new segment
            current_indices = [i]
            current_lines = [curr_line.get("original", "")]
            current_emotion = curr_emotion
            current_ner = list(curr_ner)
            current_meanings = [curr_line.get("literal_meaning", "")]
            current_imageries = [curr_line.get("imagery", "")]
            current_symbolisms = [curr_line.get("symbolism", "")]
            current_backgrounds = [curr_line.get("background", "")]

    # Append trailing segment
    seg_id = len(segments)
    segments.append(Segment(
        segment_id=seg_id,
        line_indices=current_indices,
        lines=current_lines,
        merged_text=" / ".join(current_lines),
        dominant_emotion=current_emotion,
        ner_tags=current_ner,
        literal_meaning="; ".join(current_meanings),
        imagery=" ".join(current_imageries),
        symbolism="; ".join(current_symbolisms),
        background="; ".join(set(current_backgrounds))
    ))

    print(f"  [Segmentation] ✓ Grouped {len(lines)} lines into {len(segments)} visual segments")
    for s in segments:
        print(f"    • Segment {s.segment_id+1}: lines {s.line_indices} | Emotion: '{s.dominant_emotion}' | \"{s.merged_text[:40]}\"")

    return segments
