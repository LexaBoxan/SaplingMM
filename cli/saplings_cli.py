from __future__ import annotations
import argparse
from pathlib import Path
from core.service import CoreService
from core.scale import compute_scale_from_points, save_scale_near_image

def cmd_calibrate(args):
    p = Path(args.image)
    # простая CL-версия: ожидаем координаты через аргументы, GUI делает клики
    p1 = (args.x1, args.y1); p2 = (args.x2, args.y2)
    scale = compute_scale_from_points(p1, p2, args.step_mm)
    out = save_scale_near_image(p, scale)
    print(f"Saved {out} mm/px={scale.mm_per_px:.6f}")

def cmd_process(args):
    service = CoreService(args.det1, args.det2, conf=args.conf, iou=args.iou)
    p = Path(args.path)
    paths = [p] if p.is_file() else [q for q in p.rglob('*') if q.suffix.lower() in {'.jpg','.jpeg','.png','.tif','.tiff'}]
    for img in paths:
        res = service.process(img, export_excel=args.export_excel)
        print(f"Processed {img} → {res['overlay_path']}")


def main():
    ap = argparse.ArgumentParser("Saplings CLI")
    sub = ap.add_subparsers(dest='cmd', required=True)

    apc = sub.add_parser('calibrate')
    apc.add_argument('image')
    apc.add_argument('--x1', type=float, required=True)
    apc.add_argument('--y1', type=float, required=True)
    apc.add_argument('--x2', type=float, required=True)
    apc.add_argument('--y2', type=float, required=True)
    apc.add_argument('--step-mm', type=float, default=5.0)
    apc.set_defaults(func=cmd_calibrate)

    app = sub.add_parser('process')
    app.add_argument('path')
    app.add_argument('--det1', required=True)
    app.add_argument('--det2', required=True)
    app.add_argument('--conf', type=float, default=0.25)
    app.add_argument('--iou', type=float, default=0.45)
    app.add_argument('--export-excel', action='store_true')
    app.set_defaults(func=cmd_process)

    args = ap.parse_args()
    args.func(args)

if __name__ == '__main__':
    main()
