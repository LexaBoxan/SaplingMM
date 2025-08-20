from __future__ import annotations

from pathlib import Path

from PyQt5 import QtCore, QtWidgets


class RightExplorer(QtWidgets.QWidget):
    """Проводник файлов на основе QFileSystemModel."""

    sig_file_selected = QtCore.pyqtSignal(object)  # Path

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumWidth(260)
        layout = QtWidgets.QVBoxLayout(self)

        self.model = QtWidgets.QFileSystemModel(self)
        self.model.setRootPath(str(Path.home()))
        self.model.setNameFilters(["*.png", "*.jpg", "*.jpeg", "*.tif", "*.tiff"])
        self.model.setNameFilterDisables(False)

        self.view = QtWidgets.QTreeView(self)
        self.view.setModel(self.model)
        self.view.setRootIndex(self.model.index(str(Path.home())))
        self.view.setAlternatingRowColors(True)
        self.view.setStyleSheet(
            "QTreeView {background-color:#2b2b2b;color:#f0f0f0;}"
            "QHeaderView::section {background-color:#333;color:#f0f0f0;}"
        )
        self.view.doubleClicked.connect(self._on_dbl_click)

        layout.addWidget(self.view)

    # ------------------------------------------------------------------
    def _on_dbl_click(self, index: QtCore.QModelIndex):
        path = Path(self.model.filePath(index))
        if path.is_file():
            self.sig_file_selected.emit(path)

