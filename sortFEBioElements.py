# read in FEBio file and sort the elements such that they
# are in the same order as the netlogo patches will be.
# write the ordered element IDs to a file
import sys

febioName = sys.argv[1]
outputName = sys.argv[2]
febio = open(febioName, 'r')

inNodes = 0
nodeids = []
nodex = []
nodey = []
s_nodeInfo = []

inElements = 0
elementIDs = []
elementNodeList = []

for line in febio:
	#------NODES------------------------
	if line.find('<Nodes>') > -1:
		inNodes = 1
	# Find node positions
	if inNodes == 1 and line.find('0.0000000e+000</node>') > -1:
		lineClean = line.rstrip().lstrip().replace(', 0.0000000e+000</node>','').replace('<node id="','')
		lps = lineClean.split('"')
		nodeID = int(lps[0])
		xys = lps[1].lstrip('">').split(',')
		x = float(xys[0])
		y = float(xys[1])
		nodeids.append(nodeID)
		nodex.append(x)
		nodey.append(y)
	# Sort nodes by y, then by x (so that we can iterate over the elements by row (left-to-right, top-to-bottom)
	if line.find('</Nodes>') > -1:
		inNodes = 0
		nodeInfo = zip(nodex,nodey,nodeids)
		# sort by y's, then by x's
		s_nodeInfo = sorted(nodeInfo, key=lambda x: (-x[1], x[0]))
	
	#------ELEMENTS---------------------
	if line.find('<Elements>') > -1:
		inElements = 1
	# 
	if inElements == 1 and line.find('</hex8>') > -1:
		lineClean = line.rstrip().lstrip().replace('</hex8>','').replace('<hex8 id="','')
		lps = lineClean.split('"')
		elementID = int(lps[0].lstrip().rstrip())
		elementNodes = lps[3].lstrip('>').lstrip().split(',')
		elementNodes = [int(x.lstrip().rstrip()) for x in elementNodes ]
		elementIDs.append(elementID)
		elementNodeList.append(elementNodes)
	# 
	if line.find('</Elements>') > -1:
		inElements = 0	
febio.close()


# Sort nodes into rows so that it's easier to grab the four nodes that belong to an element
nodeMat = []
curY = max(nodey)
tmpRow = []
for node in s_nodeInfo:
	if node[1] == curY:
		tmpRow.append(node)
	else:
		nodeMat.append(tmpRow)
		curY = node[1]
		tmpRow = []
		tmpRow.append(node)
nodeMat.append(tmpRow)

# ftmp = open('sortedNodes.txt','w')
# for row in nodeMat:
	# ftmp.write(str(row) + '\n')
# ftmp.close()
		
elementOrder = []
#iterate over the elements by row (left-to-right, top-to-bottom) and write to file in correct order
for i in range(len(nodeMat) - 1):
	for j in range(len(nodeMat[0])-1):
		nodesInElement = [ nodeMat[i+1][j][2],  nodeMat[i+1][j+1][2], nodeMat[i][j+1][2], nodeMat[i][j][2] ]
		for k in range(len(elementNodeList)):
			curElement = elementNodeList[k][0:4]
			if curElement == nodesInElement:
				elementOrder.append(elementIDs[k])

fout = open(outputName,'w')
for el in elementOrder:
	fout.write(str(el) + ' ')
fout.close()
				

