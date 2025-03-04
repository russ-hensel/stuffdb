


Use the next for search:

====chat
====stuff
====Tech
====Versions
==== Scratch
==== Snips

====Vocab
====Environment
===========ORM
========ram disk

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

for clipboard
    accumulate copys automatically

    ?? strip list of file names does to base name


PythonCookbook

====Tech
main    - > stuff_db_qt  --> stuff_db_main_window --> document_maker

                             midi_management

====stuff




====Versions   old version info in  ./docs/version_notes.txt


                also see tech_notes.txt

----
---- ver63

    why
        -- just another checkpoint
                help working quite well, mostly saves when it should
                hyper commans work at base level
                improved layout and data dict

        !! paste prior is broken again
        ** add snippet command

    ** fix close and distruction of window and perhaps the titles

    !! check add copy in picture and fix
FileNotFoundError: [Errno 2] No such file or directory: '/mnt/WIN_D/temp_photo/99/new_test/9903_004.jpg'

        >>---- multiple add to picture
                ** began work
                **  need to update add_copy thru data dict then good enough for now
                    regenerate fileds, test
                    why not fix picture detail layout a bit  -- done better but not all  working
                                                                is good in help
        add picture and album tables to examples/help

        -- quiet down the logging
        -- fix
            ** history prior next broken -- click on list works
                    seems to work but did not really change, continue to watch
                    did add some save
            ** copy add  --- pretty good for now
                add data dict item -- fix up dict and regen code and test
                        try on help and stuff
                        then pictures
                add in add as option ?
                    clear_add
                    clear_clear   via agument
                        clear but_keep_if
                        some work in custom_widgets

            ** text search is broken
            *! quiet down some logging



move to debug and or delete
doc->str
tab->str



---- ver62

        why
                -- just another checkpoint
                     add works
                     save bug fixed
                     a few more docs working
                     db build from scratch much improved
                     logging much improved and prints removed

        ** selects seem broken for everyting but help -- no files are missing

        *! need data dict work for editable and columnspan
        ** history is broken cannot select from list
        ** prior-next should save



        *! save and tab switching  -- put note in ex_python.db
            where is tab switching tracked
                    document base   on_tab_changed

                need some sort of guid base  -- look in help

        *! executable help
            ?? idle command
            ** Python      use qt_exec
            ** url         use webbrowser
            ** Bash        use terminal
            ** text        use text editor
            ** shell       like double click
            ** search      just in help for key words now

        !! doc to str and tab to str  get off menu bar ??
        !! load a lot of photos to pictures and to an album

        !! run out of github ??
        !! look at  links in text exp in help

                save if
        ** test do save on add  -- works on help
        ** rebuild help form with new fields

         ** rebuild help column headers -- enter in how to do it howto as word

            !! add an end or commen thing  >>ignore  >>comment to keep out of code

          !! review pictures albums subjects
             !! picture tab not changed if no pic in detail picture on detail tab ok
             !! subject add does not seem to come across from stuff
                     think fixed to come across but not always triggered -- use data_manager

              File /mnt/WIN_D/russ/0000/python00/python3/_projects/stuffdb/stuff_document.py:144 in get_topic
                if self.record_state:

                AttributeError: 'StuffDocument' object has no attribute 'record_state'

                !! brose when empy still has a pic look at what to trigger create and move

            !! subject from plant  -- look in data_manager

  File /mnt/WIN_D/russ/0000/python00/python3/_projects/stuffdb/picture_document.py:2706 in populate_model_other
    open_topics_list    = AppGlobal.mdi_management.open_topics    # list of dicts

  File /mnt/WIN_D/russ/0000/python00/python3/_projects/stuffdb/mdi_management.py:415 in open_topics
    topic_dict[ "topic"]      = i_window.get_topic()

  File /mnt/WIN_D/russ/0000/python00/python3/_projects/stuffdb/plant_document.py:174 in get_topic
    a_id        = self.detail_tab.id_field.get_raw_data()

AttributeError: 'PlantDetailTab' object has no attribute 'id_field'


          !! plantsubwindow should be Plant Document and so on
          *! automate some save
          !! validate an int
          !! trim the line edict
          !! trim text after end of line


