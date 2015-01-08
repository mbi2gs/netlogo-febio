## netlogo-febio
A set of example scripts to integrate the Netlogo and FEBio modeling frameworks

## WHAT IS IT?

An example of how to integrate FEBio (a software package for finite element analysis) and NetLogo (a software package for agent-based modeling). 

## WHY?

ABMs and FE models have different strengths. ABMs are good at representing heterogeneous systems with independent agents that make decisions based on discrete and even complex rules. FE models, on the other hand, are good at representing the mechanical properties of relatively homogeneous systems. 
There are cases that crop up now and again that require representations of both types of systems. For example, after a heart attack, the dead tissue begins to form a scar. The direction of scar fiber alignment, the shape, etc. will change the mechanical properties of the heart, but at the same time, the constant motion of the heart exerts forces on the injured region of tissue that impact the fiber alignment and shape of the scar. Such complex feedback loops between the macro scale (muscle tissue) and the micro scale (immune and remodeling cells) require multi-scale models. 
Rather than re-invent the wheel, it would be convenient to use existing, proven tools to create multi-scale models (at least for proof-of-concept studies). This example code does not represent a real system, but is instead an example of how NetLogo and FEBio can be integrated into a single modeling tool.

## HOW IT WORKS

The communication between NetLogo and FEBio is essentially a text-processing problem, and so the majority of the communication is handled by a series of Python scripts (easy text parsing!).

This is a 2D simulation of a square of elastic material ("Mooney-Rivlin solid" in FEBio). The square is divided into 30x30 patches in NetLogo, corresponding to 30x30 elements in FEBio. Two material types ("1" and "2") were defined in an FEBio simulation file beforehand, one stiffer, and one more elastic. As the simulation progresses, the patches change material based on the stress they experience. The time step is also defined beforehand in the FEBio simulation file (which I created through the FEBio GUI).

One cycle of the simulation follows these steps:
1) NetLogo updates the material composition of each patch based on the current strain experienced. The update rule causes a patch to adopt material "1" if its strain is greater than the average strain of its neighbors. Otherwise, it adopts material "2".
2) The new material for each patch is written to a text file
3) NetLogo calls a Python script ("updateFEBioSim.py") that re-writes the FEBio simulation file with the new material IDs as determined in steps 1 and 2
4) NetLogo calls FEBio, and runs the FEBio simulation. Results from the simulation are written to "dataFile.txt", as defined in the simulation file under the "<Output>" elements
5) NetLogo calls a Python script that parses the simulation results (the strain from the last time step) in "dataFile.txt", and re-writes them to a new file, in the correct order for NetLogo to read in and assign to patches
6) NetLogo reads in the new strains and updates the patch colors

## HOW TO USE IT

1) Install NetLogo
2) Install Python
3) Download FEBio and put the executable in a folder called "FEBio1p8". Put that folder in the same directory with the NetLogo file "testNL_and_FEBio.nlogo"
4) Open "testNL_and_FEBio.nlogo"
5) Press the "Setup" button
6) Press the "Go" button to advance one or more time steps. 

## THINGS TO NOTICE

Eventually the system reaches a sort of oscillating equilibrium.

## THINGS TO TRY

Change the patch update rules, the material types, etc. 

## DETAILS

This simulation was tested on a Windows 7 machine, running NetLogo 5.0.4, FEBio 1.8, and Python 2.7.

## CREDITS AND REFERENCES

This example was prepared by Matt Biggs (mb3ad[at]virginia[dot]edu).

FEBio: http://febio.org/febio/
NetLogo: https://ccl.northwestern.edu/netlogo/
Python: https://www.python.org/
