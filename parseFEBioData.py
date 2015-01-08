# Extract data from FEBio output and arrange it for NetLogo to read in

import sys

inputDataFileName = sys.argv[1]
outputDataFileName = sys.argv[2]
elementOrderFileName = sys.argv[3]

idf = open(inputDataFileName,'r')
odf = open(outputDataFileName,'w')
eof = open(elementOrderFileName,'r')

EO = eof.read().split()

# Count number of time steps in data file
steps = 0
for line in idf:
	if line.find('*Step  =') > -1:
		steps += 1
idf.close()

# Grab data from last time step
orderedData = [0] * len(EO)
idf = open(inputDataFileName,'r')
inLast = 0
for line in idf:
	if line.find('*Step  = ' + str(steps)) > -1:
		inLast = 1
	elif inLast == 1 and line.find('Time') == -1 and line.find('Data') == -1 and len(line) > 2:
		lps = line.split(',')
		elID = lps[0]
		sumStress = float(lps[1])# + float(lps[2]) + float(lps[3])
		elIndex = EO.index(elID)
		orderedData[elIndex] = sumStress

# Write last time step data to file
for data in orderedData:
	odf.write(str(data) + ' ')

eof.close()
idf.close()
odf.close()