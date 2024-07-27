
"""
pretty sure never worked
"""


# ---- imports

from PyQt5.QtSql import QSqlQuery, QSqlQueryModel
from PyQt5.QtCore import Qt, QModelIndex

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableView, QVBoxLayout, QWidget, QMessageBox
from PyQt5.QtSql import QSqlDatabase, QSqlQueryModel, QSqlQuery, QSqlError
from PyQt5.QtCore import Qt
# ----QtWidgets
from PyQt5.QtWidgets import (
    QWidget,
    QPushButton,
    QAction,
    QDateEdit,
    QMenu,
    QAction,
    QLineEdit,
    QActionGroup,
    QApplication,
    QDockWidget,
    QTabWidget,
    QLabel,
    QListWidget,
    QMainWindow,
    QMessageBox,
    QSpinBox,
    QMdiSubWindow,
    QTextEdit,
    QButtonGroup,
    )




class CustomSqlQueryModel(QSqlQueryModel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.additional_row = []
        self.deleted_rows = set()# ----QtWidgets big
        from PyQt5.QtWidgets import (
            QAction,
            QMenu,
            QApplication,
            QMainWindow,
            QToolBar,
            QTableView,
            QFrame,
            QMainWindow,
            QMdiArea,
            QMdiSubWindow,
            QMdiArea,
            QMdiSubWindow,
            )

    def addRow(self, row_data):
        self.additional_row = row_data
        self.layoutChanged.emit()
        print( "add row complete")

    def deleteRow(self, row):
        if row < super().rowCount():
            self.deleted_rows.add(row)
        elif row == super().rowCount():
            self.additional_row = []
        self.layoutChanged.emit()

    def rowCount(self, parent=None):
        count = super().rowCount(parent)
        count -= len(self.deleted_rows)
        if self.additional_row:
            count += 1
        return count

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid() or role != Qt.DisplayRole:
            return None

        if index.row() in self.deleted_rows:
            return None

        if index.row() < super().rowCount():
            actual_row = index.row()
            for deleted_row in sorted(self.deleted_rows):
                if actual_row >= deleted_row:
                    actual_row += 1
            if actual_row >= super().rowCount():
                return None
            return super().data(self.index(actual_row, index.column()), role)
        elif index.row() == super().rowCount():
            return self.additional_row[index.column()]
        return None

# # Your SQL query
# sql = """
#     SELECT
#       photo.name,
#       photo.photo_fn,
#       photo.id,
#       photoshow.name,
#       photoshow.id
#     FROM   photo
#     JOIN   photoshow_photo
#     ON     photoshow_photo.photo_id = photo.id
#     JOIN   photoshow
#     ON     photoshow.id = photoshow_photo.photoshow_id
#     WHERE  photoshow.id = :id;
# """

# # Set up the query
# query = QSqlQuery()
# query.prepare(sql)

# # Create and set up the model
# model = CustomSqlQueryModel()
# model.setQuery(query)

# # Add a custom row to the model
# custom_row_data = ["Custom Name", "Custom Photo Fn", -1, "Custom Show Name", -1]
# model.addRow(custom_row_data)

# # Example code to delete a row from the model
# model.deleteRow(0)  # Deletes the first row from the model

# # Set the model to a QTableView
# tableView = QTableView()
# tableView.setModel(model)



class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self._build_gui()

   # def _setup_model(self):


    def _build_gui(self):
        self.setWindowTitle('Photo Viewer')

        # Create a widget for the window contents
        self.widget = QWidget()
        self.setCentralWidget(self.widget)

        # Set up the layout
        self.layout = QVBoxLayout()
        self.widget.setLayout(self.layout)

        # Create and set up the table view
        self.table_view = QTableView()
        self.layout.addWidget(self.table_view)

        button_layout    = self.layout



        # Set up the database connection
        self.db = QSqlDatabase.addDatabase('QSQLITE')
        self.db.setDatabaseName('/mnt/WIN_D/Russ/0000/python00/python3/_projects/stuff_db_qt/data/appdb.db')

        if not self.db.open():
            QMessageBox.critical(self, "Database Error", self.db.lastError().text())
            return

        # Set up the model
        self.model = CustomSqlQueryModel()

        # Set the query
        query = """
            SELECT
              photo.name as photo_name,
              photo.photo_fn,
              photo.id as photo_id,
              photoshow.name as photoshow_name,
              photoshow.id as photoshow_id
            FROM   photo
            JOIN   photoshow_photo
            ON     photoshow_photo.photo_id = photo.id
            JOIN   photoshow
            ON     photoshow.id = photoshow_photo.photoshow_id
            WHERE  photoshow.id = 29;
        """
        self.model.setQuery(query, self.db)

        if self.model.lastError().isValid():
            QMessageBox.critical(self, "Query Error", self.model.lastError().text())
        else:
            # Set the model to the view
            self.table_view.setModel(self.model)
            self.table_view.setEditTriggers(QTableView.DoubleClicked)  # Enable editing on double-click
            self.table_view.doubleClicked.connect(self.edit_item)

        a_widget         = QPushButton( "add" )
        # connect_to      = functools.partial( self.select_by_id,
        #                                       29  )
        connect_to   = self.model.addRow
        a_widget.clicked.connect(  connect_to )
        button_layout.addWidget( a_widget )


    def edit_item(self, index):
        if not index.isValid():
            return

        # Get the data for the selected row
        photo_id = self.model.data(self.model.index(index.row(), 2))
        photoshow_id = self.model.data(self.model.index(index.row(), 4))
        column_name = self.model.headerData(index.column(), Qt.Horizontal)

        new_value, ok = self.get_new_value(column_name, self.model.data(index))
        if ok:
            self.update_database(photo_id, photoshow_id, column_name, new_value)

    def get_new_value(self, column_name, current_value):
        from PyQt5.QtWidgets import QInputDialog
        return QInputDialog.getText(self, f"Edit {column_name}", f"New value for {column_name}:", text=str(current_value))

    def update_database(self, photo_id, photoshow_id, column_name, new_value):
        query = QSqlQuery(self.db)
        if column_name == "photo_name":
            query.prepare("UPDATE photo SET name = ? WHERE id = ?")
            query.addBindValue(new_value)
            query.addBindValue(photo_id)
        elif column_name == "photo_fn":
            query.prepare("UPDATE photo SET photo_fn = ? WHERE id = ?")
            query.addBindValue(new_value)
            query.addBindValue(photo_id)
        elif column_name == "photoshow_name":
            query.prepare("UPDATE photoshow SET name = ? WHERE id = ?")
            query.addBindValue(new_value)
            query.addBindValue(photoshow_id)
        else:
            return  # If the column is not editable, return early

        if not query.exec():
            QMessageBox.critical(self, "Update Error", query.lastError().text())
        else:
            self.model.setQuery(self.model.query().executedQuery())   # Refresh the model



if __name__ == '__main__':
    app = QApplication( [] )
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

