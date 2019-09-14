#region imports
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import pyqtSignal

import time
from datetime import datetime
from configparser import ConfigParser

from shlex import split
import argparse
import re
import sys
from CoreLib.AbsHandler import AbsHandler
from Utils.loaders import load_module, load_handlers
#endregion imports

font_but = QtGui.QFont()
font_but.setFamily("Segoe UI Symbol")
font_but.setPointSize(10)
font_but.setWeight(95)

class HandlerThread(QtCore.QThread):
    progress_signal = pyqtSignal(str)
    finish_signal = pyqtSignal(str)
    def __init__(self, installed_handlers, parent=None):
        QtCore.QThread.__init__(self, parent=None)
        self.installed_handlers = installed_handlers
        self.default_handler = self.installed_handlers['DefaultHandler']
        self.default_handler.set_notifications(self.progress_signal.emit, self.finish_signal.emit)
        self.selected_handler = self.default_handler
        for h in installed_handlers.values():
            h.set_notifications(self.progress_signal.emit, self.finish_signal.emit)
    def set_handler_params_string(self, params_string):
        self.handler_params_string = params_string
    def set_selected_handler(self, name_of_handler):
        self.selected_handler = self.installed_handlers.get(name_of_handler, self.default_handler)

    def run(self):
        self.selected_handler.start_handling(self.handler_params_string)

    def stop(self):
        self.selected_handler.stop_handling()
        #todo check if need to terminate the thread (and how to re-initialize the thread if it is terminated) - like self.terminate()

class PushBut1(QtWidgets.QPushButton):
    def __init__(self, parent=None):
        super(PushBut1, self).__init__(parent)
        self.setMouseTracking(True)
        self.setStyleSheet("margin: 1px; padding: 7px; background-color: rgba(1,255,255,100); color: rgba(0, 0, 0, 1); border-style: solid;"
                           "border-radius: 3px; border-width: 0.5px; border-color: rgba(127,127,255,255);")

    def enterEvent(self, event):
        if self.isEnabled() is True:
            self.setStyleSheet("margin: 1px; padding: 7px; background-color: rgba(1,255,255,100); color: rgba(0,230,255,255);"
                               "border-style: solid; border-radius: 3px; border-width: 0.5px; border-color: rgba(0,230,255,255);")
        if self.isEnabled() is False:
            self.setStyleSheet("margin: 1px; padding: 7px; background-color: rgba(1,255,255,100); color: rgba(0, 0, 0, 1); border-style: solid;"
                               "border-radius: 3px; border-width: 0.5px; border-color: rgba(127,127,255,255);")

    def leaveEvent(self, event):
        self.setStyleSheet("margin: 1px; padding: 7px; background-color: rgba(1,255,255,100); color: rgba(0, 0, 0, 1); border-style: solid;"
                           "border-radius: 3px; border-width: 0.5px; border-color: rgba(127,127,255,255);")
