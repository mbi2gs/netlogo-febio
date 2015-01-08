# This script adds the logfile elements to the FEBio sim file
import sys

febioFileName = sys.argv[1]
datFileName = sys.argv[2]

febio = open(febioFileName,'r')
febioNewLines = []
inOutput = 0
for line in febio:
	if line.find('<Output>') > -1: #------OUTPUT-----------------------
		inOutput = 1
		febioNewLines.append(line)
	elif inOutput == 1:
		febioNewLines.append('\t\t<logfile>\n')
		# variables are listed here: http://help.mrl.sci.utah.edu/help/index.jsp?topic=/edu.utah.mrl.help.febio_um_1.7/html/3.12.1.html
		febioNewLines.append('\t\t\t<element_data data="sx;sy;sz" name="data" file="' + datFileName + '" delim=","/>\n')
		febioNewLines.append('\t\t</logfile>\n')
		inOutput = 0	
		febioNewLines.append(line)
	else:
		febioNewLines.append(line)
febio.close()

# Write new lines to file
febio = open(febioFileName,'w')
for nl in febioNewLines:
	febio.write(nl)
febio.close()