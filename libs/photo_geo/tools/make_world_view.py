"""Generate an equirectangular "satellite view" world map.

Drop-in companion to make_world_map.py: same projection (plate carrée /
equirectangular, width == 2 * height), different name, different look.

To use:
    1) Edit the variables at the top of main() (PRESET, INPUT_IMAGE, ...).
    2) Run:  python tools/make_world_view.py

The image lands next to the module by default, with a different filename
from world_equirectangular.png so both can coexist.

------------------------------------------------------------------------
Where the "satellite" pixels come from
------------------------------------------------------------------------
By default this script uses cartopy's bundled ``ax.stock_img()`` which
is the Natural Earth 50m shaded-relief raster. It works with zero
downloads and zero setup, but its native resolution is about 1024x512;
at "high" or "ultra" presets the image will be visibly soft.

For TRUE photographic satellite imagery, download a NASA Blue Marble PNG
or JPG (public domain, already equirectangular) and point ``INPUT_IMAGE``
at it:

    https://visibleearth.nasa.gov/collection/1484/blue-marble

Look for a file named like ``world.topo.bathy.YYYYMM.3x21600x10800.png``
or the smaller 8192x4096 / 5400x2700 variants.

The script then ``imshow``s the file as the figure background and the
coastlines / borders are drawn on top with a touch of transparency.

------------------------------------------------------------------------
Image must be equirectangular
------------------------------------------------------------------------
The supplied image MUST be an equirectangular (plate carree) world map
with 2:1 aspect ratio (width = 2 * height) covering lon [-180, 180] and
lat [-90, 90]. Any other projection will produce wrong locations.

First run (or first cartopy use) will download the Natural Earth
shapefiles (~few MB) and cache them under ``~/.cartopy``.
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")              # headless: no Qt/Tk needed

import cartopy.crs       as ccrs       # noqa: E402
import cartopy.feature   as cfeature   # noqa: E402
import matplotlib.image  as mpimg      # noqa: E402
import matplotlib.pyplot as plt        # noqa: E402


# ----- named resolution presets ----------------------------------------
# (width, height, line_scale).  Same shape as make_world_map.PRESETS so
# the two scripts stay in sync conceptually.  Duplicated rather than
# imported so each script can be read and run standalone.
PRESETS: dict[str, tuple[int, int, float]] = {
    "low":      ( 2000,  1000, 0.6),
    "medium":   ( 4000,  2000, 1.0),
    "high":     ( 8000,  4000, 1.7),
    "ultra":    (16000,  8000, 2.8),
}


# ----- overlay styling (drawn ON TOP of the satellite image) -----------
# White / cream tend to read well against the mostly dark blues, greens
# and browns of a satellite background.  Alpha < 1 so the underlying
# imagery still shows through.
COASTLINE_COLOR = "#ffffff"
COASTLINE_ALPHA = 0.65
BORDER_COLOR    = "#ffe9a8"
BORDER_ALPHA    = 0.55


# -----------------------------------------------------------------------
def render(
    width:           int,
    height:          int,
    output:          Path,
    line_scale:      float        = 1.0,
    input_image:     Path | None  = None,
    show_coastlines: bool         = True,
    show_borders:    bool         = True,
) -> None:
    """Render one PNG to ``output``.

    If ``input_image`` is a real file, it is used as the photographic
    background; otherwise cartopy's stock image is used.
    """
    if width != 2 * height:
        raise ValueError(
            f"width must be exactly 2 * height for equirectangular "
            f"(got {width}x{height})"
        )

    output.parent.mkdir(parents=True, exist_ok=True)

    dpi     = 100
    figsize = (width / dpi, height / dpi)

    fig = plt.figure(figsize=figsize, dpi=dpi, frameon=False)
    ax  = fig.add_axes([0.0, 0.0, 1.0, 1.0], projection=ccrs.PlateCarree())
    ax.set_global()
    ax.set_axis_off()

    if input_image is not None and Path(input_image).is_file():
        # User-supplied equirectangular satellite image (e.g. NASA Blue
        # Marble).  ``extent`` tells matplotlib what geographic rectangle
        # the pixels cover; ``transform`` says the pixels themselves live
        # in PlateCarree coordinates.
        img = mpimg.imread(str(input_image))
        ax.imshow(
            img,
            origin    = "upper",
            extent    = [-180, 180, -90, 90],
            transform = ccrs.PlateCarree(),
        )
        used_source = str(input_image)
    else:
        # Fallback: cartopy's bundled Natural Earth 50m raster.  ~1024 px
        # wide natively, so it will look soft at high preset output.
        ax.stock_img()
        used_source = "cartopy stock_img (Natural Earth 50m)"

    if show_coastlines:
        ax.add_feature(
            cfeature.COASTLINE,
            edgecolor = COASTLINE_COLOR,
            linewidth = 0.5 * line_scale,
            alpha     = COASTLINE_ALPHA,
        )
    if show_borders:
        ax.add_feature(
            cfeature.BORDERS,
            edgecolor = BORDER_COLOR,
            linewidth = 0.4 * line_scale,
            alpha     = BORDER_ALPHA,
        )

    fig.savefig(output, dpi=dpi, pad_inches=0)
    plt.close(fig)

    # cheap warning so the user notices when the stock image will be
    # outclassed by the output resolution.
    if input_image is None and width >= 6000:
        print(
            "  note: stock_img is ~1024 px wide; at this preset the image "
            "will look soft.\n"
            "        set INPUT_IMAGE to a NASA Blue Marble file for sharp "
            "satellite pixels."
        )

    print(f"  source: {used_source}")


# -----------------------------------------------------------------------
def main() -> int:
    # =================== EDIT THESE ====================================
    PRESET           = "high"            # one of PRESETS keys
    INPUT_IMAGE      = None              # or Path("/path/to/blue_marble.png")
    SHOW_COASTLINES  = True
    SHOW_BORDERS     = True

    here    = Path(__file__).resolve().parent
    project = here.parent
    OUTPUT  = project / "world_satellite.png"
    # ===================================================================

    width, height, line_scale = PRESETS[PRESET]

    render(
        width           = width,
        height          = height,
        output          = OUTPUT,
        line_scale      = line_scale,
        input_image     = INPUT_IMAGE,
        show_coastlines = SHOW_COASTLINES,
        show_borders    = SHOW_BORDERS,
    )

    size_kb = OUTPUT.stat().st_size / 1024
    print(
        f"Wrote {OUTPUT}  ({width}x{height}, "
        f"line_scale={line_scale:.2f}, {size_kb:.1f} KB)"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
