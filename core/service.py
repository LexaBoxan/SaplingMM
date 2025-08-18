from __future__ import annotations
from pathlib import Path
import cv2
from .types import Detection, PartMeasure, SeedlingResult
from .scale import load_scale_near_image
from .detectors.seedling import SeedlingDetector
from .detectors.parts import PartsDetector
from .vision.crops import crop_with_pad
from .vision.binarize import clean_binary
from .vision.skeleton import to_skeleton, longest_path_polyline
from .vision.measure import length_and_angle_from_polyline, px_to_mm
from .visualize import draw_bbox, draw_polyline, COLORS
from .export import save_json, save_csv, maybe_save_excel
from .io_paths import results_dir_for

class CoreService:
    def __init__(self, det1_path: str, det2_path: str, conf: float = 0.25, iou: float = 0.45,
                 imgsz_seedling: int = 1280, imgsz_parts: int = 640, device: str = 'cpu'):
        self.det1 = SeedlingDetector(det1_path, conf=conf, imgsz=imgsz_seedling, device=device)
        self.det2 = PartsDetector(det2_path, conf=conf, iou=iou, imgsz=imgsz_parts, device=device)

    def process(self, image_path: Path, export_excel: bool = True) -> dict:
        img = cv2.imread(str(image_path))
        if img is None:
            raise RuntimeError(f"Не удалось загрузить изображение: {image_path}")
        out_dir = results_dir_for(image_path)
        scale = load_scale_near_image(image_path)

        # 1) det#1
        seed_boxes = self.det1.predict(img)
        overlay = img.copy()
        rows = []
        instances = []

        for sid, (x,y,w,h,score) in enumerate(seed_boxes, start=1):
            draw_bbox(overlay, (x,y,w,h), COLORS['seedling'], f"seedling#{sid} {score:.2f}")
            crop, (ox,oy) = crop_with_pad(img, (x,y,w,h), pad=10)
            # 2) det#2
            parts = self.det2.predict(crop)
            parts_meas: dict[str, PartMeasure] = {}
            for (cls, px,py,pw,ph,pconf) in parts:
                roi = crop[py:py+ph, px:px+pw]
                _, binroi = clean_binary(roi)
                sk = to_skeleton(binroi)
                poly = longest_path_polyline(sk) if cls in ("stem","root") else []
                Lpx, ang = length_and_angle_from_polyline(poly) if poly else (0.0, None)
                meas = PartMeasure(length_px=Lpx, angle_deg=ang, polyline=[(x+px+ox, y+py+oy) for (x,y) in poly])
                parts_meas[cls] = meas
                # viz
                draw_bbox(crop, (px,py,pw,ph), COLORS.get(cls,(255,255,255)), f"{cls}")
                if meas.polyline:
                    draw_polyline(overlay, meas.polyline, COLORS.get(cls,(255,255,255)))

            stem_mm = px_to_mm(parts_meas.get('stem', PartMeasure()).length_px, scale.mm_per_px)
            root_mm = px_to_mm(parts_meas.get('root', PartMeasure()).length_px, scale.mm_per_px)

            instances.append({
                'id': sid,
                'seedling_bbox': [x,y,w,h],
                'parts': {k: {
                    'length_px': v.length_px,
                    'angle_deg': v.angle_deg,
                    'polyline': v.polyline or []
                } for k,v in parts_meas.items()}
            })
            rows.append({
                'image': image_path.name,
                'seedling_id': sid,
                'stem_len_mm': round(stem_mm,2),
                'root_len_mm': round(root_mm,2)
            })

        # save
        import cv2
        cv2.imwrite(str(out_dir/"overlay.jpg"), overlay)
        save_json({'image': image_path.name, 'mm_per_px': scale.mm_per_px, 'seedlings': instances}, out_dir/"instances.json")
        save_csv(rows, out_dir/"measurements.csv")
        if export_excel:
            maybe_save_excel(rows, out_dir/"measurements.xlsx")

        return {
            'out_dir': out_dir,
            'overlay_path': out_dir/"overlay.jpg",
            'csv_path': out_dir/"measurements.csv",
            'json_path': out_dir/"instances.json",
            'stats': {'seedlings': len(instances), 'errors': 0}
        }