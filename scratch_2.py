#!/usr/bin/env python3
# -*- coding: utf-8 -*-



 Handling Large .db-wal Files:

    Why large?: Frequent writes or uncommitted transactions can cause growth.
    Fix:
        Run

PRAGMA wal_checkpoint(FULL);
    did on test db size did not change -- do a change


to force a full checkpoint.
        Check for stuck transactions or unclosed connections in your application.
        Vacuum the database (VACUUM;) to optimize if needed.

Deleting .db-wal Files:

    Caution: Do not manually delete .db-wal files while the database is in use, as this can corrupt the database or cause data loss.
    Only delete if:
        All database connections are closed.
        You’re sure no transactions are pending.
        You’ve backed up the database.




1. Check for any remaining connections:

# On Linux/Mac, check if any process is using the database -- add this a linux command ??
lsof your_database.db*

# Or check for SQLite processes  - add this a linux command ??
ps aux | grep sqlite




    #---------------- restart here model view dialog name
    #  ---- chat functions
    def add(self):
        """
        Open dialog to add a new event and insert it into the model.
        """
        dialog      = self._build_dialog( edit_data = None )
        model       = self.model

        if dialog.exec_() == QDialog.Accepted:
            form_data   = dialog.get_form_data()

            # Create a new record
            row         = self.model.rowCount()
            self.model.insertRow(row)

            model.non_editable_columns = { 99 }  # beyond all columns -- delete soon

            self.fix_add_keys( form_data )  # mutable dict so no return needed.

            ix_col = -1   # could make loop or even list comp
            for i_column_name, col_dict in self.field_dict.items():
                try:  # if we do not have all fields will get key errors
                    ix_col    += 1
                    model.setData( model.index( row, ix_col ), form_data[ i_column_name ] )
                except KeyError as error:
                    # if we do not want to do all fields
                    error_message = str(error)
                    debug_msg = ( f"SubTabWithEditBase.add() KeyError Caught an error: {error_message} skipping this field" )
                    logging.log( LOG_LEVEL,  debug_msg, )