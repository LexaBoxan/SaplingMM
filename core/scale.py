from __future__ import annotations
import json
from pathlib import Path
from .types import Scale

def compute_scale_from_points(p1: tuple[float,float], p2: tuple[float,float], step_mm: float) -> Scale:
    import math
    dx = p2[0] - p1[0]
    dy = p2[1] - p1[1]
    dist_px = math.hypot(dx, dy)
    if dist_px <= 0:
        raise ValueError("Нулевая дистанция для калибровки")
    return Scale(mm_per_px=step_mm / dist_px)


def scale_path_near_image(img: Path) -> Path:
    out = img.parent / f"{img.stem}_results" / "scale.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    return out


def save_scale_near_image(img: Path, scale: Scale) -> Path:
    p = scale_path_near_image(img)
    with open(p, "w", encoding="utf-8") as f:
        json.dump({"mm_per_px": scale.mm_per_px}, f, ensure_ascii=False, indent=2)
    return p


def load_scale_near_image(img: Path) -> Scale:
    p = scale_path_near_image(img)
    data = json.loads(p.read_text(encoding="utf-8"))
    return Scale(mm_per_px=float(data["mm_per_px"]))