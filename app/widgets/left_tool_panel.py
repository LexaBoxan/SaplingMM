from __future__ import annotations
from PyQt5 import QtCore, QtWidgets


class LeftToolPanel(QtWidgets.QWidget):
    """
    Левая панель инструментов.
    Сигналы:
      - sig_open: открыть файл
      - sig_calibrate: начать калибровку
      - sig_process: запустить обработку
      - sig_save_overlay: сохранить overlay (опц.)
    """
    sig_open = QtCore.pyqtSignal()
    sig_calibrate = QtCore.pyqtSignal()
    sig_process = QtCore.pyqtSignal()
    sig_save_overlay = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._build_ui()

    def _build_ui(self):
        self.setMinimumWidth(220)
        layout = QtWidgets.QVBoxLayout(self)

        self.btn_open = QtWidgets.QPushButton("Открыть изображение")
        self.btn_calibrate = QtWidgets.QPushButton("Калибровка (2 клика)")
        self.btn_process = QtWidgets.QPushButton("Обработать")
        self.btn_save = QtWidgets.QPushButton("Сохранить overlay")

        # примеры доп. настроек
        self.step_label = QtWidgets.QLabel("Шаг сетки (мм):")
        self.step_mm = QtWidgets.QDoubleSpinBox()
        self.step_mm.setDecimals(1)
        self.step_mm.setRange(0.1, 50.0)
        self.step_mm.setValue(5.0)

        self.conf_label = QtWidgets.QLabel("conf:")
        self.conf_spin = QtWidgets.QDoubleSpinBox()
        self.conf_spin.setDecimals(2)
        self.conf_spin.setRange(0.05, 0.99)
        self.conf_spin.setValue(0.25)

        self.iou_label = QtWidgets.QLabel("iou:")
        self.iou_spin = QtWidgets.QDoubleSpinBox()
        self.iou_spin.setDecimals(2)
        self.iou_spin.setRange(0.10, 0.99)
        self.iou_spin.setValue(0.45)

        layout.addWidget(self.btn_open)
        layout.addSpacing(8)
        layout.addWidget(self.step_label)
        layout.addWidget(self.step_mm)
        layout.addWidget(self.btn_calibrate)
        layout.addSpacing(8)
        layout.addWidget(self.conf_label)
        layout.addWidget(self.conf_spin)
        layout.addWidget(self.iou_label)
        layout.addWidget(self.iou_spin)
        layout.addSpacing(8)
        layout.addWidget(self.btn_process)
        layout.addSpacing(8)
        layout.addWidget(self.btn_save)
        layout.addStretch()

        # сигнализация
        self.btn_open.clicked.connect(self.sig_open)
        self.btn_calibrate.clicked.connect(self.sig_calibrate)
        self.btn_process.clicked.connect(self.sig_process)
        self.btn_save.clicked.connect(self.sig_save_overlay)

    # удобные геттеры для параметров
    def get_grid_step_mm(self) -> float:
        return float(self.step_mm.value())

    def get_conf(self) -> float:
        return float(self.conf_spin.value())

    def get_iou(self) -> float:
        return float(self.iou_spin.value())
