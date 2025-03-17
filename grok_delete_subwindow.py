#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 28 09:41:16 2025

@author: russ
"""


# ---- tof

# ---- imports

# ---- end imports


#-------------------------------






# ---- eof

I am programming in python with QT5


I have a window_menu        = menubar.addMenu( "Windows" )


i have a menubar = menuBar() and i add a
window_menu      = menubar.addMenu( "Windows" )

Then i add an action

window_menu.addAction( action )

Now given the action how do i delete the action from the menu?

grok

import sys

from PyQt5.QtWidgets import QAction, QApplication, QMainWindow, QMenuBar


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Remove Action Example")

        # Create the menu bar
        menubar = self.menuBar()

        # Add a "Windows" menu to the menu bar
        window_menu = menubar.addMenu("Windows")

        # Create an action
        self.action = QAction("My Action", self)
        self.action.triggered.connect(self.on_action_triggered)

        # Add the action to the menu
        window_menu.addAction(self.action)

        # Example: Remove the action (you can call this later, e.g., in a button click)
        # Uncomment the line below to remove it immediately
        # window_menu.removeAction(self.action)

    def on_action_triggered(self):
        print("Action triggered!")

    # Example method to remove the action later
    def remove_action(self):
        # Remove the action from the "Windows" menu
        window_menu = self.menuBar().findChild(QMenu, "Windows")
        window_menu.removeAction(self.action)
        print("Action removed from menu!")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()


===============================

