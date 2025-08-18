from __future__ import annotations
from pathlib import Path
from PyQt5 import QtCore

class _ProcessTask(QtCore.QRunnable):
    def __init__(self, det1_path: str, det2_path: str, image_path: str, done_sig: QtCore.pyqtSignal, status_sig: QtCore.pyqtSignal):
        super().__init__()
        self.det1_path = det1_path
        self.det2_path = det2_path
        self.image_path = image_path
        self.done_sig = done_sig
        self.status_sig = status_sig

    def run(self):
        try:
            # лениво импортируем только в рабочем потоке
            from core.service import CoreService
            svc = CoreService(self.det1_path, self.det2_path, device='cpu')  # CPU во избежание CUDA-конфликтов
            res = svc.process(Path(self.image_path))
            # вернуть результат в GUI-поток
            QtCore.QMetaObject.invokeMethod(
                self.done_sig, "emit", QtCore.Qt.QueuedConnection, QtCore.Q_ARG(str, str(res["overlay_path"]))
            )
            QtCore.QMetaObject.invokeMethod(
                self.status_sig, "emit", QtCore.Qt.QueuedConnection, QtCore.Q_ARG(str, f"Готово: {res['csv_path']}")
            )
        except Exception as e:
            QtCore.QMetaObject.invokeMethod(
                self.status_sig, "emit", QtCore.Qt.QueuedConnection, QtCore.Q_ARG(str, f"Ошибка: {e}")
            )

class AppController(QtCore.QObject):
    sig_status = QtCore.pyqtSignal(str)
    sig_overlay_ready = QtCore.pyqtSignal(str)

    def __init__(self, det1_path: str, det2_path: str, parent=None):
        super().__init__(parent)
        self.det1_path = det1_path
        self.det2_path = det2_path
        self.pool = QtCore.QThreadPool.globalInstance()

    def set_scale(self, image_path: Path, p1, p2, step_mm: float):
        # импортируем локально (без OpenCV/Torch)
        from core.scale import compute_scale_from_points, save_scale_near_image
        scale = compute_scale_from_points(p1, p2, step_mm)
        save_scale_near_image(image_path, scale)
        self.sig_status.emit(f"Калибровка сохранена. mm/px={scale.mm_per_px:.6f}")

    @QtCore.pyqtSlot(str)
    def process_image(self, image_path: str):
        self.sig_status.emit("Обработка запущена…")
        task = _ProcessTask(self.det1_path, self.det2_path, image_path, self.sig_overlay_ready, self.sig_status)
        self.pool.start(task)