---- ver61

        why
                -- just another checkpoint after a few things fixed
                     add new may finally work so help works, now see
                     if we can get photos to work  -- add then update

        ** add at detail seems to work
        ** try to add a picode_timercture --- seems to work, but needs clean up on details
        ** does add work for photo show ??  = album
                redo_photoshow_tables

                how to gen code
                    dict_main     --- seems to gen the field ok, lets look at more
                                        now going with dict_main for fields
                    code_gen
                    rpt_data_dict
        lets gen the fields for the photoshow
                    got the fields put into album_document
        ** new fields, add seems to work
        ** criteria_select is broke
        ** put new logging in album at least a few places
        **    cleaned up criter gui a bit

        ** time for add to album  -- we can add an album and add a picture to it
            add an album does not reset photos in album  -- the 404 param was wrong but can uw clear

        !! is there a clear for pictures other than 404 ?? in code as .clear but does it work

        ** in help text first update works second fails fixed

        ** review stuff for select add update
            ** redo tables
            ** redo build gui

            ** fixed  text not getting saved --- what about picture text -- seems to be saved

        ** review plant for select add update
            ** update plant criteria
                         self._build_top_widgets(  placer ) was missing
                    ** key words seem to work
            ** new tables
            ** key word table name corrected, key words work
            ** text not saved --- table name was wrong -- seems fixed

get_topic   --- record state in data manager why do we need it
  File /mnt/WIN_D/russ/0000/python00/python3/_projects/stuffdb/base_document_tabs.py:1128 in post_init
    self._build_gui()

  File /mnt/WIN_D/russ/0000/python00/python3/_projects/stuffdb/picture_document.py:708 in _build_gui
    sub_tab      = PictureSubjectSubTab( self )

  File /mnt/WIN_D/russ/0000/python00/python3/_projects/stuffdb/picture_document.py:2297 in __init__
    open_topics         = AppGlobal.mdi_management.open_topics

  File /mnt/WIN_D/russ/0000/python00/python3/_projects/stuffdb/mdi_management.py:415 in open_topics
    topic_dict[ "topic"]      = i_window.get_topic()

  File /mnt/WIN_D/russ/0000/python00/python3/_projects/stuffdb/plant_document.py:170 in get_topic
    if self.record_state:

AttributeError: 'PlantDocument' object has no attribute 'record_state'

        !! tried to fix with record_state   =          self.detail_tab.data_manager.record_state
                did it work
        also thid needed fix in plant doc   self.enable_send_topic_update  = True


