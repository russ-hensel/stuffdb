
SELECT   help_info.id,  help_info.title,  help_info.system, help_info.key_words    FROM help_info
    INNER JOIN  help_key_word  ON help_info.id = help_key_word.id
    WHERE  lower(help_info.system = "powerbuilder"  AND   key_word IN ( "testxxx" )
    GROUP BY   help_info.id,  help_info.title,  help_info.system, help_info.key_words
    HAVING  count(*) = 1
     ORDER BY  lower(help_info.title) ASC

these all work

SELECT   help_info.id,  help_info.title,  help_info.system, help_info.key_words    FROM help_info
    WHERE   help_info.system = "Java"
     ORDER BY  lower(help_info.title) ASC


SELECT   help_info.id,  help_info.title,  help_info.system, help_info.key_words    FROM help_info
    WHERE  lower( help_info.system ) = "java"
     ORDER BY  lower(help_info.title) ASC

SELECT   help_info.id,  help_info.title,  help_info.system, help_info.key_words    FROM help_info
    WHERE  lower( help_info.system ) = "powerbuilder"
     ORDER BY  lower(help_info.title) ASC

SELECT   help_info.id,  help_info.title,  help_info.system, help_info.key_words    FROM help_info
    WHERE  lower( help_info.system ) = "powerbuilder"
     ORDER BY  lower(help_info.title) ASC

--- seemed not to work
SELECT   help_info.id,  help_info.title,  help_info.system, help_info.key_words    FROM help_info
    WHERE  lower(help_info.system = "powerbuilder"
     ORDER BY  lower(help_info.title) ASC

    WHERE  lower(help_info.system = "powerbuilder"
    WHERE  lower( help_info.system ) = "powerbuilder"
---------------
SELECT   people.id,  people.l_name,  people.f_name, people.add_kw    FROM people
    WHERE lower( f_name )  like "%ru%"




I would like to add to this select

    select
    photo_subject.id,
	photo_subject.photo_id,
	photo_subject.table_id,
	photo_subject.table_joined,

    FROM photo_subject
    WHERE  photo_subject.table_joined  = "people"

to join to a table people


CREATE TABLE people   (
	id    			INTEGER,
	id_old          VARCHAR(15),
	add_kw        	VARCHAR(50),
	descr 			VARCHAR(50)
    )

using photo_subject.table_id  = people.id





print(f"Date: {date_obj}")
print(f"Datetime: {datetime_obj}")




I have


class SendSignals( QObject ):

    topic_update_signal = pyqtSignal(str, int, str )

    def send_topic_update(self, table, table_id, info):
        print( "send_topic_update emit next")
        self.topic_update_signal.emit( table, table_id, info )


and

in Class X  __init__

    send_signals  = mdi_management.SendSignals()
    send_signals.topic_update_signal.connect( self.topic_update )

and finally in Class X

   def topic_update( self,   table, table_id,  info, ):

       print( f"got topic update {table = } {table_id = } {info = }")

but while i call send_topic_update it does not seem to be
recieved by topic_update.

Any idea why?  Should I be using a @slot decorator?


def two_way_to_remove_mapper():


    # Disconnect the mapper from the model
    self.mapper.setModel( None )


    # Clear the mappings
    self.mapper.clearMapping()

    # Optionally, clear any custom delegate
    self.mapper.setItemDelegate(None)





from PyQt5.QtCore import QObject, pyqtSignal


class MDI(QObject):
    # Define a custom signal with arguments
    update_signal = pyqtSignal(str, int, dict)

    def send_update(self, table, table_id, info):
        # Emit the signal when needed
        self.update_signal.emit(table, table_id, info)

class PicSubject(QObject):
    def __init__(self):
        super().__init__()
        # Connect the signal to the slot
        mdi = MDI()
        mdi.update_signal.connect(self.topic_update)

    def topic_update(self, table, table_id, info):
        # Handle the update signal
        print(f"Received update: table={table}, table_id={table_id}, info={info}")

# Example usage
mdi = MDI()
pic_subject = PicSubject()
mdi.send_update("photo_table", 101, {"description": "Updated photo"})


class PicSubject(QObject):
    def __init__(self):
        super().__init__()
        # Connect the signal to the slot
        mdi = MDI()
        mdi.update_signal.connect(self.topic_update)

    def topic_update(self, table, table_id, info):
        # Handle the update signal
        print(f"Received update: table={table}, table_id={table_id}, info={info}")








view.setSelectionBehavior(QTableView.SelectRows)  # For row selection
view.setSelectionBehavior(QTableView.SelectColumns)  # For column selection






i want to

pub.sendMessage( TOPIC_UPDATE,  table, table_id, info   )

in another part of the program how to I subscribe to this
message and what sort of function is needed.
-------------------



in a mdi_management module an object say MDI sends a message with:

pub.sendMessage( TOPIC_UPDATE,  table = table, table_id = table_id, info = info   )

in a picture_document module an object say PicSubject
it trys to subscribe with:

pub.subscribe( self.topic_update, mdi_management.TOPIC_UPDATE )

and
PicSubject has a method

def topic_update( self,   table, table_id,  info  ):
    .....


but i get an error:

ListenerMismatchError: Listener "PictureSubjectSubTab.topic_update" (from module "picture_document") inadequate: needs to accept 2 more args (arg2, arg1)

how do i fix this?


---------------

i changed my subscriber to

def topic_update( self,    *args, **kwargs ):

but when i use:

pub.sendMessage( TOPIC_UPDATE,  table = table, table_id = table_id, info = info   )

it complains

SenderMissingReqdMsgDataError: Some required args missing in call to sendMessage('topic_update', table,table_id,info): arg1

and by the way what is arg1?






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
