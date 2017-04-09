# -*- coding: utf-8 -*-
from maya import cmds

def main():
	samplerInfoList = cmds.ls(type='samplerInfo')
	if not samplerInfoList:
		samplerInfo = cmds.shadingNode('samplerInfo', asUtility=True)
	else:
		samplerInfo = samplerInfoList[0]
	
	ramp = cmds.shadingNode('ramp', n='fresnel_ramp', asTexture=True)
	cmds.removeMultiInstance(ramp+'.colorEntryList[2]', b=True)
	cmds.setAttr(ramp+'.colorEntryList[0].color', 1, 1, 1)
	cmds.setAttr(ramp+'.colorEntryList[0].position', 0)
	cmds.setAttr(ramp+'.colorEntryList[1].color', 0, 0, 0)
	cmds.setAttr(ramp+'.colorEntryList[1].position', 0.6)
	cmds.connectAttr(samplerInfo+'.facingRatio', ramp+'.vCoord')
	
	material = cmds.shadingNode('surfaceShader', n='fresnel_MT', asShader=True)
	cmds.connectAttr(ramp+'.outColor', material+'.outColor')
	
	sg = cmds.sets(r=True, nss=True, em=True, n=material+'SG')
	cmds.connectAttr(material+'.outColor', sg+'.surfaceShader')