Change Log:
            newest at bottom


            import stuff_text
                    code_gen.... is sort of gone, make use of data_dict_....
                    convert to use parameters
                    updated adjust_path

                    lots of update but the sql --- bind is still bad

                    wrote util to insert fake text see stuff_util_sql.py

            ** fix undesired tab switch on select
                            in base document .... looks like list not set up correctly
                            if current_ix not in [ self.detail_tab_index, self.text_tab_index, self.picture_tab_index, ]:
                                tab_folder.setCurrentIndex( self.detail_tab_index )

                            picture ok but not text
                            this may be fix in _build_gui
                                  self.text_tab_index      = ix
            ** check that this is used when it should be in all documents
                    self.picture_tab             = base_document_tabs.StuffdbPictureTab( self )


            ** improved data_dict including a bootstrap from sql

            ** fixed list and  history on plant planting

                   !!look at list and history on album and.....

            ** help save seems ok but not sure

            !! build table for pictures  = photos   not sure if want photo text
                    stuff_util_sql.py   --- uses parameters

                    bootstrap    in rpt_....

            !! picture document
                !! list of what works
                    add
                        failed on 1005  but the text go in -- look in log
                         added some debug to new record, but need more



                        2025-01-30 11:25:25,139 - DEBUG - document_manager update_new_record  self.table_name  = 'photo'
                        2025-01-30 11:25:25,140 - DEBUG - CQEditBase get_data_for_record     id
                        2025-01-30 11:25:30,176 - ERROR - submitAll error: DataManager.update_new_record  self.current_id = 1005 self.table_name = 'photo'
                        2025-01-30 11:25:30,182 - ERROR - error text: No Fields to update
                        2025-01-30 11:25:30,188 - DEBUG - delete_rows for key words 1005   set()

                        so does add not set fields to changed = true\

                        add message for model dirty .... need more now just in add new record

                    update  failed on key word after add


                    add picture file
                    display picture file


                    browse  one pic
                        moved ok but old pic still displayed -- seems ok when multiple files
                        move when already there  -- got message ok

                    looks like edit.is_changed shold largely be changed as invalid not reset not clear we really use it

                    need to get info_about into better shape add some tests

                    get rid of whole universal convert instead have pair of functions
                    rec    record
                    str    string
                    format default to None
                    in the data dict name the functions, and the edit_format


                    in the data dict

                    self.rec_to_edit        =  rec_to_edit   # default None will use str to str
                    self.edit_to_rec        =  edit_to_rec   # default None will use str to str
                    self.edit_format        =                # default to none no special formatting


                    rec_to_edit( )
                    edit_to_rec( )

                    for most fields, just string to string
                    value   = rec_to_edit_str_to_str( rec_val, format = None )      # use partial closure to set format a string
                    value   = edit_to_record str_str( rec_val, format = None  )


                    value   = rec_to_edit_int_to_str( rec_val, format )
                    value   = edit_to_record string_to_int( rec_val, format )

                    value   = rec_to_edit_int_to_qdate( rec_val, format )
                    value   = edit_to_record qdate_to_int( rec_val, format )


                some is working
                !! add sub dir  = or check on its function think it should auto fill
                *! change print to logging   -- got tired, still more to do
                changed print to dialog for already have a picture

            ** broke help, fixed help  probably broke all docs as I changed custom edits
            !! continue breaking custom edits

            !! fix picture for new custom edits
                    fetch update may work
                    add fails -- why  self.id_field.set_preped_data( str(next_key ),  )
                        remove old function and convert all id's to strings

                            # looks like a du whab about setRecord what does it do ?
                            # record = model.record(0)
                            # self.field_to_record(  record )
                            # model.setRecord( 0, record)'

            ** change parameter to clear log file exch time

            ** add model state ( data_manager ) to the toolbar getting rid of xxxx

            ** prints removed from custom widgets
                        msg         = ( f"get_rec_data Field {field_name} "
                                        f"does not exist in the record.")
                        logging.error( msg )
                        logging.debug( msg )
                        a_str   = ( f"{a_str}\nRow {row}: {row_data}")


            ** so much trouble with logging move into own object

            ** add easy rebuild of help files, key gen, later other areas

            !! highlight does not work correctly on some custom edits why

            ** add manual add to log functionality for debugging  in main window

            ** save on help is finally working on new records

            ** make db just for help examples of python
            ** improve button placement
            ** get auto run working on python examples

            !! fix run in idle

            !! quite down prints and logging even more

            !! time for a version update ?? soon in any case



self.model_display

---- ver60

        why
                -- just another checkpoint after a few things fixed
                !! work on logging and prints and debug and code gen

 ----ver59

        why
                -- just another checkpoint after a few things fixed
                    not a big backup


                    *! start adding templates to help  may want real list not ddl
                    *! implement print to logging -- that is redo logging

                    *! fix initial window size kluge ok for now
                    *! make enter on criteria caluse select -- for line edist only in help so far
                    *! test save on add
                    *! continue with qt exe
                    ** set the number of characters for a tab in the text area
                    *! fix the history heading and functionalityt
                    ** get title on help and lengthen at least key words

        logger = logging.getLogger()
        logger.log(22, "This is a 22 message from my_logger.")
        logging.debug( "call was: logging.debug" )
        logging.debug( msg )
        logger.log( logging.CRITICAL, msg )



what are the arguments to QApplication( []  ) and what do they do?
Please explain.



>> debugt
self.tab_name
print( self.data_manager )

in widget

print( self )
in data manager
self.table_name

---
        #rint( f"set_data_from_record {debug_fn}")
        data       = record.value( self.field_name  )
        can we error check above
        i have a   PyQt5.QtSql.QSqlRecord i can get the data for a field
        with record.value( "some_name"  )
        but how can i be sure the field some_name is in the
        record

# Check if the field exists
if record.indexOf(field_name) != -1:
    value = record.value(field_name)
    print(f"Value for '{field_name}': {value}")
else:
    print(f"Field '{field_name}' does not exist in the record.")



