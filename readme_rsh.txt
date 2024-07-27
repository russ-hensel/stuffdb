

====chat
====stuff
====Tech
====Versions

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

====Tech
main    - > stuff_db_qt  --> stuff_db_main_window --> document_maker

                             midi_management
====stuff


    >>  cd /mnt/WIN_D/Russ/0000/python00/python3/_projects/qt5_book/ex_1.ui

    >>  conda activate py_10_scrape
most outer window
    stuff_outer.ui
    >>  pyuic5 stuff_outer.ui -o stuff_outer.py


=========== own orm

    name of primary updatable table
    dict for all columns, key is full column name
    sql for select may be join....
    primary id for table -- always id?

    for each record ( by id ) layout id
    for each column\
        id     -- track is from select or new ( insert or update, or delete  )
        select_value of column
        current_value  --- managed by system
        window field
        db type
        convert to field function
        convert from field function


    can we find a field by name in a layout




====Versions


--- ver19    ----- move on do a big delete
    why:
        help beginning to work, do some more delete

     more
        ** delete the dead again including channel -- stuff in stuff
        *! get help on one tab, make second tab have no fields, then do not place
                just have to remove tab, pretty much comment out a few lines

        ** history messed up, filter at end of select removed, now seems ok
        ** photo fails to show photo, this seems to be missing in select
           self.parent_window.display_photo( self.photo_fn_field.text( ) )
           we can add this may need override ant extend or not
           >>>> this is it, photo a sort of field record to field  may be place in descandant

        !! history update on click on row, but not on prior next perhaps move all to
              record_to_field -- but history would update it self, maybe that is ok
              or ok for now

        !! prior next no good in photo_show throwing an error, fix this

        *! stuff sub tab may need or not need an anceston but not the tab one
           this should wait

        *! stuff add - save not working, is any add-save working, look around
            and fix  -- but new test below says ok


        *! testing add - save
            photos   3003    -- is ok
            stuff     10     -- is ok
            help      id missing on window -- fix first -- now there but id does not show
            photo_show  bunch of issues, keep working on it

        !! put on github

        !! look into rework of add to history base on passing a dict.

--- ver18    ----- move on do a big delete
    why:
        move on, do a big delete

     more
        ** delete the dead
        ** spell check
        !! add ancestor for the text_tab --- move code to it
        ?? is it key words or add_key.....
        !! do a real help document = subwindow
            ** copy rename stuff
            ** finish db tables and 3 rows in each
            ** already had a key_gen entry
            !! help table missing timstamp fields, need to add and redo data
            ** remove stuff sub tabs
            ** stuff had some dead code already out of help but still in stuff
            ** looks like no change to document_maker because opens in same way as channel versigon

            4:50 first trial
            4:55 basically runs, with mucho bugs -- history not right -- go see if stuff history is ok

        *! review stuff document to new standards
                ** basics working other stuff still needs checking
                !! select from criteria not working
        !! also for photo show


--- ver17   ----- move on do a big delete
    why:
        most of crud works on photo --- less some important details
        and much promoted, backup and delete stuff


        **  saved fetched seems good, factoring out seems good
        *!  get saved new..... working --- ok but timestamp issues
        *!  promote save new to ancestor
        !!  next prior for list seems to not work on text




--- ver16
    why:
        lots of progress on photo ( and a bit on photo show )
        promote some to ancestors, clean up and
        continue to get save and new .... working on photo

        **  saved fetched seems good, factoring out seems good
        *!  get saved new..... working --- ok but timestamp issues
        !!  promote save new to ancestor
        !!  next prior for list seems to not work on text

    more

--- ver15
    why:
        stuff events works on fetch so a checkpoint

    more
        ^^ add -> save works on photo_text but not photo so convert photo to crud
        !! a key or id or a_id or a mix it is the key gen key might be value id column name
        !! add seems to add but will not save....
        !! add should on save add to history
        !! add in text if missing -- working on in photo_sub_window
        !! add labels to photo_sub window  detail
        get a criteria select working for $like$  may be some code around
        fill in from below:
        *! add a tab for one photo at a time -- add the prior next buttons to it
        *! some update code in place, second model one that updates
        *! get basics of photo show working
            !! select from criteria  just for %like%
            *! single photo tab
            *! better layout
        !! updates to detail -- may be some code from copy

        !! photoshow photos subtab basics working
            ** add from photo window
            !! delete from self

        ** remove channel and youtube stuff

