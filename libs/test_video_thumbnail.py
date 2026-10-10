#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ---- tof
"""
test_video_thumbnail.py

claude drafted, a bit on the clever side
"""


import subprocess
import sys
import traceback
from   pathlib import Path

from   PIL import Image

from   video_thumbnail import make_thumbnail


# ---- end imports


VIDEO_DIR       = Path( "/mnt/8ball1/first6_root/temp_picture_test/src_scr/mp4" )

VIDEO_FILES     = [
                    VIDEO_DIR / "PXL_20260705_215438384.mp4",     # 21.5 s
                    VIDEO_DIR / "PXL_20260705_220418411.mp4",     # 215.7 s, 541 MB
                    ]


# ---- helpers
# -------------------------------------
def thumb_path( video_path, label, extension = ".jpg" ):
    """
    what it says -- where the thumbnail for one test goes, next to the video
    """
    video_path      = Path( video_path )
    file_name       = ( f"{video_path.stem}_thumb_{label}{extension}" )

    return video_path.with_name( file_name )

# -------------------------------------
def make_thumb( video_path, label, extension = ".jpg", **kwargs ):
    """
    read it -- remove any old thumbnail first, so a stale file from an
    earlier run can not make a failed call look like a pass
    """
    output_path     = thumb_path( video_path, label, extension )
    output_path.unlink( missing_ok = True )

    msg              = ( "\nmake_thumb call make_thumbnail with:"
                        f"\n    {video_path} "
                        f"\n    {output_path}  "
                        f"\n    {kwargs}" )
    print( msg )
    make_thumbnail( video_path, output_path, **kwargs )

    # seems to also work
    make_thumbnail( Path( video_path ), Path( output_path ), **kwargs )

    return output_path


# ---- tests
# -------------------------------------
def test_videos_exist():
    """ what it says -- nothing else means much if this fails """
    for video_path in VIDEO_FILES:
        assert video_path.is_file(), ( f"missing test video {video_path}" )

# -------------------------------------
def test_default_jpg():
    """
    defaults: 10% in, longest side 320, written as a real jpeg
    """
    for video_path in VIDEO_FILES:
        output_path     = make_thumb( video_path, "default" )

        assert output_path.is_file(), ( f"not written {output_path}" )

        with Image.open( output_path ) as img:
            assert img.format == "JPEG", ( f"{output_path.name} format {img.format}" )
            assert max( img.size ) == 320, ( f"{output_path.name} size {img.size}" )

# -------------------------------------
def test_png_small():
    """
    format follows the output extension, size is the longest side
    """
    for video_path in VIDEO_FILES:
        output_path     = make_thumb( video_path, "png_160", ".png", size = 160 )
        # "png_160", ".png" used to construct output path
        # = make_thumbnail( video_path, output_path, **kwargs ) kwargs = { "size": 160 }

        with Image.open( output_path ) as img:
            assert img.format == "PNG", ( f"{output_path.name} format {img.format}" )
            assert max( img.size ) == 160, ( f"{output_path.name} size {img.size}" )

# -------------------------------------
def test_original_size():
    """
    size = 0 keeps the video's own frame size, bigger than any thumbnail
    """
    for video_path in VIDEO_FILES:
        output_path     = make_thumb( video_path, "full_size", size = 0 )

        with Image.open( output_path ) as img:
            assert max( img.size ) > 320, ( f"{output_path.name} size {img.size}" )

# -------------------------------------
def test_timestamps_differ():
    """
    read it -- 10% and 90% in should be different frames. the
    make_thumbnail() docstring warns some phone mp4s fail to seek and
    silently give the first frame -- this is the test that catches that
    """
    for video_path in VIDEO_FILES:
        path_10         = make_thumb( video_path, "pct_10", timestamp = "10%" )
        path_90         = make_thumb( video_path, "pct_90", timestamp = "90%" )

        assert path_10.read_bytes() != path_90.read_bytes(), (
                f"{video_path.name} 10% and 90% thumbnails are identical, seek failed?" )

# -------------------------------------
def test_absolute_timestamp():
    """
    "hh:mm:ss" form -- 5 s is inside both videos
    """
    for video_path in VIDEO_FILES:
        output_path     = make_thumb( video_path, "at_5s", timestamp = "00:00:05" )

        assert output_path.stat().st_size > 0, ( f"{output_path.name} is empty" )

# -------------------------------------
def test_bad_video_raises():
    """
    what it says -- a missing video must raise, not quietly write nothing
    """
    video_path      = VIDEO_DIR / "no_such_video.mp4"
    output_path     = thumb_path( video_path, "bad" )

    try:
        make_thumbnail( video_path, output_path )

    except subprocess.CalledProcessError:
        pass

    else:
        raise AssertionError( "no CalledProcessError for a missing video" )

    assert not output_path.exists(), ( f"{output_path.name} written anyway" )


# ---- runner
# -------------------------------------
def run_all():
    """
    read it -- a tiny stand in for pytest: call every test_* function in
    this module, report each, return the number that failed
    """
    tests           = [ ( name, obj ) for name, obj in globals().items()
                        if name.startswith( "test_" ) and callable( obj ) ]
    failed          = 0

    for ix, ( name, a_test ) in enumerate( tests ):
        try:
            a_test()
            print( f"PASS  {ix:2d}  {name}" )

        except Exception:
            failed      += 1
            print( f"FAIL  {ix:2d}  {name}" )
            traceback.print_exc()

    msg             = ( f"\n{len( tests ) - failed} passed, {failed} failed, thumbnails in {VIDEO_DIR}" )
    print( msg )

    return failed


# --------------------
if __name__ == "__main__":
    sys.exit( 1 if run_all() else 0 )

# ---- eof