----

        need some more buttons.... on the text field of stuff and.....



 ----ver58

        why
                -- back from key west
                -- text in general and esp help working fairly well
                fetch add save working fairly well

                next
                    -->
                    some rough edges
                        ** move text search to bottom
                        * continue on executable text ?? or done for now
                        *! remove some dead stuff
                        ** get text code out of base documents
                        *! column headers on list and history
                        ** minimize text id and make read only
                        *! helps if you feel like it
                        *! quiet down prints no longer useful




                big    !! get picture document running again
                        !! album document







 ----ver56

        why

            !! get picture fetch to work again
                      a bit of a pain without a picture db so wait till home ??

            !! instead of code gen look at using data dict at runtime as arguments
               perhaps start with history

            --->   *! get history going again  -- still need an update function
                    when to add to history
                    save of a new
                    selection from the criteria list
                         both clicked and prior next  --- clicke call prior next
                         not from selection from history -- history does not change history
                          # want to update on save


            *!  next help key word update on fetched or add record.
                for add go back to the qt5_by_example

            !! get all docs running

            !! define text tables for all docs

            lots of progress good save point --
            custom edit progress

            !! add record count to fetch ( but think self limiting )
            !! too much space in sql for order by

            !! put in update manager for detail like check update in stuff
               and help -- not auto update yet
                        but some auto update is left in base  Document
            stuff
                !! update
                !! add
                        detail does not get key
                        text   does not change

 --->>     help

                ** fetch
                            seem ok now, plus enhances, may still not work in all combo
                            use fully qualified proof carefully
                            fails without notice as far as i can tell  -- if an error
                            can we clear a control  -- yes with bad query
                            so if it fails we at least have nothing
                            in list the control is



                ** update   detail      seems to work on fetched records will it survive key word fix
                            text        seems to work on fetched records will it survive key word fix
                            key words
                                        fetched ng  -- they were not added to the data manager search on is_key_word


                ** add
                            does it save
                            are key words ok

                ** test the build of fields from data dict





            perhaps go back to controls and
                redo set_to_default
                set_to_default_function

                set_to


                set_as_pass
                set_as_value
                set_as_changed


 ----ver55

        why
            lots of progress good save point --

            key words implementing  in base and stuf
                stuff some fields added

            ** finish detail move to parent, stuff is the model



            next maye in order
            !! make new record take an argument for add_copy ....
                argumen added but only for default option = "default"

            ** pictures are a lot better but not done
            !! for pictures add copy would be good, need
                to work on custom edits and perhaps qt_by_example for that
                what about my grid layout is it written?

            ** check all documents to see if they run,
                check select all
                look at parents for all
                use stuff as the reference

                parents ok on ....
                ** album
                ** help
                ** people
                ** picture   text tab fixed
                ** plant
                ** planting
                ** stuff

                select runs  ....
                ** album
                ** help
                ** people
                ** picture
                ** plant
                ** planting
                ** stuff




 ----ver54
            why
                lots of progress good save point --
                got help back working with python and idle

                ** remove dead code
                !! decide what next
                !! back to picture
                        !! add to album where
                        *! first add picture including move
                        !! inject file not found pic into picture viewer
                        !! add picture
                            !! save at end of add
                            !! redo browse picture show
                            !! at add of picture change to unknow pic -- no change to what fields say may have been been
                            a default ( but unlikely )

                !! at end of browse select first row


                set up a fake picture db -- with some of the photos
                    where
                    source where

 ----ver53
            why
                lots of progress good save point --
                    add picture to album almost works after weeks of messing about
                        now accept relational will not work use qsqlquery

            !! does add work ??

                    ** picture  -- yes with some oddities
                    !! stuff ??

                        DetailTabBase new_record   stuff 3951
                        TypeError: CQEditBase.on_data_changed() missing 1 required positional argument: 'new_text'

                        set_data id = <built-in function id> self.is_changed = False
                        time stuff may be lost


            !! work on picture browse

                    ** files added to table
                        !! have date and size but date is in timestamp
                        ** get column header sort
                    ** experiment move works so far...
                    !! finish picture move   ... lot of progress
                    !! set up test photo source and target for picture move


            !! help is a mess, way behind the other tabs

                    key_words.KeyWords( kw_table_name, AppGlobal.qsql_db_access.db )


                 *! get the select cleande up
                 !! look into python code examples in help -- can we run code in python console and then use breakpoint
                ** add seems not to work, does it work anywhere --- had wrong base document

            *! make stuff add if it does not so far --- and check others
                    note no key word update anywhere -- check all the base text documents

 ----ver52
            why
                lots of progress good save point --
                    add picture to album almost works after weeks of messing about
                        now accept relational will not work use qsqlquery

            ** Album add picture from picture document -- works
            !! Album add picture from picture document -- add more error checking and test

            !! back to add subject to a picture  -- lets say from stuff model on picture to album
                    add does not delete from other

            send_topic_update needs fixing !!



