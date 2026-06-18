"""QGraphicsScene that owns the world pixmap, the projection, and the crosshair.

Also provides a small public draw API (add_marker / add_line / add_text /
clear_drawings / reload_pixmap) so callers can annotate the map and undo it
without touching the underlying pixmap.
"""
from __future__ import annotations

from pathlib import Path
from typing  import Iterable

from qtpy.QtCore    import Qt
from qtpy.QtGui     import (
    QBrush, QColor, QFont, QPainter, QPainterPath, QPen, QPixmap,
)
from qtpy.QtWidgets import (
    QGraphicsEllipseItem, QGraphicsItem,    QGraphicsPathItem,
    QGraphicsPixmapItem, QGraphicsScene,    QGraphicsSimpleTextItem,
)

from crosshair_item import CrosshairItem
from projections    import EquirectangularProjection

# z-values: pixmap 0, lines 4, markers 5, text 6, crosshair 10
Z_LINE      = 4
Z_MARKER    = 5
Z_TEXT      = 6


class MapScene( QGraphicsScene ):
    """Holds the world pixmap and a single shared crosshair overlay."""
    DEFAULT_H = 720
    DEFAULT_W = DEFAULT_H * 2      # 2:1 aspect for equirectangular

    #-----------------------------
    def __init__(self, image_path: str | Path | None = None) -> None:
        super().__init__()

        # remembered so reload_pixmap() can fall back to the original.
        self._image_path                    = image_path
        # tracks every QGraphicsItem the public draw API added so that
        # clear_drawings() removes exactly those (not pixmap or crosshair).
        self._drawings: list[QGraphicsItem] = []

        pixmap = self._load_pixmap(image_path)
        self._pixmap_item   = QGraphicsPixmapItem(pixmap)
        self.addItem(self._pixmap_item)
        self.setSceneRect(0, 0, pixmap.width(), pixmap.height())

        self.projection     = EquirectangularProjection(pixmap.width(), pixmap.height())

        self.crosshair      = CrosshairItem()
        self.crosshair.setVisible(False)
        self.addItem( self.crosshair )

    #-----------------------------
    def show_crosshair_at(self, x: float, y: float) -> None:
        self.crosshair.setPos(x, y)
        self.crosshair.setVisible(True)

    #-----------------------------
    def hide_crosshair(self) -> None:
        self.crosshair.setVisible(False)

    # --- public draw API -----------------------------------------------------
    #-----------------------------
    def add_marker(
        self,
        lat: float,
        lon: float,
        *,
        color:  QColor | str | None = None,
        radius: int  = 8,
        label:  str | None = None,
    ) -> QGraphicsItem:
        """
        Drop a filled circle (and optional text label) at (lat, lon).

        Returns the QGraphicsItem so the caller can also remove just this one
        with self.removeItem(item).  All items added here are tracked, so
        clear_drawings() will remove them too.

        Marker stays the same screen size at any zoom (ItemIgnoresTransformations).
        """
        col      = QColor(color) if color is not None else QColor(220, 40, 40)
        x, y     = self.projection.latlon_to_pixel(lat, lon)

        pen      = QPen(col)
        pen.setCosmetic(True)
        pen.setWidth(2)
        brush    = QBrush(col)

        item     = QGraphicsEllipseItem(-radius, -radius, 2 * radius, 2 * radius)
        item.setPos(x, y)
        item.setPen(pen)
        item.setBrush(brush)
        item.setFlag(QGraphicsItem.ItemIgnoresTransformations, True)
        item.setZValue(Z_MARKER)
        self.addItem(item)
        self._drawings.append(item)

        if label:
            txt   = QGraphicsSimpleTextItem(label)
            txt.setBrush(QBrush(col))
            font  = QFont()
            font.setPointSize(10)
            font.setBold(True)
            txt.setFont(font)
            # nudge the label clear of the dot, top-right.
            txt.setPos(x + radius + 2, y - radius - 4)
            txt.setFlag(QGraphicsItem.ItemIgnoresTransformations, True)
            txt.setZValue(Z_TEXT)
            self.addItem(txt)
            self._drawings.append(txt)

        return item

    #-----------------------------
    def add_line(
        self,
        points: Iterable[tuple[float, float]],
        *,
        color:  QColor | str | None = None,
        width:  int = 2,
    ) -> QGraphicsItem:
        """
        Connect a sequence of (lat, lon) points with straight pixel segments.

        Note: a straight pixel line on equirectangular is approximately a
        rhumb line, not a great-circle path, and a line crossing the
        antimeridian will be drawn the long way around.  Pre-split your
        points if either matters.

        Cosmetic pen so width stays constant at any zoom.
        """
        col   = QColor(color) if color is not None else QColor(40, 80, 200)
        pen   = QPen(col)
        pen.setCosmetic(True)
        pen.setWidth(width)

        path  = QPainterPath()
        first = True
        for lat, lon in points:
            x, y = self.projection.latlon_to_pixel(lat, lon)
            if first:
                path.moveTo(x, y)
                first = False
            else:
                path.lineTo(x, y)

        item = QGraphicsPathItem(path)
        item.setPen(pen)
        item.setZValue(Z_LINE)
        self.addItem(item)
        self._drawings.append(item)
        return item

    #-----------------------------
    def add_text(
        self,
        lat:    float,
        lon:    float,
        text:   str,
        *,
        color:  QColor | str | None = None,
        font_pt: int = 12,
    ) -> QGraphicsItem:
        """
        Draw a text label whose anchor is at (lat, lon).
        Text size is constant at any zoom (ItemIgnoresTransformations).
        """
        col   = QColor(color) if color is not None else QColor(20, 20, 20)
        x, y  = self.projection.latlon_to_pixel(lat, lon)

        item  = QGraphicsSimpleTextItem(text)
        item.setBrush(QBrush(col))
        font  = QFont()
        font.setPointSize(font_pt)
        item.setFont(font)
        item.setPos(x, y)
        item.setFlag(QGraphicsItem.ItemIgnoresTransformations, True)
        item.setZValue(Z_TEXT)
        self.addItem(item)
        self._drawings.append(item)
        return item

    #-----------------------------
    def clear_drawings(self) -> None:
        """
        Remove every item the draw API added.  The pixmap and the crosshair
        are untouched.
        """
        for item in self._drawings:
            self.removeItem(item)
        self._drawings.clear()

    #-----------------------------
    def reload_pixmap(self, image_path: str | Path | None = None) -> None:
        """
        Replace the underlying world image.  If image_path is None, the path
        used at construction is reused (cheap "restore" call).

        Drawings (markers, lines, text added via the public API) are kept;
        call clear_drawings() before/after if you want them gone too.
        Crosshair is hidden because the prior scene point may now mean
        something different if the projection changed.
        """
        path     = image_path if image_path is not None else self._image_path
        pixmap   = self._load_pixmap(path)
        self._pixmap_item.setPixmap(pixmap)
        self.setSceneRect(0, 0, pixmap.width(), pixmap.height())
        self.projection  = EquirectangularProjection(
                                pixmap.width(), pixmap.height())
        self._image_path = path
        self.crosshair.setVisible(False)

    #-----------------------------
    def _load_pixmap(self, image_path: str | Path | None) -> QPixmap:
        if image_path is not None:
            path = Path(image_path)
            if path.is_file():
                pix = QPixmap(str(path))
                if not pix.isNull():
                    return pix
        return self._make_placeholder(self.DEFAULT_W, self.DEFAULT_H)

    #-----------------------------
    @staticmethod
    def _make_placeholder(w: int, h: int) -> QPixmap:
        """Draw a blue ocean with a 30-degree graticule.

        Lets the app run end-to-end without a real world map asset.
        """
        pix = QPixmap(w, h)
        pix.fill(QColor(170, 200, 230))

        painter = QPainter(pix)
        try:
            painter.setRenderHint(QPainter.Antialiasing, False)

            painter.setPen(QPen(QColor(120, 150, 180), 1))
            for lon in range(-180, 181, 30):
                x = (lon + 180) / 360 * w
                painter.drawLine(int(x), 0, int(x), h)
            for lat in range(-90, 91, 30):
                y = (90 - lat) / 180 * h
                painter.drawLine(0, int(y), w, int(y))

            painter.setPen(QPen(QColor(60, 90, 130), 2))
            painter.drawLine(0, h // 2, w, h // 2)         # equator
            painter.drawLine(w // 2, 0, w // 2, h)         # prime meridian

            painter.setPen(QColor(40, 40, 60))
            font = QFont()
            font.setPointSize(12)
            painter.setFont(font)
            painter.drawText(
                20, 30,
                "Placeholder world map - run tools/make_world_map.py to "
                "produce world_equirectangular.png next to this module.",
            )
        finally:
            painter.end()
        return pix


# ---- eof