--- ver14
    why:
        big struggle getting photos read only working, prior code thouth good
        was not AI cold not fix until along cam black_box.
        not finished the conversion but too much dead and dying code so
        a checkpoint

    more
        ** stuff events works on select
        *! add a tab for one photo at a time
        *! some update code in place, second model one that updates
        *! get basics of photo show working
            !! select from criteria
            *! single photo tab
            *! better layout
        !! updates to detail -- may be some code from copy

        !! photoshow photos subtab basics working
            ** add from photo window
            !! delete from self

        ** remove channel and youtube stuff


        just make model_
        self.query_model_read.addRow( row_list )
        self.query_model_read.layoutChanged.emit()


--- ver13
    why:
        photoshows now in existing but functionally incomplete, so checkpoint
        as we add features.

    more
        *! add a tab for one photo at a time
        *! some update code in place, second model one that updates
        *! get basics of photo show working
            !! select from criteria
            *! single photo tab
            !! better layout
        !! updates to detail -- may be some code from copy

        !! photoshow photos subtab basics working
            !! add from photo window
            !! delete from self

        !! remove channel and youtube stuff


        just make model_
        self.query_model_read.addRow( row_list )
        self.query_model_read.layoutChanged.emit()




--- ver12
    why:
        photoshows now in existing but functionally incomplete, so checkpoint
        as we add features.

    more:
        *! get basics of photo show working
            !! select from criteria
            ** photoshow photos subtab started
            *! single photo tab
                    !! better layout
                    ** display when clicked
                    ** display first if exists when show selected

            !! updates to detail -- may be some code from copy



        !! photoshow photos subtab basics working
            ** select
            !! add from photo window
            !! delete from self
            ** display clicked on photo


        !! remove channel and youtube stuff









--- ver11
    why:
        photo sort of works except for text ... so checkpoint
        and begin to work on shows a one to many -- inter document communication
        ** begin on photo show
            ** hand enter a bit of photoshow data
            ** define photoshow schema

    more:

        *! get basics of photo show working
            !! select from criteria
            ** photoshow photos subtab started
            !! single photo tab
            !! updates to detail -- may be some code from copy



        !! photoshow photos subtab basics working
            ** select
            !! add from photo window
            !! delete from self
            !! display clicked on photo


        ** stuff_db --- to stuffdb for main name of app


--- ver10
    why:
        lots of progress so a checkpoint
        ** lets add some photo stuff even though there is a lot to fix in old stuff
    more:
        ** get define db queries working
        ** move to __version__

--- ver09
    why:
        lots of progress so a checkpoint
        ** start adding stuff -- have windows with wrong table....
    more:
        *! have some of stuff and stuff_text defined and populated need more
        ** make list and detail work some
        !! get text working
        ** update -- now save on toolbar
        *! get menu caught up to toolbar
        !! get define db queries working
        !! make a select using link %%
        !* create_tab to _create_gui

        *! convert to stuff tables


--- ver08
    why:
        lots of progress so a checkpoint
        ** basic key gen seems to work
    and more:
        !! lots of dead to prune, but kept in ver07
        ** list -> detail basically works
        ** detail -> history basically works
        ** default and copy prior of detail basically works
        ** history -> detail basically works

    ** add text table and select..... on text tab
        ** channel_text say
        ** text_data
        default to blank if missing on detail fetch
        make sure saved
        ** create tab
        ** create database

--- ver07
    why:
        lots of progress so a checkpoint

    ** list and history navigation basically works
        !! do detail saves
        !! auto add to history on fetch of new id
        !! make sure prior and next select their rows

    !! start on timestamps
        add to db's
        add add_ts '

    !! add text table and select..... on text tab
        channel_text say
        text_data
        default to blank if missing on detail fetch
        make sure saved
        ** create tab
        ** create database


    !! improve about box
    ** size pos from parameters
    *! clean up dead and dying

    *! help is still channel, but has been broken
        into object that should be generalizerable

    ** add and implement toolbar with forward back, placeholders for some other
        ** forward in list -- and promoted, and simpler call method
        ** back
            !! forwarded and back do not fix history or save

--- ver06
    why:
        lots of progress a checkpoi9nt
        *! start help with text on second tab
        ** lots of test to call to active sub window


    *! help is still channel, but has been broken
        into object that should be generalizerable

    *! add and implement toolbar
        ** forward in list -- and promoted, and simpler call method
        ** back
        !! forwarded and back do not fix history or save


    ** get history working again
    ** click on history to detail



--- ver05  more
    why:
        !! start help with text on second tab
    ** get history working again
    ** click on history to detail


----ver05
    why: rename in channel model
        *!rename in channel model

    *! many prints to logging

        msg      = f"{ = }"
        AppGlobal.logger.debug( msg )
            #.error



    *! prior next for list
            !! need save
            !! needs init from click on list

    !! prior next on history
        !! shorten history, or do via max history in parms


    ** add history
    *! clean up dead and dying


