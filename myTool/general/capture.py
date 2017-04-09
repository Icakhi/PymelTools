# -*- coding: utf-8 -*-
from maya import OpenMaya, OpenMayaUI, cmds


def save(filename):
	
	view  = OpenMayaUI.M3dView.active3dView()
	image = OpenMaya.MImage()
	view.readColorBuffer(image, True)
	
	try:
		temp = filename.split('.')
		format = temp[-1]
		image.writeToFile(filename, format)
	except:
		return False
	
	return True

def main():
	filename = cmds.fileDialog2(
					ds=2, cap='Save Image', fm=0,
					ff='*.bmp;;*.jpg;;*.png;;*.tif;;*.gif;;*.iff;;*.psd'
					)
	if not filename:
		return
	
	result = save(filename[0])
	if result:
		OpenMaya.MGlobal.displayInfo('Done!')
	else:
		OpenMaya.MGlobal.displayError('Failed to save picture.')
