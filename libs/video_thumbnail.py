#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ---- tof
"""
video_thumbnail.py

KEY_WORDS:      thumbnail video mp4 ffmpegthumbnailer subprocess
DESCRIPTION:    grab a single-frame thumbnail image from a video file by
                shelling out to ffmpegthumbnailer ( a small CLI built on
                the ffmpeg/libav libraries -- already installed here
                alongside vlc, no separate ffmpeg install needed ). no
                Qt dependency -- usable from any script, not just a tab
MORE:           ffmpegthumbnailer does its own seeking/decoding -- this
                is just a thin subprocess wrapper around it
"""


# --------------------
if __name__ == "__main__":
    #----- run the full app
    import main   # noqa  stops auto removal by pycln
# --------------------


import subprocess


# ---- end imports


#-----------------------------------------------
def make_thumbnail( video_path, output_path, timestamp = "10%", size = 320, quality = 8 ):
    """
    does not get it makes it consider change of names also paths or not
    what it says -- extract one frame from video_path and save it as an
    image at output_path ( image format is taken from output_path's
    extension -- .jpg/.png ). raises subprocess.CalledProcessError on
    failure ( e.g. bad video_path ), FileNotFoundError if
    ffmpegthumbnailer itself is not installed

    are the paths paths or strings

        video_path      -- path to the source video
        output_path     -- path to write the thumbnail image to
        timestamp       -- "hh:mm:ss" absolute, or "NN%" percentage into the
                            video ( ffmpegthumbnailer's own -t option ). some
                            files ( odd container metadata, e.g. some phone
                            mp4s ) fail to seek and silently fall back to the
                            first frame instead of raising
        size            -- thumbnail size in pixels ( longest side ), 0 for
                            the video's original size
        quality         -- jpeg/png quality, 0 ( worst ) - 10 ( best )

        from video_thumbnail import make_thumbnail  #  make_thumbnail( video_path, output_path, timestamp = "10%", size = 320, quality = 8 )
    """
    command             = [
                            "ffmpegthumbnailer",
                            "-i", str( video_path ),
                            "-o", str( output_path ),
                            "-s", str( size ),
                            "-t", str( timestamp ),
                            "-q", str( quality ),
                            ]

    subprocess.run( command, check = True, capture_output = True )


# --------------------------------
def test_make_thumbnail():

    """
    # --- How to use it now ---
    this makes filters from partial


    """
    a_file      = "/mnt/8ball1/first6_root/russ/0000/python00/python3/_projects/rshlib/utils/readme_rsh.txt"
    new_path    = make_thumbnail( a_file, "bmp" )
    print( f"new_path  {new_path}")

    a_file      = "/mnt/8ball1/first6_root/russ/0000/python00/python3/_projects/rshlib/utils/readme_rsh"
    new_path    = set_extension( a_file, "bmp" )
    print( f"new_path  {new_path}")

    a_file      = "/mnt/8ball1/first6_root/russ/0000/python00/python3/_projects/rshlib/utils/readme_rsh.txt"
    new_path    = set_extension( a_file, "mp3" )
    print( f"new_path  {new_path}")

    a_file      = Path( "/mnt/8ball1/first6_root/russ/0000/python00/python3/_projects/rshlib/utils/readme_rsh.txt" )
    new_path    = set_extension( a_file, "mp3" )
    print( f"new_path  {new_path}")

# "/mnt/8ball1/first6_root/russ/0000/python00/python3/_projects/rshlib/utils/string_list_utils.py",
# "/mnt/8ball1/first6_root/russ/0000/python00/python3/_projects/rshlib/utils/string_utils.py"


# ---- eof
