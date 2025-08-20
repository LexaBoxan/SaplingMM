from __future__ import annotations
import sys
from pathlib import Path
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import QMainWindow, QSplitter
# НЕ импортируем torch/ultralytics нигде здесь

# Вспомогательные отладочные инструменты
from app.debug_utils import setup_debug_logging
import logging

# UI-виджеты
from app.widgets.viewer import ImageViewer
from app.widgets.left_tools import LeftToolPanel
from app.widgets.right_explorer import RightExplorer

# Контроллер (лёгкий)
from app.controllers.app_controller import AppController


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Saplings GUI (Safe Boot)")
        self.resize(1300, 800)

        self.viewer = ImageViewer()
        self.left = LeftToolPanel()
        self.right = RightExplorer()

        sp = QSplitter()
        sp.addWidget(self.left)
        sp.addWidget(self.viewer)
        sp.addWidget(self.right)
        sp.setStretchFactor(0, 0)
        sp.setStretchFactor(1, 1)
        sp.setStretchFactor(2, 0)
        self.setCentralWidget(sp)

        # Контроллер создаётся без тяжёлых зависимостей
        self.ctrl = AppController(det1_path='models/seedling.pt', det2_path='models/parts.pt')

        # wiring
        self._current_path = ''
        self._dlg_opening = False
        self.left.sig_open.connect(self._dialog_open)
        self.left.sig_process.connect(self._process)
        self.right.sig_file_selected.connect(self._open)
        self.right.sig_file_closed.connect(self._on_file_closed)
        self.ctrl.sig_overlay_ready.connect(self._show_overlay)
        self.ctrl.sig_status.connect(self.statusBar().showMessage)

        # опционально — калибровка 2 клика:
        # self.left.sig_calibrate.connect(self._start_calibration)
        # self.viewer.sig_click.connect(self._on_view_click)

    def _dialog_open(self):
        if self._dlg_opening:
            return
        self._dlg_opening = True
        QtCore.QMetaObject.invokeMethod(
            self, "_dialog_open_impl", QtCore.Qt.QueuedConnection
        )

    @QtCore.pyqtSlot()
    def _dialog_open_impl(self):
        try:
            options = QtWidgets.QFileDialog.Options()
            options |= QtWidgets.QFileDialog.DontUseNativeDialog
            p, _ = QtWidgets.QFileDialog.getOpenFileName(
                self,
                'Открыть',
                str(Path.home()),
                'Images (*.png *.jpg *.jpeg *.tif *.tiff)',
                options=options,
            )
            if p:
                self._open(Path(p))
        finally:
            self._dlg_opening = False

    def _open(self, path: Path):
        self.viewer.load_image(path)
        self._current_path = str(path)
        self.right.add_file(path)
        self.statusBar().showMessage(f"Открыт файл: {path}")

    def _process(self):
        if not self._current_path:
            QtWidgets.QMessageBox.information(self, "Saplings", "Сначала откройте изображение.")
            return
        self.ctrl.process_image(self._current_path)

    def _show_overlay(self, overlay_path: str):
        from PyQt5.QtGui import QPixmap
        self.viewer.set_pixmap(QPixmap(overlay_path))

    def _on_file_closed(self, path: Path):
        if self._current_path == str(path):
            self.viewer.clear()
            self._current_path = ''
            self.statusBar().showMessage("Файл закрыт")


def main():
    # включаем отладочное логирование и обработчик аварий
    log_file = setup_debug_logging()
    logging.debug("GUI starting; log file: %s", log_file)

    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("Fusion")
    palette = QtGui.QPalette()
    palette.setColor(QtGui.QPalette.Window, QtGui.QColor(53, 53, 53))
    palette.setColor(QtGui.QPalette.WindowText, QtCore.Qt.white)
    palette.setColor(QtGui.QPalette.Base, QtGui.QColor(25, 25, 25))
    palette.setColor(QtGui.QPalette.AlternateBase, QtGui.QColor(53, 53, 53))
    palette.setColor(QtGui.QPalette.ToolTipBase, QtCore.Qt.white)
    palette.setColor(QtGui.QPalette.ToolTipText, QtCore.Qt.white)
    palette.setColor(QtGui.QPalette.Text, QtCore.Qt.white)
    palette.setColor(QtGui.QPalette.Button, QtGui.QColor(53, 53, 53))
    palette.setColor(QtGui.QPalette.ButtonText, QtCore.Qt.white)
    palette.setColor(QtGui.QPalette.BrightText, QtCore.Qt.red)
    palette.setColor(QtGui.QPalette.Highlight, QtGui.QColor(142, 45, 197).lighter())
    palette.setColor(QtGui.QPalette.HighlightedText, QtCore.Qt.black)
    app.setPalette(palette)

    # ВАЖНО: временно без qt-material (может быть причиной падения)
    # try:
    #     from qt_material import apply_stylesheet
    #     apply_stylesheet(app, theme='dark_teal.xml')
    # except Exception:
    #     pass

    w = MainWindow()
    w.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
