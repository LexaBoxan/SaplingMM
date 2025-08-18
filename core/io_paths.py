from pathlib import Path

def results_dir_for(image_path: Path, root: Path | None = None) -> Path:
    root = Path(root) if root else image_path.parent / f"{image_path.stem}_results"
    root.mkdir(parents=True, exist_ok=True)
    return root