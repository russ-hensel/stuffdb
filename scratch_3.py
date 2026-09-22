

planting_document_edit_fix_me
edit_selected_record   setData for id 9216
edit_selected_record   setData for id_old
edit_selected_record   setData for planting_id_old
edit_selected_record   setData for planting_id 50004
edit_selected_record   setData for event_dt 1400904000
edit_selected_record   setData for dlr 0
edit_selected_record   setData for cmnt new comment zz
edit_selected_record   setData for type
edit_selected_record   setData for dt_mo
edit_selected_record   setData for dt_day
edit_selected_record   setData for day_of_year



    # ----------------------------------
    def edit_selected_record(self):
        """
        from stuff then update
        Open dialog to edit the currently selected event.
        not clear this works at all
        """
        selected_data = self.get_selected_row_data()
        if selected_data is None:
            return

        row, data = selected_data

        # # Open dialog with the current data
        # #dialog = StuffEventDialog(self, edit_data=data)
        # dialog = people_document_edit.EditPeopleContact( self, edit_data = data )
            # self the parent tab
        dialog    = self._build_dialog( data )
        model     = self.model

        if dialog.exec_() == QDialog.Accepted:
            form_data = dialog.get_form_data()

            # for field_name, field_ix in  PEOPLE_CONTACT_COLUMN_DICT.items():
            #     model.setData( model.index( row, field_ix ), form_data[ field_name ] )

            field_ix = -1   # could make loop or even list comp
            for i_column_name, col_dict in self.field_dict.items():

                msg     = f"edit_selected_record   setData for {i_column_name} {form_data[ i_column_name ] }"
                print( msg )

                field_ix    += 1
                model.setData( model.index( row, field_ix ), form_data[ i_column_name ] )
                # model.setHeaderData( ix_col, Qt.Horizontal, col_dict[ "col_head_text"  ] )
                # view.setColumnWidth( ix_col,                col_dict[ "col_head_width" ] )


Key points for QSqlTableModel (PyQt5/Qt5):

Editable vs. non-editable

Whether a column is “editable” in a QTableView depends on what your flags() implementation returns for that column.

If you don’t give Qt.ItemIsEditable, the user can’t type into it in the view — but that doesn’t prevent you from inserting or changing data programmatically.

Storing data

If you call model.setData(index, value) (even on a non-editable column), the underlying record in the model is updated.

When you later call model.submitAll(), those changes will be written to the database, provided the column isn’t read-only at the database level (e.g. it’s not a computed column, generated column, or restricted by triggers/permissions).

Example