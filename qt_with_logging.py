#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ---- tof

"""

On advice of chat  --- not sure worth keeping --- or work ??

Created on Sun Aug 11 17:23:25 2024
chat with hellp from russ

This method still relies on the capabilities of the QSqlDriver and might not capture all internal operations depending on the driver and database being used.
For more comprehensive logging, you might need to consider enabling query logging on the database server itself.
If your database driver supports SQL tracing (setTracingEnabled), this feature
is temporarily enabled during the submitAll call to capture all SQL operations.

import   qt_with_logging
model             = qt_with_logging.QSqlTableModelWithLogging( self, self.db  )


qt_with_logging.QSqlTableModelWithLogging(    )
qt_with_logging.QSqlRelationalTableModelWithLogging()


unclear on how well this works -- keep trying for awhile





"""
# ---- imports

from qt_compat import QApplication, QAction, exec_app, qt_version
from PyQt.QtWidgets import QMainWindow, QToolBar, QMessageBox



from PyQt.QtCore import Qt
# ---- QtSql
from PyQt.QtSql import (QSqlDatabase,
                         QSqlDriver,
                         QSqlError,
                         QSqlField,
                         QSqlQuery,
                         QSqlQueryModel,
                         QSqlRecord,
                         QSqlRelation,
                         QSqlRelationalDelegate,
                         QSqlRelationalTableModel,
                         QSqlTableModel)

import logging
# ---- end imports

LOG_LEVEL   = 30    # higher is more
logger      = logging.getLogger( )

# logging code incompletee


class QSqlTableModelWithLoggingxxx(QSqlTableModel):
    """
    from chat
    """
    def __init__(self, parent=None, db=None):
           # Call the parent class constructor
           super().__init__(parent, db)

    def submitAll(self):
        # Track before calling the base method
        db = self.database()
        driver = db.driver()

        # Enable tracing if supported
        if hasattr(driver, 'setTracingEnabled'):
            driver.setTracingEnabled(True)

        # Call the original submitAll method
        result = super().submitAll()

        # Track the last executed query
        if driver.hasFeature(driver.LastQuery):
            query = QSqlQuery(db)
            last_query    = query.lastQuery()
            bound_values  = query.boundValues()
            print( f"Executed Query during submitAll:  {last_query = } ")
            print( f"With Bound Values:   {bound_values = } ")

        # Disable tracing if it was enabled
        if hasattr(driver, 'setTracingEnabled'):
            driver.setTracingEnabled(False)

        return result

    def select(self):
        # Same as before for select method logging -- which seems not to work
        query = QSqlQuery(self.database())
        success = super().select()
        if success:
            last_query     = query.lastQuery()
            bound_values   = query.boundValues()
            # ?? not getting any info from next
            #rint("Executed Query during select: ", last_query, )
            #rint("With Bound Values: ", bound_values)
        return success

class QSqlTableModelWithLogging(QSqlTableModel):
    def __init__(self, parent=None, db=None):
        """
        basically seems not to work  --- not sure can be made to work
            features needed just may not be present


        import   qt_with_logging
        = qt_with_logging.QSqlTableModelWithLogging( )

        Args:
            parent (TYPE, optional): DESCRIPTION. Defaults to None.
            db (TYPE, optional): DESCRIPTION. Defaults to None.

        Returns:
            None.

        """
        # Call the parent class constructor
        super().__init__(parent, db)

    def submitAll(self):
        """
        an override trying to add logging but
        does not seem to work and having trouble
        debugging into it


        """
        # Get the database and query
        db = self.database()

        # Optionally, enable SQL tracing here (driver dependent)
        # driver = db.driver()
        # if hasattr(driver, 'setTracingEnabled'):
        #     driver.setTracingEnabled(True)

        # Call the original submitAll method
        result = super().submitAll()

        # Access the last executed query through the database's last query
        query         = QSqlQuery( db )
        last_query    = query.lastQuery()
        bound_values  = query.boundValues()


        print( f"submitAllExecuted Query during submitAll:  {last_query = } ")
        print( f"submitAllWith Bound Values:   {bound_values = } ")

        #query = model.query()
        if query.lastError().isValid():
            print(f"submitAllError: {query.lastError().text()}")
        else:
            print(f"submitAll Last Query: {query.lastQuery()}")



        # Optionally, disable SQL tracing here
        # if hasattr(driver, 'setTracingEnabled'):
        #     driver.setTracingEnabled(False)

        return result

    def select(self):
        query = QSqlQuery(self.database())
        success = super().select()
        if success:
            last_query      = query.lastQuery()
            bound_values    = query.boundValues()

            print( f"select Executed Query during submitAll:  {last_query = } ")
            print( f"select With Bound Values:   {bound_values = } ")

        return success

# # Usage
# model = LoggingQSqlTableModel(self)
# model.setTable("your_table_name")
# model.select()

# # Make some changes to the model and call submitAll to trigger logging
# model.submitAll()



# # Usage
# model = LoggingQSqlTableModel(self)
# model.setTable("your_table_name")
# model.select()

# # Make some changes to the model and call submitAll to trigger logging
# model.submitAll()



class QSqlRelationalTableModelWithLogging( QSqlRelationalTableModel ):
    """
    from chat
        use in place of QSqlRelationalTableModel for tracking sql
        not sure if works
    """
    def __init__(self, *args, **kwargs):
        """
        tbd, for now read
        """
        super().__init__(*args, **kwargs)

    def select(self):
        """
        tbd, for now read
        """
        debug_msg = (f"QSqlRelationalTableModelWithLogging.select SQL select: {self.selectStatement()}")
        logging.log( LOG_LEVEL,  debug_msg, )

        return super().select()

    def insertRowIntoTable(self, record):
        """
        tbd, for now read
        """
        query   = self.database().driver().sqlStatement(QSqlDriver.InsertStatement,
                                                         self.tableName(), record, False)
        debug_msg = (f"QSqlRelationalTableModelWithLogging SQL insertRowIntoTable: {query}")
        logging.log( LOG_LEVEL,  debug_msg, )

        return super().insertRowIntoTable(record)

    def updateRowInTable(self, row, record):
        """
        tbd, for now read
        """
        query = self.database().driver().sqlStatement(QSqlDriver.UpdateStatement, self.tableName(), record, False)
        print(f"SQL updateRowInTable : {query}")
        return super().updateRowInTable(row, record)

    def deleteRowFromTable(self, row):
        """
        tbd, for now read
        """
        query = self.database().driver().sqlStatement(QSqlDriver.DeleteStatement, self.tableName(), QSqlRecord(), False)
        print(f"SQL deleteRowFromTable: {query}")
        return super().deleteRowFromTable(row)


"""
!! russ set this up
from PyQt.QtSql import QSqlDatabase, QSqlQuery
from PyQt.QtCore import Qt

# Assuming db is your QSqlDatabase connection
db = QSqlDatabase.addDatabase('QSQLITE')
db.setDatabaseName('your_database_name.db')
db.open()

model = QSqlTableModel(self, db)
model.setTable("your_table_name")
model.select()

# Tracking SQL query and parameters
query = QSqlQuery(db)
last_query = query.lastQuery()
bound_values = query.boundValues()

print("Last Query: ", last_query)
print("Bound Values: ", bound_values)

"""