---- messed up version number again but stuff in backup

 ----ver49
            why
                lots of progress good save point -- ** most photo work except pictures and albums are special

            ** mode and version to about box -- add memory from something else


            ** Album display now working
            !! Album add picture from picture document
                    back to this after about a week away working on test of QtWidgets
                    in the picture sub tab
                        add_photo_test
                            is this possible:  test in qsql_widgets

                            photo_in_show
                                need to gen an id                 id                     for db
                                need to add the photo_show_id     photo_show_id          for db
                               * need to add the photo_id,                                for db   --- this may be the problematic one
                                 sequence                          sequence               for db

                               * file name                   display only would be fetched
                               * sub dir                    display only would be fetched
                               * the name of the photo             photo.name    in dict photo_name  display only would be fetched

                                * need to come in in the add dict



            need update of photo_in_show key gen, think there is a util for this, check
            album -- and others when selecting a row make sure it is in scroll view
            this is a fix to prior next may be in normal sub tab look


            ** most of code done to make sure key gen is up to date see import key_gen

            ** picture document not opening


 ----ver48
            why
                lots of progress good save point

                !! stuff get pictures to show


                !! lot of undone stuff from below, but wait on that for a bit
                !! add a file to pictures
                Album:
                    photoshow, problem with date import do not seem to be timestamps,
                       ** may just set to default until have time to process

                    *! got picture data, display works only a tiny bit
                    ** redo fields -- seem ok
                    !! add a picture to album  --- album still much a copy from plant, fix all this
                        ** fix select
                        ** generate key words for album
                        *! photo in show table is missing   which is photoshow_photo sometimes
                                import does not seem to fix up the keys, add this to import
                ** change all document to base changes

                ** album should have a picture subtab with a list of pictures and also a picture tab

                !! rename to DetailTabBase, need parent_window in init and may be overusing

            may need new import of photo subject and other fix up

            more:

                as it comes up
                !! a clear before select to show select has failed??
                ** alpha document in open menu

        try

               /mnt/WIN_D/Russ/0000/python00/python3/_projects/stuffdb/russ_temp/russ_qsqlrelationalmodel_photos.py



 ----ver47
            why
                lots of progress good save point

            ?? some confusion on types is it int or integer or either
             int here was a mistake, change to enum??


            ** get stuff new to work
                    id generated but not saved
                    needs more test

            ** stuff add id to criteria for testing id for sort
                both directions for sort
                cap insensitive sort
                !! add tiebreaker to sort say id  ??

            *! may still want to work on sort

            *! improve names of modules and classes

    # ------------------------------------------
    def set_picture_ix( self, picture_ix   ):
        """
        try to go to absolute index
        """

        above is what needs work


                ** prior next for going thru list are fine but do not change the selection

                !! stuff doc
                    ** save from tool bar works but some odd messages track down

                    !! pictures on stuff

                !! planting pictures where are they

                        ** planting key_words seems not to work -- table is missing

                        saharas rose will select pictures --- data is very spotty so use this record

                        !! pictures do not show up

                !! pictures --- subject sub tab what happened
                        !! picture subjects table for the picture_document
                        -- table there but is working ? -- many id's are messed up

                !! get some other sub tabs back

                !! add standard criteria buttons to all criteria tabs

                *! add id old_id to criteria for debugging purposes -- but change to bind var

                !! should need only one code gen file driven by parameters, put rest in sub dir
                   see if can get by on just code gen


