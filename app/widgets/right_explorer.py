from __future__ import annotations
from pathlib import Path
from PyQt5 import QtCore, QtWidgets


class RightExplorer(QtWidgets.QWidget):
    """
    Правая панель: проводник файлов.
    Показывает дерево, сигналит выбранный файл.
    """
    sig_file_selected = QtCore.pyqtSignal(object)  # Path

    def __init__(self, root_path: Path | None = None, parent=None):
        super().__init__(parent)
        self.setMinimumWidth(260)
        layout = QtWidgets.QVBoxLayout(self)

        self.model = QtWidgets.QFileSystemModel(self)
        self.model.setRootPath(str(root_path or Path.home()))
        self.model.setNameFilters(["*.png", "*.jpg", "*.jpeg", "*.tif", "*.tiff"])
        self.model.setNameFilterDisables(False)

        self.view = QtWidgets.QTreeView(self)
        self.view.setModel(self.model)
        self.view.setRootIndex(self.model.index(str(root_path or Path.home())))
        self.view.setColumnWidth(0, 220)
        for c in range(1, 4):  # спрячем лишние столбцы
            self.view.setColumnHidden(c, True)

        layout.addWidget(self.view)

        self.view.selectionModel().selectionChanged.connect(self._on_sel)

    def _on_sel(self, *_):
        idxs = self.view.selectionModel().selectedIndexes()
        if not idxs:
            return
        idx = idxs[0]
        path = Path(self.model.filePath(idx))
        # отдаём только файлы картинок
        if path.is_file() and path.suffix.lower() in {".png", ".jpg", ".jpeg", ".tif", ".tiff"}:
            self.sig_file_selected.emit(path)
