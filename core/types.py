from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, List, Tuple, Dict
import numpy as np

BBox = Tuple[int, int, int, int]  # x,y,w,h
Polyline = List[Tuple[int, int]]

@dataclass
class Scale:
    mm_per_px: float
    H: Optional[np.ndarray] = None

@dataclass
class Detection:
    cls: str
    bbox: BBox
    score: float

@dataclass
class PartMeasure:
    length_px: float = 0.0
    angle_deg: Optional[float] = None
    polyline: Polyline | None = None
    width_px: float = 0.0

@dataclass
class SeedlingResult:
    seed_bbox: BBox
    parts: Dict[str, PartMeasure]