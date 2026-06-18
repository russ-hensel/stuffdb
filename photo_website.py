#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
photo_website.py -- build a simple static HTML photo gallery from a list
of photo dicts (the same shape SlideShowSubWindow produces).

No Qt, no third-party dependencies; pure stdlib.

Typical use:
    from photo_website import PhotoWebsite

    site = PhotoWebsite(
        photo_list   = [ ... dicts ... ],   # photo_file, photo_sub_dir, photo_name, ...
        output_dir   = "/some/place/website_album_42",
        picture_root = "/path/to/photos/root",
        title        = "My Album", )
    site.build( )

    # site.index_path is an absolute Path to index.html
"""

# ---- imports
import html
import logging
import shutil
from   pathlib import Path


# ---- constants
CSS = """\
body { font-family: sans-serif; max-width: 1100px;
       margin: 0 auto; padding: 1em;
       background: #111; color: #eee; }
a { color: #6cf; }
h1, h2 { color: #fff; }

.grid { display: grid;
        grid-template-columns: repeat( auto-fill, minmax( 220px, 1fr ) );
        gap: 12px; }
.grid a { display: block; text-decoration: none; color: inherit;
          background: #1a1a1a; padding: 6px; border-radius: 4px; }
.grid img { width: 100%; height: 200px;
            object-fit: cover; display: block; }
.grid .caption { padding: 6px 4px 2px;
                 font-size: 0.9em; color: #ccc;
                 overflow: hidden; text-overflow: ellipsis;
                 white-space: nowrap; }

.photo img { max-width: 100%; max-height: 80vh;
             display: block; margin: 0 auto; }

.nav { display: flex; justify-content: space-between;
       margin: 1em 0; gap: 1em; }
.nav a, .nav span { flex: 1; text-align: center;
                    padding: 0.5em 1em; background: #1a1a1a;
                    border-radius: 4px; text-decoration: none; }
.nav a:hover { background: #2a2a2a; }
.nav span { color: #555; }

.meta { font-size: 0.9em; color: #aaa; margin-top: 0.5em; }
"""


# ---- helpers
def _safe_html( s ):
    """
    html-escape s; treat None as empty.
    """
    if s is None:
        return ""
    return html.escape( str( s ) )


# ----------------------------------------
class PhotoWebsite( ):
    """
    Build a self-contained static photo gallery in `output_dir`.

    Layout produced:
        output_dir/
            index.html
            style.css
            photos/0001.html, 0002.html, ...
            images/0001<.ext>, 0002<.ext>, ...
    """

    # ------------------------------------
    def __init__(
        self,
        photo_list,
        output_dir,
        picture_root,
        title         = "Photo Album",
        copy_images   = True,
    ):
        """
        photo_list   -- iterable of dicts with photo_file, photo_sub_dir,
                        photo_name keys (plus anything else, ignored)
        output_dir   -- directory to (re-)create; will be wiped on build
        picture_root -- filesystem root the photo_sub_dir/photo_file is
                        relative to
        title        -- shown on index page + in <title>
        copy_images  -- True copies originals into images/; False symlinks
        """
        self.photo_list     = list( photo_list )
        self.output_dir     = Path( output_dir )
        self.picture_root   = Path( picture_root )
        self.title          = title
        self.copy_images    = copy_images

        self.index_path     = None     # set by build()

    # ------------------------------------
    def build( self ):
        """
        Generate the whole site. Wipes and recreates `self.output_dir`.
        Returns the absolute Path to index.html.
        """
        self._prepare_dirs( )
        self._write_css( )

        entries = []
        seq_n   = 0
        for photo in self.photo_list:
            src = self._source_path( photo )
            if not src.is_file( ):
                msg = f"photo_website: skipping missing source: {src}"
                logging.warning( msg )
                continue

            seq_n      += 1
            seq         = f"{seq_n:04d}"
            ext         = src.suffix.lower( ) or ".jpg"
            image_rel   = f"images/{seq}{ext}"
            page_rel    = f"photos/{seq}.html"

            self._stage_image( src, self.output_dir / image_rel )

            entries.append( {
                "seq":          seq,
                "photo":        photo,
                "image_rel":    image_rel,
                "page_rel":     page_rel, } )

        for i, entry in enumerate( entries ):
            prev_e = entries[ i - 1 ] if i > 0                  else None
            next_e = entries[ i + 1 ] if i < len( entries ) - 1 else None
            self._render_photo_page( entry, prev_e, next_e )

        self._render_index( entries )

        self.index_path = ( self.output_dir / "index.html" ).resolve( )

        msg = ( f"photo_website: wrote {self.index_path} "
                f"({len( entries )} photos)" )
        logging.info( msg )

        return self.index_path

    # ------------------------------------
    def _prepare_dirs( self ):
        """
        wipe only our own output dir; never anything else
        """
        if self.output_dir.exists( ):
            shutil.rmtree( self.output_dir )
        self.output_dir.mkdir( parents = True )
        ( self.output_dir / "photos" ).mkdir( )
        ( self.output_dir / "images" ).mkdir( )

    # ------------------------------------
    def _source_path( self, photo ):
        # lstrip the leading slashes so pathlib's `/` operator doesn't
        # treat sub_dir or file as an absolute path and discard picture_root.
        sub_dir = ( photo.get( "photo_sub_dir" ) or "" ).lstrip( "/\\" )
        file    = ( photo.get( "photo_file"    ) or "" ).lstrip( "/\\" )
        return ( self.picture_root / sub_dir / file ).resolve( )

    # ------------------------------------
    def _stage_image( self, src, dst ):
        """
        """
        dst.parent.mkdir( parents = True, exist_ok = True )
        if self.copy_images:
            shutil.copy2( src, dst )
        else:
            if dst.exists( ) or dst.is_symlink( ):
                dst.unlink( )
            dst.symlink_to( src )

    # ------------------------------------
    def _write_css( self ):
        """
        """
        ( self.output_dir / "style.css" ).write_text(
            CSS, encoding = "utf-8" )

    # ------------------------------------
    def _render_photo_page( self, entry, prev_e, next_e ):
        """
        """
        photo   = entry[ "photo" ]
        name    = _safe_html( photo.get( "photo_name" )
                              or photo.get( "photo_file" ) )

        # images live one level up from photos/
        img_src = "../" + entry[ "image_rel" ]

        if prev_e is not None:
            prev_html = ( f'<a href="{prev_e["seq"]}.html">'
                          f'&larr; Previous</a>' )

        else:
            prev_html = '<span>&larr; Previous</span>'

        if next_e is not None:
            next_html = ( f'<a href="{next_e["seq"]}.html">'
                          f'Next &rarr;</a>' )

        else:
            next_html = '<span>Next &rarr;</span>'

        total = f"{len( self.photo_list ):04d}"

        html_doc = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>{name} -- {_safe_html( self.title )}</title>
<link rel="stylesheet" href="../style.css">
</head>
<body class="photo">
<h1>{name}</h1>
<img src="{img_src}" alt="{name}">
<div class="meta">{entry[ "seq" ]} of {total}</div>
<div class="nav">
  {prev_html}
  <a href="../index.html">Index</a>
  {next_html}
</div>
</body>
</html>
"""
        page_path = self.output_dir / entry[ "page_rel" ]
        page_path.write_text( html_doc, encoding = "utf-8" )

    # ------------------------------------
    def _render_index( self, entries ):
        tiles = []
        for e in entries:
            photo = e[ "photo" ]
            name  = _safe_html( photo.get( "photo_name" )
                                or photo.get( "photo_file" ) )
            tile  = ( f'<a href="{e["page_rel"]}">'
                      f'<img src="{e["image_rel"]}" alt="{name}">'
                      f'<div class="caption">{name}</div>'
                      f'</a>' )
            tiles.append( tile )

        tiles_html = "\n".join( tiles )

        html_doc = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>{_safe_html( self.title )}</title>
<link rel="stylesheet" href="style.css">
</head>
<body>
<h1>{_safe_html( self.title )}</h1>
<p class="meta">{len( entries )} photos</p>
<div class="grid">
{tiles_html}
</div>
</body>
</html>
"""
        ( self.output_dir / "index.html" ).write_text(
            html_doc, encoding = "utf-8" )


# ---- eof
