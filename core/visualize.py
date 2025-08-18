import cv2, numpy as np
COLORS = {
    'seedling': (0,180,255), 'inflorescence': (0,200,0), 'stem': (255,160,0), 'root': (180,0,255)
}

def draw_bbox(img, xywh, color, label: str | None = None):
    x,y,w,h = xywh
    cv2.rectangle(img, (x,y), (x+w,y+h), color, 2)
    if label:
        cv2.putText(img, label, (x, y-6), cv2.FONT_HERSHEY_SIMPLEX, 0.55, color, 2, cv2.LINE_AA)

def draw_polyline(img, pts, color, thickness=2):
    if len(pts)>=2:
        cv2.polylines(img, [np.array(pts, dtype=np.int32)], False, color, thickness)