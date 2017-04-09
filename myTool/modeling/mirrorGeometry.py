# -*- coding: utf-8 -*-
import os, json
from maya import cmds, OpenMaya
from PySide import QtGui
from ..lib import qt

class Settings(object):
	def __init__(self):
		temp = __name__.split('.')
		self.__filename = os.path.join(
			os.getenv('MAYA_APP_DIR'),
			temp[0],
			temp[-1]+'.json'
			)
		self.reset()
		self.read()
		
	def read(self):
		if os.path.exists(self.__filename):
			with open(self.__filename, 'r') as f:
				saveData = json.load(f)
				self.across = saveData['across']
				self.merge = saveData['merge']
				self.softEdge = saveData['softEdge']
				self.threshold = saveData['threshold']	
		
	def reset(self):
		self.across = 1
		self.merge = True
		self.softEdge = True
		self.threshold = 0.001	
		
	def save(self):
		saveData = { 'across':self.across,
			'merge':self.merge,
			'softEdge':self.softEdge,
			'threshold':self.threshold
			}
		if not os.path.exists(self.__filename):
			os.makedirs(os.path.dirname(self.__filename))
		with open(self.__filename, 'w') as f:
			json.dump(saveData, f)

settings = Settings()

class OptionWidget(QtGui.QWidget):
	def __init__(self, *args, **kwargs):
		super(OptionWidget, self).__init__(*args, **kwargs)
		mainLayout = QtGui.QFormLayout(self)
		
		xy = QtGui.QRadioButton('XY', self)
		yz = QtGui.QRadioButton('YZ', self)
		xz = QtGui.QRadioButton('XZ', self)
		
		acrossLayout = QtGui.QHBoxLayout(self)
		acrossLayout.addWidget(xy, True)
		acrossLayout.addWidget(yz, True)
		acrossLayout.addWidget(xz, True)
		
		mainLayout.addRow('Across', acrossLayout)
		
		self.__across = QtGui.QButtonGroup(self)
		self.__across.addButton(xy, 0)
		self.__across.addButton(yz, 1)
		self.__across.addButton(xz, 2)
		
		self.__marge = QtGui.QCheckBox('Merge', self)
		mainLayout.addRow('', self.__marge)
		
		self.__softEdge = QtGui.QCheckBox('Soft Edge', self)
		mainLayout.addRow('', self.__softEdge)
		
		self.__threshold = QtGui.QDoubleSpinBox(self)
		self.__threshold.setMinimum(0)
		self.__threshold.setMaximum(9999)
		self.__threshold.setDecimals(5)
		mainLayout.addRow('Threshold', self.__threshold)
		self.initialize()
		
	def initialize(self):
		self.__across.button(settings.across).setChecked(True)
		self.__marge.setChecked(settings.merge)
		self.__softEdge.setChecked(settings.softEdge)
		self.__threshold.setValue(settings.threshold)
		
	def resetSettings(self):
		settings.reset()
		self.initialize()	
		
	def saveSettings(self):
		settings.across = self.__across.checkedId()
		settings.merge = self.__marge.isChecked()
		settings.softEdge = self.__softEdge.isChecked()
		settings.threshold = self.__threshold.value()
		settings.save()		

	def apply(self):
		self.saveSettings()
		main()
	


class MainWindow(QtGui.QMainWindow):
	def __init__(self, *args, **kwargs):
		super(MainWindow, self).__init__(*args, **kwargs)
		self.setWindowTitle('Mirror Geometry')
		self.resize(400, 200)
		
		toolWidget = qt.ToolWidget(self)
		self.setCentralWidget(toolWidget)
		
		optionWidget = OptionWidget(self)
		toolWidget.setOptionWidget(optionWidget)

		toolWidget.setActionName(self.windowTitle())
		toolWidget.applied.connect(qt.Callback(optionWidget.apply))
		toolWidget.closed.connect(self.close)
		
		menuBar = self.menuBar()
		menu = menuBar.addMenu('File')
		action = menu.addAction('Save Settings')
		action.triggered.connect(optionWidget.saveSettings)
		
		action = menu.addAction('Reset Settings')	
		action.triggered.connect(optionWidget.resetSettings)		
			
def mirrorGeometry(node, across=0, merge=True, softEdge=True, threshold=0.001):
	shapes = cmds.listRelatives(node, s=True, pa=True)
	if not shapes:
		return False
	if cmds.objectType(shapes[0]) != 'mesh':
		return False
	shape = shapes[0]
	pivot = cmds.xform(node, q=True, ws=True, piv=True)
	
	if across == 0:
		direction = 4
		index = 2
	elif across == 1:
		direction = 0
		index = 0
	else:
		direction = 2
		index = 1
		
	kwargs = {}
	if merge:
		kwargs['mm']=True
		kwargs['mt']=threshold
	else:
		kwargs['mm']=False
		
	cmds.polyMirrorFace(shape, ws=True, d=direction, p=pivot[0:3], **kwargs)
	
	
	if softEdge:
		vertices = cmds.polyListComponentConversion(
			shape, fv=1, ff=1, fe=1, fuv=1, fvf=1, tv=1
			)
		vertices = cmds.ls(vertices, fl=True)
		
	centerVertices = []
	for vertex in vertices:
		pos = cmds.pointPosition(vertex, w=True)
		if abs(pivot[index] - pos[index]) <= threshold:
			centerVertices.append(vertex)
			
			
	centerEdges = []
	if centerVertices:
		centerEdges = cmds.polyListComponentConversion(
			centerVertices,
			fv=1, ff=1, fuv=1, fvf=1, te=1, internal=1
			)
	if centerEdges:
		cmds.polySoftEdge(centerEdges, a=180)
				

def option():
	window = MainWindow(qt.getMayaWindow())
	window.show()
	
def main():
	nodes = cmds.ls(sl=True, type='transform')
	if not nodes:
		OpenMaya.MGlobal.displayError('Select polygon to mirror geometry')
		return
	for node in nodes:
		mirrorGeometry(	
		node,
		settings.across,
		settings.merge,
		settings.softEdge,
		settings.threshold
		)
	OpenMaya.MGlobal.displayInfo('Done')