----ver04
    ** add history
    *! clean up dead and dying

----ver03

    got some basic stuff tabs working, still no one to many on detail
    still no history
    lots of message box to change to logging
    lost of code from other apps much dead



====chat --- all moved to sub directory chat
====================================

"""
i am using qt designer (using qt 5.15.3)
I am trying to add a QMidiArea which works but
does not fill all of the main window.

Could you give me step by step directions
on how to do this in qt-designer ?

....py

"""

directions did not work, eliminate qt designer and just do code
================

"""
i am  using qt 5.15.3 and would like the code for a main window with:
* a midi area that fills the mainwindowtwo
* two sub windows with buttons
* two menus, each with two sub menus, one of which links to an about box.


chat_top_mdi_window.py

"""

==========================

"""
i am  using qt 5.15.3 with a main window and sub windows.
    What events are triggered when a sub window is closed.
    Are there any arguments for the event, and how do I make
    a function to process the event and arguments?

    chat_close_sub_window.py

"""




====================================

"""
i am using qt designer (using qt 5.15.3) but cannot find the workspace widget, can you tell me how to add it?

The QWorkspace class was deprecated in Qt 4 and has been removed in Qt 5.
If you're looking to manage multiple document interface (MDI) applications, you should use
QMdiArea instead. Here's how you can add a QMdiArea in Qt Designer:

chat_static_subwindow.py

"""


===========================

QMdiSubWindow

i am using qtdesigner (using qt 5.15.3) an have a main window with
a QMdiArea but qtdesigner does not have a QMdiSubWindow.  How
do i add it or otherwise deal with it?


-------------------

In Qt Designer, there isn't a QMdiSubWindow widget available directly in the widget box.
However, you can manage QMdiSubWindow pro grammatically after designing your main window.
Here's how you can add and manage QMdiSubWindow instances in your QMdiArea:


--------------------


====chat
====================================
"""
i am using   qt 5.15.3 ( which is installed ) where i have a QMenu object on my gui.
How do i dynamically add and delete menu items  to that object.

I would like to delete the menu item by title, and if possible
by some attribute I can capture when I add the menu item.

!
chat_add_menu_2.py
-------------------
"""
========================================
    """
How can I move the menus I create
ChatGPT
chat_move_menu.py




====================================
"""
i am using   qt 5.15.3 ( which is installed ) where I have a Main window.
I would like to add two notebooks each with 2 tabs.
The notebooks should appear one above the other.

chat_2_notebooks.py
-------------------
"""

====================

"""


I forgot to say the tab should be able to
updated rows, so I have changed my request
just a bit to include it.

Now I want:

I am using python qt 5.15.3) with an SQLite database.

the database has a table defined as:


CREATE TABLE channel (
    id       INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
    yt_id    VARCHAR( 40 ),
    name     VARCHAR( 40 ),
    url      VARCHAR( 100 ),
    mypref   INTEGER,
    mygroup  VARCHAR( 20 )

I would like a qtwindow with a tab.
On the tab should be a widgets for displaying
one row from the db, perhaps linked by
a  QDataWidgetMapper.

The tab should have 3 buttons so as to be able to:
    fetch a single row based on its id.
       and provide for its update
    delete a fetched row.
    create a new empty row
        and provide for its update

Can you create sample Python code for this?



chat_detail_db_subwindow.py

"""

=========================

"""

i am using  python with  qt 5.15.3 where i have  QMdiArea.
I would like to dynamically add a new subwindow to it.
The subwindow should have 5 widgets on it, not
all of the same type.  They should be laid out using
a grid as the layout manager




chat_subwindow_with_widgets.py
=========================


=========================

"""

chat_add_history.py


I am using  python with  qt 5.15.3 where i have  QMdiArea.

I also have a database and table:

CREATE TABLE channel (
    id       INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
    yt_id    VARCHAR( 40 ),
    name     VARCHAR( 40 ),
    url      VARCHAR( 100 ),
    mypref   INTEGER,
    mygroup  VARCHAR( 20 )

On one subwindow I would like to have a
list of all the rows in the database ( using a QSqlTableModel).

I would like a second subwindow with a display similar to the QSqlTableModel,
but only with the id and name from the database,
perhaps a second QSqlTableModel.
I would like to be able  to click on
a row in the first subwindow, and the data in the row, just for id and name
will be added to the second subwindow.
I do not want to connect the second subwindow to the database.

Could you write the code for this?

"""



chat_subwindow_with_widgets.py
=========================QSqlTableModel