----ver46
            why
                lots of progress good save point
                right now implement windows up to date at detail level but not sub windows
                new custom controls work but not finished
                code gen..... is better, imports is better but improvements need to be spread around

            *! make custom text edit like line edit but....

            *! get the help text tab to work -- but would like to move onto detail tab, should not be
               be so hard

            !! make fix up sql to supply default text to items missing it.

            ** fix picture document select on filename like

            ** clear criteria after building

            !! think about implementing too few criteria limits ??

            ** make clear on dates work better at least checked ignore  --- default values later
                    ** picture ignore clear dates

            ** stuff select may be broken  -- also order of order by fixed

            *! help will not even open
                    problem is ?? look at building of fields in criteria and detail to start with
                    check create fields for correct timestamp, but may be in data dict

               *! the text page is missing else okish
               !! date select missing
               !! some controls on criteria missing -- make the standard ones now ??


            ** update people for criteria and fields -- works for select on minimal test

            then

            ** clean out dead code
                ** photo
                ** album
                ** people
                ** stuff
                ** plant
                ** Planting
                ** help

             more
                !! will need to test all documents --
                !! need to look at sub detail
                !! clear field not yet implemented for detail window --- also needed in custom_widget or is in parent -- no code is at least in progress
                !! album needs create tab cleaned up and perhaps total pdate

----ver45
            why
                lots of progress good save point

                 do import_photo_subject.py
                *! do plant from scratch ?? --- partway thru basic doc works

                   **  in criteria is is build_tab or _build_tab, find and fix   use _build everywhere, but some changes did not get made
                record_to_field_promoted  look for in all docs

                *! get stuff and its photos back in db and update the does
                     by 18:00 --- did not make it

                ** stuff works against stuff table but not detail sub tabs
                ** do stuff key words stuff_key_word_indexer.py

                ** do picture key word

                !! clean up db create for parameterized versions -- at least change names for now

                    yes
                    !! plant table a mess just get some in id failed to load fix
                    !! plant text  -- in but did not convert from old id to id
                         where is the sql for that --- in sql seems ok but see file for more work


                *! fix criteria clear fields on both all -- need to update all docs coming soon

                !! add key words for both and make sure working

                !! on all criteria use the criteria widgets --- think line edit and need combo Boxes
                !! key words for picture and planting
                !! make criteria widgets build the criteria dict for you
                            add criteria_name to the init of all of them


                !! make planting as up to date as pictures
                !! copy db to hard drive with current name

                *! planting

                    *! criteria tab -- better -- changed parent, build_gui...
                                       select runs but needs to be fixed will do in a bit
                                       select most of code moved from document to criteria to get closer
                                       to args
                                       select works some, not key words and have not built that table
                                       for picture or planting

                    ** list            add fields
                    ** detail          rebuild using new custom fields from code gen

                    ** fix code gen integer to string was int to integer, but no fields can manage ints

                !! do a check box that takes a bool returns an int 0 or one for now


----ver44
            why
            !! get full crud cycle working with new controls -- ignore some details for now
                use picture as the reference document

                **    sql to fix null and invalid dates

                *! get dates in picture list -- just change column list, but need conversion to correct type

                !!    fix criteria select
                        ** get the dates in the select inc ignore
                        ** order by but will need enhance

                !! reduce printing of sql
                        query_builder                   = qt_sql_query.QueryBuilder( query, print_it = False, )


                **     select
                **   validate  raises and catches except ok for now
                    clear/prior
                **    update        some ok for fetched
                    add/insert
                    delete

                ** do not let history add id if present -- later compare


                !! why does picture doc have its own picture tab, dup code



            more....

                 !!    take a look at old version todo below
                 **   picture viewer pro as drop in for picture viewer
                 !! add features to picture viewer pro


----ver43

            ** have photo view display file name and if found find a 404 picture
                 if not found
            ** have a 404 pic for viewer and thumbnail
            ** on import lowercase all file names ... this will not be part or the
                app only import
            ** lower case all existing file, but not new ones brought in by app

          !! on imports all the dates are null -- think is error look into it
            picture back to record to filed with custom widgets

            are dates getting converted correctly, at least not throwing exceptions

            import of file name capitalization still messed up fix this
                    dat file seems to have mixed cap that matches
                    'rsh56360'  in db   micro1.jpg is alreay wrong case
                    rsh56411    in db   looks like sybase adds leading zeros that need to be fixed
                    rsh56412    file name extension wrong in the .dat file wrong cap

                    -- looks like I should downshift all filename in the imported
                           but not do it on any new data

            change stuffdb_tabbed_subwindow   to --- document_parents   doc_parents  as doc_parents

