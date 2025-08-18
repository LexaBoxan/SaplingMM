from __future__ import annotations
from typing import List, Tuple
import numpy as np

class SeedlingDetector:
    def __init__(self, weights_path: str, conf: float = 0.25, imgsz: int = 1280, device: str = 'cpu'):
        self.weights_path = weights_path
        self.conf = conf
        self.imgsz = imgsz
        self.device = device
        self.model = None  # lazy

    def _ensure_model(self):
        if self.model is None:
            from ultralytics import YOLO
            self.model = YOLO(self.weights_path)

    def predict(self, image_bgr: np.ndarray):
        self._ensure_model()
        res = self.model.predict(
            source=image_bgr[:, :, ::-1],
            imgsz=self.imgsz,
            conf=self.conf,
            device=self.device,   # <-- ВАЖНО
            verbose=False
        )[0]
        out = []
        for b in res.boxes:
            x1, y1, x2, y2 = map(float, b.xyxy[0].tolist())
            out.append((int(x1), int(y1), int(x2 - x1), int(y2 - y1), float(b.conf)))
        return out
