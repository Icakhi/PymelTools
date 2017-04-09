# -*- coding: utf-8 -*-
import json
from maya import OpenMaya, cmds, mel
from PySide import QtCore, QtGui
from ..lib import qt

class StockItemModel(QtGui.QStandardItemModel):
	def __init__(self, parent=None):
		super(StockItemModel, self).__init__(0, 3, parent)
		self.setHeaderData(0, QtCore.Qt.Horizontal, 'Node')
		self.setHeaderData(1, QtCore.Qt.Horizontal, 'Attribute')
		self.setHeaderData(2, QtCore.Qt.Horizontal, 'Value')
	
	def appendItem(self, nodename, attrname, value):		
		nodeItem = QtGui.QStandardItem(nodename)
		nodeItem.setEditable(False)
		
		try:
			attrname = cmds.attributeName('%s.%s' % (nodename, attrname), l=True)
		except:
			pass
		
		attrItem = QtGui.QStandardItem(attrname)
		attrItem.setEditable(False)

		valueItem = QtGui.QStandardItem(str(value))	
		valueItem.setEditable(False)
		valueItem.setData(value)
		
		self.appendRow([nodeItem, attrItem, valueItem])
	
	def rowData(self, index):
		node  = self.item(index, 0).text()
		attr  = self.item(index, 1).text()
		value = self.item(index, 2).data()
		
		return (node, attr, value)
		
		
class StockerView(QtGui.QTreeView):
	mimeType = 'application/x-mytool-copyattribute-data'
	
	def __init__(self, *args, **kwargs):
		super(StockerView, self).__init__(*args, **kwargs)		
		self.setSelectionMode(QtGui.QTreeView.ExtendedSelection)
		self.setAlternatingRowColors(True)
		self.setRootIsDecorated(False)
	
	def removeSelectedItem(self):
		model	 = self.model()
		selModel = self.selectionModel()
		
		while selModel.selectedIndexes():
			indexes = selModel.selectedIndexes()
			model.removeRow(indexes[0].row())
	
	def keyPressEvent(self, event):
		if event.matches(QtGui.QKeySequence.Copy):
			self.copyToClipboard()
		
		elif event.matches(QtGui.QKeySequence.Paste):
			self.pasteFromClipboard()
		
		elif event.key() == QtCore.Qt.Key_Delete:
			self.removeSelectedItem()
			
		else:
			super(StockerView, self).keyPressEvent(event)
			
	def copyToClipboard(self):
		data    = []
		indexes = self.selectionModel().selectedIndexes()
		if not indexes:
			return
		
		for index in indexes:
			if index.column() != 0:
				continue
			
			data.append(self.model().rowData(index.row()))
		
		mimeData = QtCore.QMimeData()
		mimeData.setData(
			StockerView.mimeType,
			QtCore.QByteArray(json.dumps(data))
		)
		
		clipboard = QtGui.QApplication.clipboard()
		clipboard.setMimeData(mimeData)
	
	def pasteFromClipboard(self):
		clipboard = QtGui.QApplication.clipboard()
		mimeData  = clipboard.mimeData()
		if not mimeData.hasFormat(StockerView.mimeType):
			return
		
		datas = mimeData.data(StockerView.mimeType)
		datas = json.loads(str(datas))
		for data in datas:
			self.model().appendItem(data[0], data[1], data[2])

		
class OptionWidget(QtGui.QWidget):
	def __init__(self, *args, **kwargs):
		super(OptionWidget, self).__init__(*args, **kwargs)
		
		layout = QtGui.QGridLayout(self)
		
		stockerView = StockerView(self)
		layout.addWidget(stockerView, 0, 0, 1, 2)
		
		self.__model = StockItemModel(self)
		stockerView.setModel(self.__model)
		self.__selModel = QtGui.QItemSelectionModel(self.__model)
		stockerView.setSelectionModel(self.__selModel)
		
		button = QtGui.QPushButton('Copy', self)
		button.clicked.connect(qt.Callback(self.copy))
		layout.addWidget(button, 1, 0)
		
		button = QtGui.QPushButton('Paste', self)
		button.clicked.connect(qt.Callback(self.paste))
		layout.addWidget(button, 1, 1)
	
	def copy(self):
		self.__model.removeRows(0, self.__model.rowCount())
		
		cb = mel.eval('$temp=$gChannelBoxName;')
		nodeList = cmds.channelBox(cb, q=True, mol=True)
		attrList = cmds.channelBox(cb, q=True, sma=True)
		self.__setItems(nodeList, attrList)
		
		nodeList = cmds.channelBox(cb, q=True, sol=True)
		attrList = cmds.channelBox(cb, q=True, ssa=True)
		self.__setItems(nodeList, attrList)
		
		nodeList = cmds.channelBox(cb, q=True, hol=True),
		attrList = cmds.channelBox(cb, q=True, sha=True)
		self.__setItems(nodeList, attrList)
	
	def paste(self):
		indexes = self.__getIndexes()
		for index in indexes:
			if index.column() != 0:
				continue
			
			(node, attr, value) = self.__model.rowData(index.row())
			
			nodes = cmds.ls(sl=True)
			for node in nodes:
				if not cmds.attributeQuery(attr, n=node, ex=True):
					OpenMaya.MGlobal.displayError(
						'%s has not %s.' % (node, attr)
						)
					continue
				
				try:
					cmds.setAttr('%s.%s' % (node,attr), value)
				
				except:
					OpenMaya.MGlobal.displayError(
						'%s.%s : Failed to set value.' % (node,attr)
						)

	def __setItems(self, nodes, attrs):
		if not nodes or not attrs:
			return
		
		for node in nodes:
			for attr in attrs:
				value = cmds.getAttr('%s.%s' % (node, attr))
				self.__model.appendItem(node, attr, value)
				
	def __getIndexes(self):
		indexes = self.__selModel.selectedIndexes()
		if not indexes:
			row	 = self.__model.rowCount()
			indexes = []
			for i in range(row):
				indexes.append(self.__model.index(i,0))
		return indexes

class MainWindow(QtGui.QMainWindow):
	def __init__(self, *args, **kwargs):
		super(MainWindow, self).__init__(*args, **kwargs)
		self.setWindowTitle('Copy Attribute')
		self.resize(430, 260)
		
		optionWidget = OptionWidget(self)
		self.setCentralWidget(optionWidget)

def main():
	window = MainWindow(qt.getMayaWindow())
	window.show()