"""Crosshair overlay drawn on the MapScene at the current cursor position."""
from __future__ import annotations

from qtpy.QtCore    import QPointF, QRectF
from qtpy.QtGui     import QColor, QPainter, QPen
from qtpy.QtWidgets import QGraphicsItem

#-----------------------------------
class CrosshairItem( QGraphicsItem ):
    """A simple '+' with a small ring at the centre.

    Uses ItemIgnoresTransformations so the crosshair stays the same screen
    size regardless of the view's zoom level.
    """

    ARM_PIXELS = 18   # half-arm length, in screen pixels
    RING_PIXELS = 4
    #-----------------------------------
    def __init__(self, color: QColor | None = None) -> None:
        super().__init__()
        self.setZValue(10)                                     # on top of pixmap
        self.setFlag(QGraphicsItem.ItemIgnoresTransformations, True)

        self._color = color or QColor(220, 40, 40)
        pen = QPen(self._color)
        pen.setCosmetic(True)
        pen.setWidth(2)
        self._pen = pen

    #-----------------------------------
    def boundingRect(self) -> QRectF:
        s = self.ARM_PIXELS + 2
        return QRectF(-s, -s, 2 * s, 2 * s)

    #-----------------------------------
    def paint(self, painter: QPainter, option, widget=None ) -> None:
        s = self.ARM_PIXELS
        r = self.RING_PIXELS
        painter.setPen(self._pen)
        painter.drawLine( -s, 0, s, 0 )
        painter.drawLine( 0, -s, 0, s )
        painter.drawEllipse(QPointF(0, 0), r, r)


# ---- eof