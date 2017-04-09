# -*- coding: utf-8 -*-
from maya import cmds

def main():
	cmds.menu(l='My Tool', p='MayaWindow', to=True)
	cmds.menuItem(l='General', to=True, sm=True, aob=True)
	cmds.menuItem(	l='Capture',
					c='from myTool.general import capture;capture.main()'
					)
	cmds.menuItem(	l='Copy Attribute',
					c='from myTool.general import copyAttribute;copyAttribute.main()'
					)
	
	cmds.setParent('..', m=True)
	cmds.menuItem(l='Modeling', to=True, sm=True, aob=True)
	cmds.menuItem(	l='Mirror Geometry',
					c='from myTool.modeling import mirrorGeometry;mirrorGeometry.main()'
					)
	cmds.menuItem(	l='Mirror Geometry Option',
					ob=True,
					c='from myTool.modeling import mirrorGeometry;mirrorGeometry.option()'
					)
	
	cmds.setParent('..', m=True)
	cmds.menuItem(l='Animation', to=True, sm=True, aob=True)
	cmds.menuItem(	l='Set Key',
					c='from myTool.animation import setKey;setKey.main()'
					)
					
	cmds.setParent('..', m=True)
	cmds.menuItem(l='Rigging', to=True, sm=True, aob=True)
	cmds.menuItem(	l='Transfar Weight',
					c='from myTool.rigging import transfarWeight;transfarWeight.main()'
					)
					
	cmds.setParent('..', m=True)
	cmds.menuItem(l='Rendering', to=True, sm=True, aob=True)
	cmds.menuItem(	l='Fresnel Shader',
					c='from myTool.rendering import fresnelShader;fresnelShader.main()'
					)