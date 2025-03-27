



#-------------------------------




# ---- eof



id_to_delete    in list was null should not be
self.current_id  was null in caller should not be


deleteing 1132   now see 1133 in detail
        1132 no longer in history


        1132 still in list


        1132 gone from db

        list tab base reports it is deleted but still viaible
ListTabBase

/mnt/WIN_D/russ/0000/python00/python3/_projects/stuffdb/logs/app.py_log_deletestuff.log







        a_partial           = partial( self.do_ct_value, "" )
        self.ct_default     = a_partial



column_list

criteria_dict

SELECT   photo.id,  photo.name,  photo.title,  photo.add_kw, photo.descr    FROM photo

     ORDER BY  dt_item ASC






- DEBUG - PictureViewer Failed to load image pixmap is null
2025-03-26 10:34:13,826 - DEBUG - PictureViewer display_file error     file_name = '' file_exists = False
2025-03-26 10:34:13,828 - DEBUG - ListTabBase_delete_row_by_id




======================================================================
from PyQt5.QtCore import QSortFilterProxyModel, Qt
from PyQt5.QtGui import QStandardItem, QStandardItemModel
from PyQt5.QtWidgets import QApplication, QTableView


class CustomFilterProxyModel(QSortFilterProxyModel):
    def __init__(self, rows_to_hide=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Store the list of row indices to hide
        self.rows_to_hide = rows_to_hide if rows_to_hide is not None else []

    # Custom filtering method to hide specific rows
    def filterAcceptsRow(self, source_row, source_parent):
        # Hide the row if its index is in the rows_to_hide list
        return source_row not in self.rows_to_hide

    # Method to update the list of rows to hide
    def setRowsToHide(self, rows):
        self.rows_to_hide = rows
        self.invalidateFilter()  # Reapply the filter to update the view

app = QApplication([])

# Create a simple QAbstractTableModel (for demo, using QStandardItemModel)
model = QStandardItemModel(5, 2)
for row in range(5):
    for col in range(2):
        item = QStandardItem(f"Item {row},{col}")
        model.setItem(row, col, item)

# Set up a proxy model to filter rows
proxy_model = CustomFilterProxyModel()

# Provide a list of rows to hide
rows_to_hide = [1, 3]  # Hide row indices 1 and 3
proxy_model.setRowsToHide(rows_to_hide)

# Set the source model for the proxy
proxy_model.setSourceModel(model)

# Create a QTableView and set the proxy model
view = QTableView()
view.setModel(proxy_model)
view.show()

app.exec_()