----ver42
        why:
            continue change to custom widgets linked to records
            !! split edits into criteria edits and field edits
                ** field edits now seem to work
                ** multiple inherit for field edits
            !! get criteria date edits to work, do not do multiple inherit yet

            !! add multiple inherit to edits
            !! expand edit types and conversions
                    decimal
                    float
                    bool
                    check box
            ** criteria controls sort of working

            ** make picture forward thru list work
                    error in field to record -- fixed for now
                    but some issues still left, have not fixed for full crud
                    !! fix now -- action not getting to picture tab

            !! fix logging and exceptions

                msg     = f"a message {data}"
                AppGlobal.logger.info( msg )
                print( msg )

            !! and exceptions  like 1/0  picture Clicked on list row 26, column 1, db_key=3316
                        same in 3317 and dt_item is 1/1/00  so bad data in database  file gar3037.jpg   'brsh421'
                        in spreadsheet seems to be null or empty
                        this is an import issue
                        can find all with a 1/1/0 filter in db beaver, am going to skip for now
                        put a try except around it


                msg    = f"where this_is_an_exception_message { = }"
                print( msg )
                AppGlobal.logger.info( msg )    # debug info warning, error critical
                raise Exception( msg, )
                raise ValueError( msg, )



            how does  '1/1/00' get in the time data
                        import_utils  string_to_timestamp( date_string, date_format ):


        todo:



---- ver41
        why:
            much progress checkpoint

        todo:
            picture document
                *! pictures show if click on list but not forward and backward buttons
                !! work on date conversions -- have some code where
                ** get rid of tab create functions to tighten up the code
                !! history broken  -- fed from select in detail, would be better from list clicked
                          and a common list of fields for the list and the history  maybe history should\
                          be the same type of stuff as list but just with no select, update....
                          now in both field to record and record to field, if dup only the new should
                          be kept, --- this logic still not there
                          fails because of the use of mapper

                ** default to allow null file to No or change to has file and make yes default
                !! detail list how do I control the columns displayed some seem to be missing

        !! look at import of photo esp the time dates which seem missing





---- ver40
        why:
            much progress checkpoint

        ** show parameters  -- !! may want to reduce no shown
        ** help -- kw select works
            !! help info add fields

        picture document
            ** key word broken again  --- table missing
            *! pictures show if click on list but not forward and backward buttons
            ** empty file name select not working -- cap problem in criteria
            ** key word and like working
            !! add more criteria
            !! get subjects import working and foreign keys straightened out
            ** get picture back on detail tab
            !! get rid of tab create functions to tighten up the code
            !! text tab not working
            ** clip file name

        ** pictures
                !! not fit and zoom fully right
                * clear on file not found ??
                ** clip file name
                ** detect file not exists
                !! use scroll bars only when needed but let zoom farther
                !! select area for zoom -- code is around some place

        !! import people
            ** people
            ** people_text
            ** people_key_words


        !! update people_document
            ** basic select is ok, does it use mapper? --- yes old field skipped
            ** add key work to select and to criteria
            ** people criteria select now work


        think next may be done
        !! stuff document
            !! index key words
        ** select in people not working -- check for table import
                looks like import is missing -- get it then
                work on pictures



---- ver39

            !! export
D:\Sybase\Sybase Central
D:\Sybase\Sybase Central\win32\scview.exe
sybase central 3. ...
sybase_central\win32 one of the exe's     stuff2000  dba   sql

            open go to connect
                  stuff2000  dba   sql



            help key words working some
            ** stuff imported
            ** stuff_text imported
            ** and a lot more of imports and key words....

            !! fix stuff document for current db structures

            !! so import stuff from pb, index and fix its select
            !! show parameters in a dialog box
            !! get mode into title ?

            more
                !! select from below




----ver38
    why: cleanup and checkpoint after good progress

            !! expand help document for more fields
            ** import help info
            ** index help key words
            *! do key word search in help
            *! figure out the timestamps


