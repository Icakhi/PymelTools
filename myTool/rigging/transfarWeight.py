# -*- coding: utf-8 -*-
from maya import cmds

def main():
	selection = cmds.ls(sl=True)
	if not selection or len(selection) <= 1:
		cmds.error('Must select a source and a destination skin.')
		
	shapes = cmds.listRelatives(selection[0], s=True, pa=True, type='mesh')
	if not shapes:
		cmds.error('Node has not shape.')#要英語訳の確認
		
	srcSkinCluster = cmds.listConnections(shapes[0]+'.inMesh', s=True, d=False)
	if not srcSkinCluster:
		cmds.error('Select a node that has a skin cluster applied.')
		
	srcSkinCluster = srcSkinCluster[0]
	skinningMethod = cmds.getAttr(srcSkinCluster+'.skm')
	dropoffRate = cmds.getAttr(srcSkinCluster+'.dr')
	maintainMaxInfluences = cmds.getAttr(srcSkinCluster+'.mmi')
	maxInfluences = cmds.getAttr(srcSkinCluster+'.mi')
	bindMethod = cmds.getAttr(srcSkinCluster+'.bm')
	normalizeWeights = cmds.getAttr(srcSkinCluster+'.nw')
	influences = cmds.skinCluster(srcSkinCluster, q=True, inf=True)
		
	for dst in selection[1:]:
		shapes = cmds.listRelatives(dst, s=True, pa=True, type='mesh')
		if not shapes:
			continue

		dstSkinCluster = cmds.listConnections(	shapes[0]+'.inMesh',
												s=True,
												d=False
												)									
		if not dstSkinCluster:
			dstSkinCluster = cmds.skinCluster(
								dst,
								influences,
								omi=maintainMaxInfluences,
								mi=maxInfluences,
								dr=dropoffRate,
								sm=skinningMethod,
								nw=normalizeWeights,
								tsb=True,
								)
		dstSkinCluster = dstSkinCluster[0]
		
		cmds.copySkinWeights(
					ss=srcSkinCluster,
					ds=dstSkinCluster,
					surfaceAssociation='closestPoint',
					influenceAssociation=['name', 'closestJoint', 'oneToOne'],
					normalize=True,
					noMirror=True
					)
					
		print 'Transfar skin weight ' + selection[0] + '>' + dst