class QthreadApp(QtWidgets.QWidget):
    def __init__(self, parent=None):
        #region install handlers dynamically
        cur_settings = ConfigParser()
        cur_settings.read('settings.config')
        self.installed_handlers = load_handlers(cur_settings['general']['folder_with_handlers'], abs_class=AbsHandler)
        self.installed_handlers['DefaultHandler'] = load_module(cur_settings['general']['default_module_name'], cur_settings['general']['default_module_filepath'])

        self.handlers_names = list(self.installed_handlers.keys())
        self.handlers_descriptions = [h.get_description() for h in list(self.installed_handlers.values()) ]

        self.current_handler_name = 'DefaultHandler'
        self.currentHandler = self.installed_handlers[self.current_handler_name]
        self.currentHandlerIndex = self.handlers_names.index(self.current_handler_name)

        self.handler_thread = HandlerThread(self.installed_handlers)
        self.handler_thread.progress_signal.connect(self.on_progress_info)
        self.handler_thread.finish_signal.connect(self.on_finish_info)

        #region  setting window
        QtWidgets.QWidget.__init__(self, parent)
        self.setWindowTitle("GUI Application for various utilities (data handling, etc.)")
        self.setWindowIcon(QtGui.QIcon("Assets\\AppIcon.png"))
        self.setMinimumWidth(resolution.width() / 3)
        self.setMinimumHeight(resolution.height() / 1.5)
        self.setStyleSheet("QWidget {background-color: rgba(0,41,59,255);} QScrollBar:horizontal {width: 1px; height: 1px;"
                           "background-color: rgba(0,41,59,255);} QScrollBar:vertical {width: 1px; height: 1px;"
                           "background-color: rgba(0,41,59,255);}")
        #endregion

        #region for setting up handlers
        self.combHandlers = QtWidgets.QComboBox(self)
        self.combHandlers.setStyleSheet("margin: 1px; padding: 7px; background-color: rgba(0,255,255,1); color: rgba(0, 0, 0, 1);"
                                 "border-style: solid; border-radius: 3px; border-width: 0.5px; border-color: rgba(0,140,255,255);")
        #attach handler for selection of the combobox
        self.combHandlers.addItems(self.handlers_names)
        self.combHandlers.setCurrentIndex(self.currentHandlerIndex)
        self.combHandlers.activated.connect(self.onComboHandlersChange)
        #endregion
        
        #region various ui elements
        self.commandInfo = QtWidgets.QTextEdit(self)
        self.commandInfo.setEnabled(False)
        self.commandInfo.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        # self.commandInfo.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.commandInfo.setPlaceholderText("Selected command info")
        self.commandInfo.setStyleSheet("margin: 1px; padding: 7px; background-color: rgba(0,255,255,1); color: rgba(0, 0, 0, 1);"
                                 "border-style: solid; border-radius: 3px; border-width: 0.5px; border-color: rgba(0,140,255,255);")
        self.commandInfo.setPlainText(self.currentHandler.get_description())

        self.command_args_string = QtWidgets.QLineEdit(self)
        self.command_args_string.setPlaceholderText("Arguments/parameters for the selected handler")
        self.command_args_string.setStyleSheet("margin: 1px; padding: 7px; background-color: rgba(0,255,255,1); color: rgba(0, 0, 0, 1);"
                                 "border-style: solid; border-radius: 3px; border-width: 0.5px; border-color: rgba(0,140,255,255);")
        self.command_handling_info = QtWidgets.QTextEdit(self)
        self.command_handling_info.setPlaceholderText("Results...")
        self.command_handling_info.setEnabled(True) #False
        self.command_handling_info.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.command_handling_info.setStyleSheet("margin: 1px; padding: 7px; background-color: rgba(0,255,255,1); color: rgba(0, 0, 0, 1);"
                                 "border-style: solid; border-radius: 3px; border-width: 0.5px; border-color: rgba(0,140,255,255);")

        self.button_start = PushBut1(self)
        self.button_start.setText(u"\u25B6")
        self.button_start.setFixedWidth(72)
        self.button_start.setFont(font_but)

        self.butStop = PushBut1(self)
        self.butStop.setText(u"\u25A0")
        self.butStop.setFixedWidth(72)
        self.butStop.setFont(font_but)
        self.butStop.setEnabled(False)

        self.grid1 = QtWidgets.QGridLayout()

        self.grid1.addWidget(self.combHandlers, 0, 0, 1, 14)
        self.grid1.addWidget(self.commandInfo, 1, 0, 1, 14)
        self.grid1.addWidget(self.command_args_string, 2, 0, 1, 12)
        self.grid1.addWidget(self.button_start, 2, 12, 1, 1)
        self.grid1.addWidget(self.butStop, 2, 13, 1, 1)
        self.grid1.addWidget(self.command_handling_info, 3, 0, 143, 14)

        self.grid1.setContentsMargins(7, 7, 7, 7)
        self.setLayout(self.grid1)
        #endregion
        self.button_start.clicked.connect(self.on_butStart)
        self.butStop.clicked.connect(self.on_butStop)

    def onComboHandlersChange(self, selection_index):
        self.current_handler_name = self.handlers_names[selection_index]
        self.currentHandler = self.installed_handlers[self.current_handler_name]
        self.currentHandlerIndex = selection_index
        self.commandInfo.setPlainText(self.currentHandler.get_description())

    def switch_start_elements(self, state_enabled):
        self.button_start.setEnabled(state_enabled)
        self.combHandlers.setEnabled(state_enabled)
        self.command_args_string.setEnabled(state_enabled)

    def on_butStart(self):
        handler_input_string = self.command_args_string.text()
        self.command_handling_info.clear()
        self.command_handling_info.append(f'{str(datetime.now())} - starting [{self.currentHandlerName}] for [{handler_input_string}]')

        self.handler_thread.set_handler_params_string(handler_input_string)
        self.handler_thread.set_selected_handler(self.current_handler_name)
        self.handler_thread.start()
        #disable all the controls except for the stop button
        self.switch_start_elements(False)
        self.butStop.setEnabled(True)

    def on_butStop(self):
        try:
            self.handler_thread.stop()
            while self.handler_thread.isRunning():
                self.command_handling_info.append("Waiting to stop the work!")
                time.sleep(2)
            self.command_handling_info.append("Stopped!")
            self.switch_start_elements(True)
            self.butStop.setEnabled(False)
        except:
            pass

    def on_progress_info(self, info):
        self.command_handling_info.append(str(info))

    def on_finish_info(self, info):
        self.command_handling_info.append(str(info))
        self.butStop.setEnabled(False)
        self.switch_start_elements(True)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    desktop = QtWidgets.QApplication.desktop()
    resolution = desktop.availableGeometry()
    myapp = QthreadApp()
    myapp.setWindowOpacity(0.95)
    myapp.show()
    myapp.move(resolution.center() - myapp.rect().center())
    app.exec_()
else:
    desktop = QtWidgets.QApplication.desktop()
    resolution = desktop.availableGeometry()
