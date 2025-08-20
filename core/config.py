"""Configuration loading utilities for the core package."""
from __future__ import annotations

from pathlib import Path
import yaml
from dataclasses import dataclass


@dataclass
class Settings:
    """Represents core configuration settings."""
    det1: Path
    det2: Path
    conf: float
    iou: float
    imgsz_seedling: int
    imgsz_parts: int
    results_dir: Path
    export_excel: bool = True


def load_settings(path: Path | str = "config/settings.yaml") -> Settings:
    """Load settings from a YAML file."""
    with open(path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    models = data.get("models", {})
    yolo = data.get("yolo", {})
    export = data.get("export", {})
    return Settings(
        det1=Path(models.get("det1", "models/seedling.pt")),
        det2=Path(models.get("det2", "models/parts.pt")),
        conf=float(yolo.get("conf", 0.25)),
        iou=float(yolo.get("iou", 0.45)),
        imgsz_seedling=int(yolo.get("imgsz_seedling", 1280)),
        imgsz_parts=int(yolo.get("imgsz_parts", 640)),
        results_dir=Path(data.get("results_dir", "results")),
        export_excel=bool(export.get("excel", True)),
    )
