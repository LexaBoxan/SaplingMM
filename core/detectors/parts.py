from __future__ import annotations
from typing import List, Tuple
import numpy as np

CLASS_NAMES = {0: "inflorescence", 1: "stem", 2: "root"}

class PartsDetector:
    def __init__(self, weights_path: str, conf: float = 0.25, iou: float = 0.45, imgsz: int = 640, device: str = 'cpu'):
        self.weights_path = weights_path
        self.conf = conf
        self.iou = iou
        self.imgsz = imgsz
        self.device = device
        self.model = None

    def _ensure_model(self):
        if self.model is None:
            from ultralytics import YOLO
            self.model = YOLO(self.weights_path)

    def predict(self, crop_bgr: np.ndarray):
        self._ensure_model()
        res = self.model.predict(
            source=crop_bgr[:, :, ::-1],
            imgsz=self.imgsz,
            conf=self.conf,
            iou=self.iou,
            device=self.device,   # <-- ВАЖНО
            verbose=False
        )[0]
        out = []
        for b in res.boxes:
            x1, y1, x2, y2 = map(float, b.xyxy[0].tolist())
            cls = {0:"inflorescence",1:"stem",2:"root"}.get(int(b.cls[0]), str(int(b.cls[0])))
            out.append((cls, int(x1), int(y1), int(x2-x1), int(y2-y1), float(b.conf)))
        return out
