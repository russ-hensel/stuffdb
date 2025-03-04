#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 21 11:06:49 2024

@author: russ
"""
// ================================
// retrieve the list
// ================================

long				ll_row
string			ls_sql
long				li_rc

string			ls_sql_and		= ""	// set to and as soon as where not empty
string			ls_and			= " and "

string			ls_where
string			ls_group
string			ls_tables
string			ls_columns
string			ls_having

string			ls_temp
string			ls_error
string			ls_modify

string			ls_keywords
string			ls_inlist
string			ls_kw_array[]
int				li_ret
int				li_kw
date				ldate_temp

integer			li_criteria

// --------------------------

if ib_nolist then
	return 0
end if

li_rc	= idw_criteria.AcceptText()

if li_rc = -1 then
	return 0
end if

// allow for multi row
ll_row							= idw_criteria.GetRow( )

is_list_dataobject  			= idw_criteria.GetItemString( ll_row,  "as_format" )

if 	( is_list_dataobject_prior <> is_list_dataobject ) then

	idw_list.dataobject				= is_list_dataobject
	is_list_dataobject_prior 		= is_list_dataobject
	idw_list.of_settransobject( SQLCA )

	// get the original sql for modification
	ls_sql		= idw_list.Describe( "datawindow.table.select")
	//
	li_rc 	= inv_sql.of_Parse( ls_sql, inv_org_sqlattrib )
	inv_sqlattrib			= inv_org_sqlattrib

end if

ls_where		= inv_org_sqlattrib[1].s_where
ls_group		= inv_org_sqlattrib[1].s_group
ls_tables	= inv_org_sqlattrib[1].s_tables
ls_columns	= inv_org_sqlattrib[1].s_columns
ls_having	= inv_org_sqlattrib[1].s_having


if ls_where <> "" then
	ls_sql_and	= ls_and
end if


// ----- where

// datawindow dependent stuff might better be here ????
//===============================================
//
//if			ls_dataObject = "dwo_planting_rpt_1" 	then
//	// this is the normal flow
//	ls_select		= "select "
//	//ls_tables		= "stuff a, stuff b, stuff c "
//	ls_tables		= "planting a, plant b, bed c"
//	//ls_where			= " a.sign_out = b.id and a.owner = c.id "
//	ls_where			= " ( a.plant_id = b.id ) and ( a.bed = c.id ) "
//	ls_orderby		= ""
//	ls_GroupBy		= ""
//	ls_having		= ""
//	ls_dwc_sort		= " a.bed A"
//else
//	// this is the normal flow
//	ls_select		= "select "
//	//sz_tables		= "stuff a, stuff b, stuff c "
//	ls_tables		= "stuff a "
//	//sz_where			= " a.sign_out = b.id and a.owner = c.id "
//	ls_where			= ""
//	ls_orderby		= ""
//	ls_GroupBy		= ""
//	ls_having		= ""
//
//end if
//
//
////==============================================


li_criteria	= 0

// --- key word part

ls_keywords			=  Trim( idw_criteria.GetItemString( 1, "as_kw" ) )

if ls_keywords <> "" then
		// must be at least one in the array ( not really, it could be white space characters

		//li_ret		= sztokeywords( ls_keywords, ls_kw_array[] )

		//li_kw			= words_to_inlist( ls_kw_array[], ls_inlist )

		li_kw			= invo_keywords.of_criteriakeywords( ls_keywords, ls_inlist )

		if li_kw > 0 then
				if ls_where <> "" then
					ls_where	+=  " and "
				end if
				ls_where		+=  " key_word in " + ls_InList + &
										" and kw_stuff.stuff_id = a.id "

				ls_Group			= ls_columns

				ls_having		=  " count(*) = " + string( li_kw, "##0")
				ls_tables		+= ", kw_stuff "
				li_criteria		= 1
		end if

end if

if li_kw = 0 then
	// no key words
else
	ls_sql_and		= ls_and
end if

ls_temp = ls_temp



// -----

ldate_temp	= idw_criteria.GetItemDate( 1, "date_lo" )
if not( isNull( ldate_temp ) ) then
	ls_where			= gnv_util.uf_add_sep( ls_where, " a.dt_enter >= '" + string(ldate_temp, "yyyy/mm/dd" ) + "'", " and ")
	li_criteria		= 1
end if

ldate_temp	= idw_criteria.GetItemDate( 1, "date_hi" )
if not( isNull( ldate_temp ) ) then
	ls_where			= gnv_util.uf_add_sep( ls_where, " a.dt_enter <= '" + string(ldate_temp, "yyyy/mm/dd" ) + "'", " and ")
	li_criteria		= 1
end if

// -----

ls_temp 		= idw_criteria.GetItemString( 1, "sz_type" )
if ls_temp  = "" then ls_temp = "<All>"
if ls_temp <> "<All>" then
		//	ls_where			= gnv_util.uf_add_sep( ls_where, " a.color = '" + ls_temp + "'", " and ")
		ls_where			= ls_where + ls_sql_and + "  a.type = '" + ls_temp + "'"
		ls_sql_and		= ls_and
		li_criteria		= 1
end if

ls_temp 		= idw_criteria.GetItemString( 1, "as_noreset" )

if ls_temp = "Y" then
	ib_noreset	= True
else
	ib_noreset	= False
end if


// -----

ls_temp 		= idw_criteria.GetItemString( 1, "s_container" )
if ls_temp  = "" then ls_temp = "<All>"
if ls_temp <> "<All>" then
		//	ls_where			= gnv_util.uf_add_sep( ls_where, " a.color = '" + ls_temp + "'", " and ")
		ls_where			= ls_where + ls_sql_and + "  a.cont_type = '" + ls_temp + "'"
		ls_sql_and		= ls_and
		li_criteria		= 1
end if

//ls_temp 		= idw_criteria.GetItemString( 1, "as_noreset" )
//
//if ls_temp = "Y" then
//	ib_noreset	= True
//else
//	ib_noreset	= False
//end if
//

// -----

ls_temp 		= idw_criteria.GetItemString( 1, "s_manufact" )

if isNull( ls_temp ) then
	ls_temp  = "<All>"
end if

if ls_temp  = "" then ls_temp = "<All>"
if ls_temp <> "<All>" then
		//	ls_where			= gnv_util.uf_add_sep( ls_where, " a.color = '" + ls_temp + "'", " and ")
		ls_where			= ls_where + ls_sql_and + "  a.manufact like '" + ls_temp + "'"
		ls_sql_and		= ls_and
		li_criteria		= 1
end if

// -----

ls_temp 		= idw_criteria.GetItemString( 1, "sz_author" )

if isNull( ls_temp ) then
	ls_temp  = "<All>"
end if

if ls_temp  = "" then ls_temp = "<All>"
if ls_temp <> "<All>" then
		//	ls_where			= gnv_util.uf_add_sep( ls_where, " a.color = '" + ls_temp + "'", " and ")
		ls_where			= ls_where + ls_sql_and + "  a.author like '" + ls_temp + "'"
		ls_sql_and		= ls_and
		li_criteria		= 1
end if

// -----

ls_temp	= idw_criteria.GetItemString( 1, "s_pictures" )

Choose Case ls_temp
	Case "y"
		ls_temp			= " exists ( select * from photo_subject WHERE ( photo_subject.table_id = a.id ) and table_joined = 'stuff' ) "
		ls_where			= ls_where + ls_sql_and + ls_temp
		ls_sql_and		= ls_and
		li_criteria		= 1
	Case "n"
		ls_temp			= " not exists ( select * from photo_subject WHERE ( photo_subject.table_id = a.id ) and table_joined = 'stuff' ) "
		ls_where			= ls_where + ls_sql_and + ls_temp
		ls_sql_and		= ls_and
		li_criteria		= 1
End Choose

if ( li_criteria	= 0 ) then
	return 0
end if

// ====== put all the parts back

inv_sqlattrib[1].s_where		= ls_where
inv_sqlattrib[1].s_columns		= ls_columns
inv_sqlattrib[1].s_tables		= ls_tables
inv_sqlattrib[1].s_group		= ls_group
inv_sqlattrib[1].s_having		= ls_having

ls_sql								= inv_sql.of_assemble( inv_sqlattrib )
ls_modify							= "datawindow.table.select=~"" + ls_sql + "~""

ls_error								= idw_list.Modify( ls_modify )
if ls_error <> "" then
	MessageBox( "sql error", ls_error + ls_modify )
	return -1
else

end if

idw_list.retrieve()

if ib_noreset then
	this.of_deletedups( idw_list, is_key_col )
end if

ib_criteria_changed		= False

return 1

// ================================= end ============================





