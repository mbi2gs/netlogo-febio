# Update FE material and simulation settings

import sys
import re

orderedFEfileName = sys.argv[1]
materialFileName = sys.argv[2]
febioFileName = sys.argv[3]

orderedFEfile = open(orderedFEfileName,'r')
materialFile = open(materialFileName,'r')

# Associate FE IDs with correct materials
oFEs = orderedFEfile.read().split()
mats = materialFile.read().split()
orderedFEfile.close()
materialFile.close()

# Re-Write FEBio simulation file with updated materials and 
# output settings
febio = open(febioFileName,'r')
febioNewLines = []
inElements = 0
for line in febio:
	if line.find('<Elements>') > -1: #------ELEMENTS---------------------
		inElements = 1
		febioNewLines.append(line)
	elif inElements == 1 and line.find('</hex8>') > -1:
		lineClean = line.rstrip().lstrip().replace('</hex8>','').replace('<hex8 id="','')
		lps = lineClean.split('"')
		elementID = lps[0].lstrip().rstrip()
		ordElIndex = oFEs.index(elementID)
		newMaterial = 'mat="' + mats[ordElIndex] + '">'
		newLine = re.sub('mat="\d+">', newMaterial, line)
		febioNewLines.append(newLine)
	elif line.find('</Elements>') > -1:
		inElements = 0	
		febioNewLines.append(line)
	else:
		febioNewLines.append(line)	
febio.close()

# Write new lines to file
febio = open(febioFileName,'w')
for nl in febioNewLines:
	febio.write(nl)
febio.close()