#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# ---- tof

"""
by cursor and russ, to replace table model
Table model: five columns — int, str, str, int, int (indices 0–4).

Typical use: picture id, subject text, other text, plus two integer fields.
"""

from qtpy.QtCore import QAbstractTableModel, QModelIndex, Qt


class PictureSubjectOtherTableModel(QAbstractTableModel):
    """
    QAbstractTableModel with columns by index:

        0 — int   id
        1 — str   table
        2 — str   topic
        3 — int   source  an id
        4 — int   ts

    Each row is a 5-tuple ``(int, str, str, int, int)``.
    """

    COLUMN_COUNT = 5

    _HEADERS = ("Picture", "Subject", "Other", "Int A", "Int B")

    def __init__(self, rows=None, parent=None):
        super().__init__(parent)
        self._rows = list(rows) if rows is not None else []

    def rowCount(self, parent=QModelIndex()):
        if parent.isValid():
            return 0
        return len(self._rows)

    def columnCount(self, parent=QModelIndex()):
        if parent.isValid():
            return 0
        return self.COLUMN_COUNT

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid():
            return None
        row, col = index.row(), index.column()
        if row < 0 or row >= len(self._rows) or col < 0 or col >= self.COLUMN_COUNT:
            return None

        value = self._rows[row][col]

        if role in (Qt.DisplayRole, Qt.EditRole, Qt.ToolTipRole):
            return value

        return None

    # ------------------------------
    def setData(self, index, value, role=Qt.EditRole):
        if not index.isValid() or role != Qt.EditRole:
            return False
        row, col = index.row(), index.column()
        if row < 0 or row >= len(self._rows) or col < 0 or col >= self.COLUMN_COUNT:
            return False

        row_data = list(self._rows[row])
        try:
            if col in (0, 3, 4):
                row_data[col] = int(value)
            else:
                row_data[col] = str(value)
        except (TypeError, ValueError):
            return False

        self._rows[row] = tuple(row_data)
        self.dataChanged.emit(index, index, [Qt.DisplayRole, Qt.EditRole])
        return True

    # ------------------------------
    def flags(self, index):
        if not index.isValid():
            return Qt.ItemIsEnabled
        return (
            Qt.ItemIsSelectable
            | Qt.ItemIsEnabled
            | Qt.ItemIsEditable
        )

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role != Qt.DisplayRole:
            return None
        if orientation == Qt.Horizontal and 0 <= section < self.COLUMN_COUNT:
            return self._HEADERS[section]
        if orientation == Qt.Vertical:
            return section + 1
        return None

    # ------------------------------
    def insertRows(self, row, count, parent=QModelIndex()):
        if parent.isValid() or count < 1:
            return False
        if row < 0:
            row = 0
        if row > len(self._rows):
            row = len(self._rows)

        self.beginInsertRows(parent, row, row + count - 1)
        default_row = (0, "", "", 0, 0)
        for _ in range(count):
            self._rows.insert(row, default_row)
        self.endInsertRows()
        return True

    # ------------------------------
    def removeRows(self, row, count, parent=QModelIndex()):
        if parent.isValid() or count < 1 or row < 0 or row >= len(self._rows):
            return False
        last = min(row + count - 1, len(self._rows) - 1)
        self.beginRemoveRows(parent, row, last)
        del self._rows[row : last + 1]
        self.endRemoveRows()
        return True

    # ------------------------------
    def set_rows(self, rows):
        """Replace all rows; each element must be a 5-tuple matching column types."""
        self.beginResetModel()
        self._rows = [tuple(r) for r in rows]
        self.endResetModel()

    # ------------------------------
    def rows(self):
        """Return a shallow copy of row tuples."""
        return list(self._rows)

    # ------------------------------
