#!/usr/bin/env python3
"""
Vibe Coded with claude  .. may want to edit


is_mounted.py - check whether a path is mounted (local or network).

Pure Python, no external commands needed for the basic check. It reads the
kernel mount table (/proc/self/mountinfo) rather than touching the
filesystem, so it won't hang on a dead NFS/SMB share.

Use as a module:

    from is_mounted import is_mounted, mount_info

    if is_mounted("/mnt/8ball1"):
        ...

    if not is_mounted("/mnt/nas", check_responsive=True):
        print("NAS missing or not responding")

    info = mount_info("/mnt/8ball1")
    # {'mountpoint': '/mnt/8ball1', 'fstype': 'ext4', 'source': '/dev/sdb1'}
    # or None if not mounted

Or from the command line (same behaviour as is-mounted.sh):

    is_mounted.py [-q] [-c] PATH [PATH...]
"""

import os
import subprocess
import sys

MOUNTINFO = "/proc/self/mountinfo"


def _unescape(field):
    """mountinfo escapes space, tab, newline and backslash as octal (\\040 etc)."""
    return (field.replace("\\040", " ")
                 .replace("\\011", "\t")
                 .replace("\\012", "\n")
                 .replace("\\134", "\\"))


def _normalise(path):
    path = os.path.abspath( os.path.expanduser(path) )
    return path.rstrip("/") or "/"

#---------------------------------
def mount_info(path):
    """
    Return info about what is mounted exactly at `path`, or None.

    Returns a dict with 'mountpoint', 'fstype' and 'source'. If several
    things are mounted on the same path, the topmost (last) one is returned.
    A systemd automount that hasn't been triggered yet has fstype 'autofs'.
    """
    path        = _normalise(path)
    found       = None

    with open(MOUNTINFO) as f:
        for line in f:
            # Format: id parent maj:min root MOUNTPOINT opts [optional...] - FSTYPE SOURCE superopts
            left, _, right = line.partition(" - ")
            left_fields     = left.split()
            right_fields    = right.split()

            if len(left_fields) < 5 or len(right_fields) < 2:
                continue

            if _unescape(left_fields[4]) == path:
                found = {
                    "mountpoint": path,
                    "fstype": right_fields[0],
                    "source": _unescape(right_fields[1]),
                }

    return found

# --------------------------------------
def is_responsive( path, timeout=5 ):
    """
    Return True if `path` answers a stat() within `timeout` seconds.

    Runs stat in a separate process, because a stat on a hung NFS mount can
    block forever and can't be interrupted from inside Python.
    """
    try:
        proc = subprocess.Popen(["stat", "-t", path],
                                stdout=subprocess.DEVNULL,
                                stderr=subprocess.DEVNULL)
    except OSError:
        return False
    try:
        return proc.wait(timeout=timeout) == 0
    except subprocess.TimeoutExpired:
        proc.kill()
        # Don't wait() again: a process stuck on a dead NFS server may not
        # die until the mount recovers.
        return False

#-----------------------------------------
def is_mounted( path, check_responsive=False, timeout = 5 ):
    """
    Return True if something is really mounted at `path`.

    - An empty mount-point directory counts as NOT mounted.
    - An untriggered x-systemd.automount (fstype 'autofs') counts as NOT mounted.
    - With check_responsive=True, the mount must also answer within `timeout`
      seconds (catches network shares whose server has gone away).
    """
    info    = mount_info(path)

    if info is None or info["fstype"] == "autofs":
        return False

    if check_responsive and not is_responsive(info["mountpoint"], timeout):
        return False

    return True

#-----------------------------------------
def is_mounted_with_info(path, check_responsive = False, timeout=5):
    """
    Return (is_mounted, info). info always has the same keys:
    mountpoint, fstype, source, is_mounted.
        not sure this is correct, but no def of correct
    """
    info = mount_info(path)

    if info is None:
        info = {"mountpoint": _normalise(path), "fstype": None, "source": None}
        mounted = False

    elif info["fstype"] == "autofs":
        mounted = False

    elif check_responsive and not is_responsive( info["mountpoint"], timeout ):

        mounted = False

    else:
        mounted = True

    info["is_mounted"] = mounted  # lets include this
    return mounted, info


#-----------------------------------------
def check_list( list_of_paths, check_responsive = True, timeout = 5 ):
    """

        note return includes info
    """
    info_dict     = {}
    all_ok        = True
    first_fail    = ""
    path_dict     = {}

    for i_path in list_of_paths:
        is_path_mounted, path_info   = is_mounted_with_info(
            i_path, check_responsive = check_responsive, timeout = timeout )

        if not is_path_mounted:
            all_ok     = False

        info_dict[ i_path ] = path_info

    # for  i_key, i_value in  info_dict.items():
    #     msg     = f"    {i_key}: >{i_value}<"
    #     print( msg )

    return ( all_ok, info_dict )


#-------------------------------------
def _main(argv):
    import argparse
    parser = argparse.ArgumentParser(description="Check whether paths are mounted.")
    parser.add_argument("-q", "--quiet", action="store_true",
                        help="print nothing, just set the exit code")
    parser.add_argument("-c", "--check", action="store_true",
                        help="also check the mount responds (hung network shares)")
    parser.add_argument("-t", "--timeout", type=float, default=5,
                        help="seconds to wait with -c (default 5)")
    parser.add_argument("paths", nargs="+", metavar="PATH")
    args = parser.parse_args(argv)

    def say(msg):
        if not args.quiet:
            print(msg)

    status = 0
    for p in args.paths:
        info = mount_info(p)
        path = _normalise(p)
        if info is None:
            say(f"NOT MOUNTED: {path}")
            status = 1
        elif info["fstype"] == "autofs":
            say(f"NOT MOUNTED: {path} (automount configured, not yet triggered)")
            status = 1
        elif args.check and not is_responsive(path, args.timeout):
            say(f"UNRESPONSIVE: {path} ({info['fstype']} from {info['source']}, "
                f"no response in {args.timeout:g}s)")
            status = 1
        else:
            say(f"MOUNTED: {path} ({info['fstype']} from {info['source']})")
    return status


if __name__ == "__main__":
    sys.exit(_main(sys.argv[1:]))
