"""Generate a country-borders equirectangular world map for the LatLon Picker.

Run from anywhere:
    python tools/make_world_map.py
    python tools/make_world_map.py --width 4000 --height 2000
    python tools/make_world_map.py --output /tmp/my_map.png

Output defaults to ``latlon_picker/assets/world_equirectangular.png``.

First run will download the Natural Earth shapefiles via cartopy (~few MB)
and cache them under ``~/.cartopy``.
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


def render(width: int, height: int, output: Path) -> None:
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
                                       edgecolor=LAKE_EDGE_COLOR, linewidth=0.3)
    ax.add_feature(cfeature.COASTLINE, edgecolor=COASTLINE_COLOR, linewidth=0.5)
    ax.add_feature(cfeature.BORDERS,   edgecolor=BORDER_COLOR,    linewidth=0.4)

    fig.savefig(output, dpi=dpi, pad_inches=0)
    plt.close(fig)


def main(argv: list[str] | None = None) -> int:
    here    = Path(__file__).resolve().parent
    project = here.parent
    default_out = project / "assets" / "world_equirectangular.png"

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--width",  type=int, default=4000)
    parser.add_argument("--height", type=int, default=2000)
    parser.add_argument("--output", type=Path, default=default_out)
    args = parser.parse_args(argv)

    render(args.width, args.height, args.output)

    size_kb = args.output.stat().st_size / 1024
    print(f"Wrote {args.output}  ({args.width}x{args.height},  {size_kb:.1f} KB)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
