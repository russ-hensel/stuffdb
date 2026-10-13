#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ---- tof

"""
Run a list of bash commands, one after another, in a new
GNOME Terminal window. Each command is echoed before it runs and the
window stays open (interactive bash) at the end.

All commands run in one bash session so cd, export ... carry
forward to the following commands.

    import bash_cmd
    a_bash_cmd  = bash_cmd.BashCmd( cmd_list )
    a_bash_cmd.run()

    a_bash_cmd.reset( other_cmd_list, title = "other" )   # reuse
    a_bash_cmd.run()

    or just:     bash_cmd.run_cmd_list( cmd_list )

Running this file runs the demo at the bottom, not main.py.
"""

# ---- imports
import os
import shlex
import subprocess
import tempfile

# ---- end imports


# ----------------------------------------
class BashCmd( ):
    """
    hold a list of commands, build a bash script on disk, run it in gnome-terminal
    """
    def __init__( self, cmd_list = None, title = "bash_cmd" ):
        """
        cmd_list    list of strings, one bash command each
        title       window title
        """
        self.cmd_list       = []
        self.title          = title
        self.terminal       = "gnome-terminal"
        self.prompt         = "\\n\\033[1;32m$PWD $\\033[0m "   # printf format, green
        self.script_fn      = None

        if cmd_list:
            self.add_cmds( cmd_list )

    # -----------------------
    def reset( self, cmd_list = None, title = None ):
        """
        clear the commands so the object can be reused
        cmd_list    optional new commands
        title       optional new title, else keep the old one
        probably not necessary, maybe just use run
        """
        self.cmd_list       = []
        self.script_fn      = None

        if title is not None:
            self.title      = title

        if cmd_list:
            self.add_cmds( cmd_list )

    # -----------------------
    def add_cmds( self, cmd_list ):
        """
        what it says, strips white space, skips blank lines
        """
        for i_cmd in cmd_list:
            a_cmd       = i_cmd.strip()
            if a_cmd:
                self.cmd_list.append( a_cmd )

    # -----------------------
    def build_script( self ):
        """
        return the bash script as a string
        each command is echoed ( with cwd ) then run
        a failing command does not stop the rest
        """
        lines       = [ "#!/usr/bin/env bash",
                        'rm -f -- "$0"',              # script deletes itself
                        ]

        for i_cmd in self.cmd_list:
            echo_line   = ( f'printf "{self.prompt}%s\\n" {shlex.quote( i_cmd )}' )
            lines.append( echo_line )
            lines.append( i_cmd )

        lines.append( ( 'printf "\\n---- done: %d commands ----\\n" '
                        f'{len( self.cmd_list )}' ) )
        lines.append( "exec bash" )                   # leaves terminal open

        script      = "\n".join( lines ) + "\n"
        return script

    # -----------------------
    def write_script( self ):
        """
        write script to a temp file, return its file name
        """
        script          = self.build_script()
        fd, script_fn   = tempfile.mkstemp( prefix = "bash_cmd_", suffix = ".sh" )

        with os.fdopen( fd, "w" ) as a_file:
            a_file.write( script )

        os.chmod( script_fn, 0o700 )
        self.script_fn  = script_fn
        return script_fn

    # -----------------------
    def run( self, cwd = None ):
        """
        open a new gnome-terminal and run the commands in it
        cwd     starting directory, default is current directory
        returns right away, does not wait for the terminal
        """
        script_fn   = self.write_script()
        args        = [ self.terminal,
                        f"--title={self.title}",
                        "--",
                        "bash", script_fn ]
        subprocess.Popen( args, cwd = cwd )

    # -----------------------
    def __str__( self ):

        a_str   = ">>>>>>>>>>* BashCmd *<<<<<<<<<<<<"
        a_str   = f"{a_str}\n    title        {self.title}"
        a_str   = f"{a_str}\n    script_fn    {self.script_fn}"
        for ix, i_cmd in enumerate( self.cmd_list ):
            a_str   = f"{a_str}\n    {ix:3}  {i_cmd}"
        return a_str


# ----------------------------------------
def run_cmd_list( cmd_list, title = "bash_cmd", cwd = None ):
    """
    what it says
    """
    a_bash_cmd  = BashCmd( cmd_list, title = title )
    a_bash_cmd.run( cwd = cwd )
    return a_bash_cmd


# ---- demo
if __name__ == "__main__":

    cmd_list   = [
    """ ls -lah    /usr/bin/*.* """,
    """pwd """,
    """cd ~""",
    """pwd""",
    """cd  ../""",
    """ls *.py""",
    """TARGET_BASE="/mnt/millhouse/rsync/_projects/stuffdb" """,
    """echo   TARGET_BASE""",
    """echo  $TARGET_BASE""",

    ]

    a_bash_cmd  = run_cmd_list( cmd_list )
    print( a_bash_cmd )

    cmd_list   = [  """sudo smartctl -a /dev/sda""",
                      """sudo smartctl -x /dev/sda""",
                      ]

    a_bash_cmd  = run_cmd_list( cmd_list )
    print( a_bash_cmd )



# ---- eof
