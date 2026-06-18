"""QGraphicsView subclass that emits lat/lon as the user moves and clicks.

Supports wheel zoom (anchored at cursor) and drag-to-pan with either the
middle mouse button or the right mouse button.  The right-button context
menu is suppressed so the drag-release doesn't trigger one.
"""
from __future__ import annotations

from qtpy.QtCore    import QPoint, Qt, Signal
from qtpy.QtGui     import QMouseEvent, QPainter, QResizeEvent, QWheelEvent
from qtpy.QtWidgets import QGraphicsView

from map_scene import MapScene


class MapView( QGraphicsView ):
    """View over a MapScene that translates mouse events into geo-coordinates.

    Signals:
        coordsHovered(lat, lon): emitted on every mouse move while inside the map.
        coordsCleared():         emitted when the cursor leaves the map.
        coordsPicked(lat, lon):  emitted on a left click inside the map.
        zoomChanged(zoom):       current zoom level (1.0 == fit-in-view).
    """

    coordsHovered = Signal(float, float)
    coordsCleared = Signal()
    coordsPicked  = Signal(float, float)
    zoomChanged   = Signal(float)

    # ---- zoom tunables --------------------------------------------------
    ZOOM_STEP = 1.20    # multiplicative factor per wheel notch
    MIN_ZOOM  = 1.0     # 1.0 == fit-in-view; cannot shrink past full globe
    MAX_ZOOM  = 16.0    # cap zoom-in

    def __init__( self, scene: MapScene ) -> None:
        super().__init__(scene)
        self._scene = scene

        self.setMouseTracking(True)
        self.setRenderHint( QPainter.SmoothPixmapTransform, True)
        self.setDragMode( QGraphicsView.NoDrag)
        self.setHorizontalScrollBarPolicy( Qt.ScrollBarAsNeeded )
        self.setVerticalScrollBarPolicy( Qt.ScrollBarAsNeeded )
        self.setBackgroundBrush(Qt.darkGray)
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse )
        self.setResizeAnchor(QGraphicsView.AnchorViewCenter )
        self.setFocusPolicy( Qt.StrongFocus )

        # right-button drag is used for panning, so don't pop a context
        # menu when the user releases the right button.
        self.setContextMenuPolicy( Qt.NoContextMenu )

        # zoom & pan state
        self._fit_scale: float  = 1.0       # absolute m11 that means "fit"
        self._user_zoomed: bool = False    # has the user touched zoom yet?
        self._panning: bool     = False

        self._pan_last: QPoint | None = None

    # --- public API -------------------------------------------------------
    def fit_in_view(self) -> None:
        """
        Reset the transform so the entire scene fits the viewport.
        """
        self.resetTransform()
        self.fitInView(self._scene.sceneRect(), Qt.KeepAspectRatio )
        self._fit_scale     = self.transform().m11() or 1.0
        self._user_zoomed   = False
        self.zoomChanged.emit( 1.0 )

    #----------------------------
    def current_zoom(self) -> float:
        """Current zoom relative to fit-in-view (1.0 == fit)."""
        if self._fit_scale == 0:
            return 1.0
        return self.transform().m11() / self._fit_scale

    #----------------------------
    def center_on_latlon(self, lat: float, lon: float) -> None:
        """
        Scroll the viewport so (lat, lon) is at the center.
        Used by LatLongMap.set_cursor() so opening a dialog pre-positioned
        actually shows the point of interest.
        """
        x, y = self._scene.projection.latlon_to_pixel(lat, lon)
        self.centerOn(x, y)

    # --- Qt event hooks ---------------------------------------------------
    def wheelEvent(self, ev: QWheelEvent) -> None:
        delta = ev.angleDelta().y()
        if delta == 0:
            return
        factor = self.ZOOM_STEP if delta > 0 else 1.0 / self.ZOOM_STEP
        self._zoom_by(factor)
        ev.accept()

    #--------------------------------
    def mouseMoveEvent(self, ev: QMouseEvent) -> None:
        # Pan: drag the scene under the cursor.
        if self._panning and self._pan_last is not None:
            view_pos = self._view_pos(ev)
            delta    = view_pos - self._pan_last
            self._pan_last = view_pos
            h = self.horizontalScrollBar()
            v = self.verticalScrollBar()
            h.setValue(h.value() - delta.x())
            v.setValue(v.value() - delta.y())
            ev.accept()
            return

        # Hover: update crosshair + readout.
        x, y = self._scene_xy(ev)
        proj = self._scene.projection
        if proj.in_bounds(x, y):
            lat, lon = proj.pixel_to_latlon(x, y)
            self._scene.show_crosshair_at(x, y)
            self.coordsHovered.emit(lat, lon)
        else:
            self._scene.hide_crosshair()
            self.coordsCleared.emit()
        super().mouseMoveEvent(ev)

    #--------------------------------
    def mousePressEvent(self, ev: QMouseEvent) -> None:
        # Middle OR right button start a pan drag.  Right is the more
        # natural one-handed option; middle is kept for compatibility.
        if ev.button() in ( Qt.MiddleButton, Qt.RightButton ):
            self._panning       = True
            self._pan_last      = self._view_pos(ev)
            self.setCursor(Qt.ClosedHandCursor)
            ev.accept()
            return


        if ev.button() == Qt.LeftButton:
            x, y = self._scene_xy(ev)
            proj = self._scene.projection
            if proj.in_bounds(x, y):
                lat, lon = proj.pixel_to_latlon(x, y)
                self._scene.show_crosshair_at(x, y)
                self.coordsPicked.emit(lat, lon)

        super().mousePressEvent(ev)


    #--------------------------------
    def mouseReleaseEvent(self, ev: QMouseEvent) -> None:
        if ev.button() in ( Qt.MiddleButton, Qt.RightButton ) and self._panning:
            self._panning  = False
            self._pan_last = None
            self.unsetCursor()
            ev.accept()
            return
        super().mouseReleaseEvent(ev)


    #--------------------------------
    def leaveEvent(self, ev) -> None:
        self._scene.hide_crosshair()
        self.coordsCleared.emit()
        super().leaveEvent(ev)


    #--------------------------------
    def resizeEvent(self, ev: QResizeEvent) -> None:

        super().resizeEvent(ev)
        # Don't smash the user's zoom on every resize; only auto-fit until
        # the first user-initiated zoom.
        if not self._user_zoomed:
            self.fit_in_view()


    #--------------------------------
    def showEvent(self, ev) -> None:
        super().showEvent(ev)
        if not self._user_zoomed:
            self.fit_in_view()

    # --- helpers ----------------------------------------------------------
    def _zoom_by(self, factor: float) -> None:
        cur = self.current_zoom()
        target = max(self.MIN_ZOOM, min(self.MAX_ZOOM, cur * factor))
        actual = target / cur
        if abs(actual - 1.0) < 1e-6:
            return
        self.scale(actual, actual)
        self._user_zoomed = True
        self.zoomChanged.emit(target)


    #--------------------------------
    def _scene_xy(self, ev: QMouseEvent) -> tuple[float, float]:
        scene_pt = self.mapToScene(self._view_pos(ev))
        return scene_pt.x(), scene_pt.y()


    #--------------------------------
    @staticmethod
    def _view_pos(ev: QMouseEvent) -> QPoint:
        # Qt6 has ev.position() (QPointF); Qt5 has ev.pos() (QPoint).
        try:
            return ev.position().toPoint()
        except AttributeError:
            return ev.pos()


# ---- eof


