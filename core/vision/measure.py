from dataclasses import dataclass
import numpy as np

def length_and_angle_from_polyline(polyline: list[tuple[int,int]]):
    if len(polyline)<2: return 0.0, None
    L=0.0
    for (x1,y1),(x2,y2) in zip(polyline[:-1], polyline[1:]):
        L += ((x2-x1)**2 + (y2-y1)**2) ** 0.5
    pts=np.array(polyline, dtype=float); x=pts[:,0]; y=pts[:,1]
    A=np.vstack([x, np.ones_like(x)]).T
    k,_=np.linalg.lstsq(A,y,rcond=None)[0]
    ang_to_x=np.degrees(np.arctan(k))
    return float(L), float(90.0 - ang_to_x)

def px_to_mm(px: float, mm_per_px: float) -> float:
    return float(px) * float(mm_per_px)