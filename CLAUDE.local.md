# CLAUDE.local.md

Personal notes for working with Russ on this project. Not shared/checked in.

## About me
- Solo author of StuffDB — I know this codebase deeply. Skip beginner-level explanations of the architecture; get straight to specifics (file/line references are great).
- This is an informal personal project (reimplementation of an old PowerBuilder app), not production software — don't suggest enterprise-grade process (CI, strict typing, etc.) unless I ask for it.

## My dev setup
- I develop with Spyder, using `uv` for the Python environment (not Anaconda, despite what the README says).
- DB target and app settings (icon, logging, paths) are chosen by hand-editing `Parameters.choose_mode()` in `parameters.py` — I comment/uncomment one `mode_*` call at a time. If a session needs a specific mode, I'll tell you which one; don't assume a default.
- Entry point is `main.py`.

## Notes from Russ
Yes I have read and understood Pep8.  I use some of the ideas.  But I like the way I format and until there lots more contributors I will format the modules I have created the way I like.

Some quirks of the coding style

# adjust_path.py
I use this module to change my path because of the way source is laid out on my machines.  It also make some modules in sub-directories loadable with just their module name.  Probably best to keep it of only modify with care

# if __name__ == "__main__": usage
At the top of most files.  In development running of most file will result in the whole app being run by means of main.py  This means you do not have to navigate to main.py to run.

# Lots of white space, equal sign and other code column alignment
I find it more readable, may or may not blacken in future.

# Cast instance variable to locals

-- I need to explain....

# Parenthesis around strings

Often used when not necessary because makes extension of string to multi-line string easy.

# unnecessary local variables

as in

msg       = ( "some message" )
print( msg )

Why:
* can assist in debug
* helps keep lines short
* may be more readable
* if local is used multiple times actually speeds code ( does no slow down )
* typos are caught in locals but not instance var.
* often used: msg, widget, sql, db,

# Prefix a_

Why:

May be used to prevent name collisions: a_str not str for a variable

# Looping with index

I normally use ix for the numerical index in a loop.  If looping over a list of names, I might use "i_name in names" with enumerate both of them.

# comments beginning with "# ---- something"
This creates an outline heading in Spyder. It is great for code navigation. # ---- tof for top of file # ---- eof for end of file.

# Long Modules
This seems to come, in part, with QT programming, but these long modules often come with multiple classes that are all loaded at the same time Separate classes gives name space isolation. The outline comments in Spyder make navigation easy.  I have not yet found a reason to break them up.

# Doc Strings say "What it Says... "
Use to keep code style tools quite and used when I think the method name, arguments, and code are self explanatory enough.

# No typing
Have not seen the cost benefit being favorable.  My try letting simulated intelligence take a try at it.  If the cost were low enough I would do it.

# No Tests
I just have not figured out how to do it especially since so many things happen primarily in the GUI.  Not sure there is a favorable cost/benefit.  Want to show me how?

# Linting
These quirks tend to lead to low scores in linting.  Additionally the Spyder linter seems unable to validate the imports from qtpy.  My adjust_path.py trick also makes imports un-findable by the linter.

# Dead Code
We slowly move out dead or commented out code.  Some of the commented out code may stay a long time for debugging.  Methods that end in xxx are on their way out.  Methods that end in _old or _bak are also on the way out, but we are not in a hurry.


# Code to re-vistit
* !! marks code that "must" be revisited.
* ?? marks questions to think about when we have time
