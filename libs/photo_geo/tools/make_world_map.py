"""Generate a country-borders equirectangular world map for the LatLon Picker.

Run from anywhere:
    python tools/make_world_map.py                       # medium preset (4000x2000)
    python tools/make_world_map.py --preset high         # 8000x4000
    python tools/make_world_map.py --preset ultra        # 16000x8000  (~90 MB PNG)
    python tools/make_world_map.py --width 5000 --height 2500
    python tools/make_world_map.py --output /tmp/my_map.png

Output defaults to ``<project>/world_equirectangular.png`` (same directory
the runtime app reads from).

First run will download the Natural Earth shapefiles via cartopy (~few MB)
and cache them under ``~/.cartopy``.

Resolution rules of thumb:
    low      2000 x 1000   ~ 2 MB on disk,  ~  8 MB as QPixmap
    medium   4000 x 2000   ~ 7 MB on disk,  ~ 32 MB as QPixmap    (default)
    high     8000 x 4000   ~25 MB on disk,  ~128 MB as QPixmap
    ultra   16000 x 8000   ~90 MB on disk,  ~512 MB as QPixmap

QPixmap RAM is the real cliff: it holds the full RGBA buffer regardless
of zoom level.  "high" is the sweet spot on most laptops.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")              # headless: no Qt/Tk needed

import cartopy.crs     as ccrs     # noqa: E402
import cartopy.feature as cfeature # noqa: E402
import matplotlib.pyplot as plt    # noqa: E402


# ----- styling ----------------------------------------------------------
OCEAN_COLOR     = "#aed0e0"
LAND_COLOR      = "#e8e1c8"
COASTLINE_COLOR = "#3a4a55"
BORDER_COLOR    = "#776655"
LAKE_EDGE_COLOR = "#7596aa"


# ----- named resolution presets ----------------------------------------
# (width, height, line_scale)
#
# line_scale multiplies the baseline matplotlib linewidths (which are in
# points) so coastlines and borders stay visually consistent across
# resolutions.  Without this, a 0.5pt line is a smaller fraction of an
# 8k-wide image than it is of a 4k-wide image and effectively disappears
# at high resolution.
PRESETS: dict[str, tuple[int, int, float]] = {
    "low":      ( 2000,  1000, 0.6),
    "medium":   ( 4000,  2000, 1.0),
    "high":     ( 8000,  4000, 1.7),
    "ultra":    (16000,  8000, 2.8),
}
DEFAULT_PRESET = "medium"


def render(
    width:       int,
    height:      int,
    output:      Path,
    line_scale:  float = 1.0,
) -> None:
    """Render one PNG.  line_scale multiplies all feature linewidths."""
    if width != 2 * height:
        raise ValueError(
            f"width must be exactly 2 * height for equirectangular "
            f"(got {width}x{height})"
        )

    output.parent.mkdir(parents=True, exist_ok=True)

    dpi     = 100
    figsize = (width / dpi, height / dpi)

    fig = plt.figure(figsize=figsize, dpi=dpi, frameon=False)
    fig.patch.set_facecolor(OCEAN_COLOR)
    ax  = fig.add_axes([0.0, 0.0, 1.0, 1.0], projection=ccrs.PlateCarree())
    ax.set_global()
    ax.set_axis_off()
    # Belt-and-braces: fill both the axes patch (cartopy draws over set_facecolor)
    # and the figure patch so anything outside the GeoAxes is also ocean-coloured.
    ax.patch.set_facecolor(OCEAN_COLOR)

    ax.add_feature(cfeature.OCEAN,     facecolor=OCEAN_COLOR)
    ax.add_feature(cfeature.LAND,      facecolor=LAND_COLOR)
    ax.add_feature(cfeature.LAKES,     facecolor=OCEAN_COLOR,
                                       edgecolor=LAKE_EDGE_COLOR,
                                       linewidth=0.3 * line_scale)
    ax.add_feature(cfeature.COASTLINE, edgecolor=COASTLINE_COLOR,
                                       linewidth=0.5 * line_scale)
    ax.add_feature(cfeature.BORDERS,   edgecolor=BORDER_COLOR,
                                       linewidth=0.4 * line_scale)

    fig.savefig(output, dpi=dpi, pad_inches=0)
    plt.close(fig)


def main(argv: list[str] | None = None) -> int:
    here    = Path(__file__).resolve().parent
    project = here.parent
    default_out = project / "world_equirectangular.png"

    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--preset", choices=list(PRESETS),
                        default=DEFAULT_PRESET,
                        help=f"resolution preset (default: {DEFAULT_PRESET}). "
                             "Overridden by explicit --width / --height.")
    parser.add_argument("--width",  type=int, default=None,
                        help="override preset width (px); must be 2 * height")
    parser.add_argument("--height", type=int, default=None,
                        help="override preset height (px); must be width / 2")
    parser.add_argument("--output", type=Path, default=default_out,
                        help=f"output PNG path (default: {default_out})")
    args = parser.parse_args(argv)

    # preset supplies the baseline; explicit --width/--height overrides it.
    preset_w, preset_h, line_scale = PRESETS[args.preset]
    width  = args.width  if args.width  is not None else preset_w
    height = args.height if args.height is not None else preset_h

    # If the user gave custom dims, scale linewidths linearly from the
    # medium baseline (4000px wide => 1.0).  Clamp so very small images
    # still get a visible coastline.
    if args.width is not None or args.height is not None:
        line_scale = max(width / 4000.0, 0.4)

    render(width, height, args.output, line_scale=line_scale)

    size_kb = args.output.stat().st_size / 1024
    print(f"Wrote {args.output}  ({width}x{height}, "
          f"line_scale={line_scale:.2f}, {size_kb:.1f} KB)")
    return 0


if __name__ == "__main__":
    sys.exit(main())


