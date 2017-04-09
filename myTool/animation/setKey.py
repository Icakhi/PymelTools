# -*- coding: utf-8 -*-
from maya import cmds, mel
from PySide import QtGui
from ..lib import qt

class KeyButton(QtGui.QWidget):
	def __init__(self, *args, **kwargs):
		super(KeyButton, self).__init__(*args, **kwargs)
		
		layout = QtGui.QHBoxLayout()
		self.setLayout(layout)
		
		button = QtGui.QPushButton('Genga')
		button.clicked.connect(qt.Callback(setGengaKeyframe))
		layout.addWidget(button)
		
		button = QtGui.QPushButton('Douga')
		button.clicked.connect(qt.Callback(setDougaKeyframe))
		layout.addWidget(button)

class MainWindow(QtGui.QMainWindow):
	def __init__(self, parent=None):
		super(MainWindow, self).__init__(parent)
		self.setWindowTitle('Set Key')
		self.resize(180, 20)
		
		widget = KeyButton()
		self.setCentralWidget(widget)


def setGengaKeyframe():
	selection = cmds.ls(sl=True)
	if not selection:
		return
	
	mel.eval('SetKey')
	currentTime = cmds.currentTime(q=True)
	for node in selection:
		cmds.keyframe(node, tds=True, t=(currentTime,currentTime))
	
def setDougaKeyframe():
	# setKeyframe -breakdown 0 -hierarchy none -controlPoints 0 -shape 0 {"pSphere1"};
	selection = cmds.ls(sl=True)
	if not selection:
		return
	mel.eval('SetKey')
	
def main():
	app = MainWindow(qt.getMayaWindow())
	app.show()