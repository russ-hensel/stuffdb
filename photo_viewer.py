#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 13 15:31:33 2024

@author: chat

photo_viewer.PhotoViewer()


"""
# --------------------
if __name__ == "__main__":
    import main
    main.main()
# --------------------

import sys
from PyQt5.QtWidgets import ( QApplication, QMainWindow,
 QGraphicsView, QGraphicsScene, QGraphicsPixmapItem,
 QVBoxLayout, QWidget, QPushButton, QDockWidget
 )
from PyQt5.QtGui import QPixmap, QPainter
from PyQt5.QtCore import Qt, QRectF

# ----QtWidgets
from PyQt5.QtWidgets import (
    QWidget,
    QPushButton,
    QAction,
    QDateEdit,
    QMenu,
    QAction,
    QLineEdit,
    QActionGroup,
    QApplication,
    QDockWidget,
    QTabWidget,
    QLabel,
    QListWidget,
    QMainWindow,
    QMessageBox,
    QSpinBox,
    QMdiSubWindow,
    QTextEdit,
    QButtonGroup,
    )



class PhotoViewer( QGraphicsView ):
    def __init__(self, parent=None):
        super(PhotoViewer, self).__init__(parent)
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)
        self.pixmap_item = QGraphicsPixmapItem()
        self.scene.addItem(self.pixmap_item)

        self.setRenderHint(QPainter.Antialiasing)
        self.setRenderHint(QPainter.SmoothPixmapTransform)
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QGraphicsView.AnchorUnderMouse)


    # -----------------------------
    def display_file( self,  file_name ):
        """
        what it says, read

        """
        pixmap      = QPixmap( file_name )
        ok          = self.set_pixmap( pixmap )
        if not ok:
            print( f"display_file error    { file_name = }")
        else:
            #rint( f"display_   { file_name = }")
            pass
        self.fit_in_view()

    # -----------------------------
    def set_pixmap( self, pixmap ):
        """
        what it says, but keep separate or merge into display_file
        pixmap may be useful for other viewer
        """
        if not pixmap.isNull():
            self.pixmap_item.setPixmap(pixmap)
            self.setSceneRect(QRectF(pixmap.rect()))  # Convert QRect to QRectF
            #rint(f"Image set: {pixmap.size()}")
            self.fit_in_view()  # Automatically fit the image to view when loaded\\\\\\
            return True
        else:
            print("Failed to load image pixmap is null")
            return False

    # -----------------------------
    def photo_1(self):
        self.display_file( "/mnt/WIN_D/PhotoDB/02/102-0253_img.jpg" )
    # -----------------------------
    def photo_2(self):
        self.display_file( "/mnt/WIN_D/PhotoDB/02/102_motor2.jpg" )

    def zoom_in(self):
        self.scale(1.2, 1.2)
        #p#rint("Zoomed In")
    # -----------------------------
    def zoom_out(self):
        self.scale(0.8, 0.8)
        #rint("Zoomed Out")

    def reset_zoom(self):
        self.resetTransform()
        #rint("Zoom Reset")

    def fit_in_view(self):
        self.fitInView(self.scene.sceneRect(), Qt.KeepAspectRatio)
        #rint("Fit in View")

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.fit_in_view()
        #rint("Window Resized and Image Fit in View")

    # -----------------------------
    def contextMenuEvent(self, event):
        context_menu        = QMenu(self)

        zoom_in_action      = context_menu.addAction("Zoom In")
        zoom_out_action     = context_menu.addAction("Zoom Out")
        reset_zoom_action   = context_menu.addAction("Reset Zoom")
        fit_in_view_action  = context_menu.addAction("Fit in View")

        photo_1_action      = context_menu.addAction("photo_1_action")
        photo_2_action      = context_menu.addAction("photo_2_action")

        action = context_menu.exec_(self.mapToGlobal(event.pos()))

        if action == zoom_in_action:
            self.zoom_in()
        elif action == zoom_out_action:
            self.zoom_out()
        elif action == reset_zoom_action:
            self.reset_zoom()
        elif action == fit_in_view_action:
            self.fit_in_view()
        elif action == photo_1_action:
            self.photo_1()
        elif action == photo_2_action:
            self.photo_2()