----ver37
    why: cleanup and checkpoint after good progress

            !* lots of progress on import of help_info and help_text in
                /mnt/WIN_D/Russ/0000/python00/python3/_projects/stuffdb_import/help_text
            !* lots of progress on indexer

            *! see how close I can get to getting everything in the ancestor
                text tab
                ** done stuff
                ** done people
                help
                album
                planting

                !! added buttons to left side, make do something
                ** context menu came for free

            Hard Issues

                !! key words
                !! stuff in stuff
                !! plants in plantings
                !! picture file names in 3 parts
                     config   root  final_part

                !! add commands to text
                        go to url
                        open shell
                        multi line commands




            *! pick up work at history tab and its selection.... some of tab is done
                  see the demo of qtablewidget
                  !! ok but dup in history
                  ** prior next not changing select

            !! stuff history mostly working but not people check all other docs
            !! text tab not working for help

            Need to fix the dyslexia   mid mdi change

            -- people detail working sort of ok now with a data mapper
            !! test people more
            !! polish off some rough parts
            !! delete dead code

            more:

                    **  prior next from main window should do an update
                    !! sync doc ops to tool bar at least as far as current choices
                    !! compact forward back.... list impiy save
                    !! same for history
                    !! is stuff events ok
                    !! is people events ok



----ver36
    why:
        cleanup and checkpoint after good progress

        !! start in on people
            people tables   people and phones

            ** have basic people functionality with datamaper and field code gen  -- more test and tweak to do

            !! work on Edit Contact Info to use
                  delegate and perhaps a datamapper
                !! get rid of test code in both this and people event



        !! review crud for all implemented

        ** stuff events --- ok for now
            update was in edit dialog -- worked but should be removed
            class StuffEventSubTab( QWidget  ):   # moving to StuffdbSubTabTab(  revise or change plan
            rework of update db and edit... and parent all seem to be working
        ** review stuff pictures for now

                ** picture added to stuff but missing the file name  --- because the picture was missing its file name ok

        !! may be time again to remove some print statements
        !! and to put in a global dev_mode esp for the ui

==== Snips

        debug_msg     = f"get_key_words just got key words {key_words = }"
        logging.debug( debug_msg )

        object_type = self.__class__.__name__

        # Get the method name using the inspect module
        method_name = inspect.currentframe().f_code.co_name

        print(f"Object Type: {object_type}")
        print(f"Method Name: {method_name}")

        -----------------
        # import inspect  # for debug i
        # mport logging
        loc        = f"{self.__class__.__name__}.{inspect.currentframe().f_code.co_name} "
        debug_msg  = f"{loc} >>> {column_name = }  {order_by_dir = }"
        logging.debug( debug_msg )
        logging.error( msg )


        logging.log( level, msg )
        LOG_LEVEL  = 20

        logging.log( LOG_LEVEL,  debug_msg, )

        ------------- info about

        model       = self.model
        msg         = ( f"model_record_info {self.table_name = }" )
        log_msg     = info_about.INFO_ABOUT.find_info_for(
                            model,
                            msg         = msg,
                            print_it    = False
                           )
        logging.debug( log_msg )



==== Scratch  see snippets.ppy


        stuff
            field order and key words

                    name
                    descr
                    add kw

                    move dates together


             add topic in title deleteme



------------------------

            addd   title deleteme    100024    -- addd is in once

            then look in key words after save    -- addd is in once

            reselect it  try addd   --- ok

            copy over to key words and save and check

            still seems ok
                 select on deleteme


==== Scratch Old
Determine the transaction state of a database

    int sqlite3_txn_state(sqlite3*,const char *zSchema);

The sqlite3_txn_state(D,S) interface returns the current transaction state of ASC

schema S in database connection D. If S is NULL, then the highest transaction state of
any schema on database connection D is returned. Transaction states are (in order of lowest to highest):

    SQLITE_TXN_NONE
    SQLITE_TXN_READ
    SQLITE_TXN_WRITE

If the S argument to sqlite3_txn_state(D,S) is not the name of a valid schema, then -1 is returned.

See also lists of Objects, Constants, and Functions.



uff tabs working, still no one to many on detail
    still no history
    lots of message box to change to logging
    lost of code from other apps much dead

=======Environment


Should run on many python >=3.6 with qt5 but so far I am just
running on my dev machine a Lenovo Thinkpad with
Linux Mint.
    I am using Python 3.12 in an anaconda/spyder install.

    My IDE is Spyder.


===========ORM

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
