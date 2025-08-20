from __future__ import annotations

from pathlib import Path
from typing import Dict

from PyQt5 import QtCore, QtWidgets


class RightExplorer(QtWidgets.QWidget):
    """Правая панель: список открытых изображений."""

    sig_file_selected = QtCore.pyqtSignal(object)  # Path
    sig_file_closed = QtCore.pyqtSignal(object)  # Path

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumWidth(260)
        layout = QtWidgets.QVBoxLayout(self)

        self.tree = QtWidgets.QTreeWidget(self)
        self.tree.setColumnCount(3)
        self.tree.setHeaderLabels(["ID", "Название", ""])
        header = self.tree.header()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
        self.tree.setAlternatingRowColors(True)
        self.tree.setStyleSheet(
            "QTreeWidget {background-color:#2b2b2b;color:#f0f0f0;}"
            "QHeaderView::section {background-color:#333;color:#f0f0f0;}"
        )

        layout.addWidget(self.tree)

        self._items: Dict[Path, QtWidgets.QTreeWidgetItem] = {}
        self.tree.itemSelectionChanged.connect(self._on_sel)

    # ------------------------------------------------------------------
    def add_file(self, path: Path):
        """Добавить файл в дерево."""
        if path in self._items:
            self.tree.setCurrentItem(self._items[path])
            return

        row_id = self.tree.topLevelItemCount() + 1
        item = QtWidgets.QTreeWidgetItem([str(row_id), path.name])
        self.tree.addTopLevelItem(item)

        btn = QtWidgets.QToolButton()
        btn.setIcon(self.style().standardIcon(QtWidgets.QStyle.SP_TitleBarCloseButton))
        btn.setAutoRaise(True)
        btn.clicked.connect(lambda _, i=item: self._remove_item(i))
        self.tree.setItemWidget(item, 2, btn)

        self._items[path] = item
        self.tree.setCurrentItem(item)

    # ------------------------------------------------------------------
    def _on_sel(self):
        items = self.tree.selectedItems()
        if not items:
            return
        item = items[0]
        for path, it in self._items.items():
            if it is item:
                self.sig_file_selected.emit(path)
                break

    # ------------------------------------------------------------------
    def _remove_item(self, item: QtWidgets.QTreeWidgetItem):
        path = None
        for p, it in list(self._items.items()):
            if it is item:
                path = p
                del self._items[p]
                break
        if path is None:
            return
        idx = self.tree.indexOfTopLevelItem(item)
        self.tree.takeTopLevelItem(idx)
        self._renumber()
        self.sig_file_closed.emit(path)

    # ------------------------------------------------------------------
    def _renumber(self):
        for i in range(self.tree.topLevelItemCount()):
            it = self.tree.topLevelItem(i)
            it.setText(0, str(i + 1))

