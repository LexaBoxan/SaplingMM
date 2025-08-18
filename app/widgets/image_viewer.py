from __future__ import annotations
from pathlib import Path
from PyQt5 import QtCore, QtGui, QtWidgets


class ImageViewer(QtWidgets.QGraphicsView):
    """
    Центр: просмотр изображения с zoom/pan.
    Методы:
      - load_image(path: Path)
      - set_pixmap(pixmap: QPixmap)
    """
    sig_click = QtCore.pyqtSignal(float, float)  # для калибровки (x,y в координатах сцены)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setRenderHints(
            QtGui.QPainter.Antialiasing
            | QtGui.QPainter.SmoothPixmapTransform
            | QtGui.QPainter.TextAntialiasing
        )
        self._scene = QtWidgets.QGraphicsScene(self)
        self.setScene(self._scene)
        self._pixmap_item: QtWidgets.QGraphicsPixmapItem | None = None
        self.setDragMode(QtWidgets.QGraphicsView.ScrollHandDrag)
        self.setTransformationAnchor(QtWidgets.QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QtWidgets.QGraphicsView.AnchorViewCenter)

    # совместимость с твоим main.py
    def load_image(self, path: Path):
        reader = QtGui.QImageReader(str(path))
        reader.setAutoTransform(True)
        img = reader.read()
        if img.isNull():
            # fallback через OpenCV
            import cv2
            bgr = cv2.imread(str(path))
            if bgr is None:
                raise RuntimeError(f"Не удалось открыть изображение: {path}")
            rgb = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)
            h, w, ch = rgb.shape
            img = QtGui.QImage(rgb.data, w, h, ch * w, QtGui.QImage.Format_RGB888)
        pix = QtGui.QPixmap.fromImage(img)
        self._scene.clear()
        self._pixmap_item = self._scene.addPixmap(pix)
        self._scene.setSceneRect(pix.rect())
        self.resetTransform()
        self.fitInView(self._pixmap_item, QtCore.Qt.KeepAspectRatio)

    def set_pixmap(self, pixmap: QtGui.QPixmap):
        self._scene.clear()
        self._pixmap_item = self._scene.addPixmap(pixmap)
        self._scene.setSceneRect(pixmap.rect())
        self.resetTransform()
        self.fitInView(self._pixmap_item, QtCore.Qt.KeepAspectRatio)

    # колесо мыши — зум
    def wheelEvent(self, event: QtGui.QWheelEvent):
        if event.angleDelta().y() == 0:
            return
        factor = 1.25 if event.angleDelta().y() > 0 else 0.8
        self.scale(factor, factor)

    # клик — координаты для калибровки
    def mousePressEvent(self, event: QtGui.QMouseEvent):
        if event.button() == QtCore.Qt.LeftButton:
            scene_pos = self.mapToScene(event.pos())
            self.sig_click.emit(scene_pos.x(), scene_pos.y())
        super().mousePressEvent(event)
