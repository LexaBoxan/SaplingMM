from typing import Tuple
import numpy as np

def crop_with_pad(img: np.ndarray, bbox_xywh: Tuple[int,int,int,int], pad: int = 10) -> tuple[np.ndarray, tuple[int,int]]:
    x, y, w, h = bbox_xywh
    H, W = img.shape[:2]
    x0 = max(0, x - pad); y0 = max(0, y - pad)
    x1 = min(W, x + w + pad); y1 = min(H, y + h + pad)
    return img[y0:y1, x0:x1].copy(), (x0, y0)