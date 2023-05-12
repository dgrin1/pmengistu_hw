
from random import random, randrange
from numpy import arange
import numpy as np
from pylab import plot,xlabel,ylabel,show
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.animation import FuncAnimation
from matplotlib.colors import LinearSegmentedColormap
from mengistu_petra_neighborfunct import neighbor,disatisfied, occupied, pltavg
from mengistu_petra_funcschellingnoswap import schelling
from mengistu_petra_funcschellingswap import schellings
#Run schelling model of constrained and unconstrained versions
disc11=schellings(50,50,553,1572,0.5)
disc12=schellings(50,50,553,1572,0.5)
disc13=schellings(50,50,553,1572,0.5)
dis1=pltavg(disc11,disc12,disc13)

disc21=schelling(50,50,553,1572,0.5)
disc22=schelling(50,50,553,1572,0.5)
disc23=schelling(50,50,553,1572,0.5)
dis2=pltavg(disc21,disc22,disc23)

disc31=schellings(50,50,488,1387,0.5)
disc32=schellings(50,50,488,1387,0.5)
disc33=schellings(50,50,488,1387,0.5)
dis3=pltavg(disc31,disc32,disc33)

disc41=schelling(50,50,488,1387,0.5)
disc42=schelling(50,50,488,1387,0.5)
disc43=schelling(50,50,488,1387,0.5)
dis4=pltavg(disc41,disc42,disc43)



tpoints1,tpoints2,tpoints3,tpoints4,tpoints5,tpoints6=[],[],[],[],[],[]
for i in range(len(dis1)):
	tpoints1.append(i)
for i in range(len(dis2)):
	tpoints2.append(i)
for i in range(len(dis3)):
	tpoints3.append(i)
for i in range(len(dis4)):
	tpoints4.append(i)

#Superpose on one plot
fig, ax = plt.subplots(figsize=(8, 7))
 
plt.rc('text',usetex=True)
plt.rc('font', family='serif',serif='Palatino')



plt.ylabel("$N_{Dissatisfied}$",fontsize=15) #set the x and y axes to x and r respectively
plt.xlabel("$N_{Rounds}$",fontsize=15)
plt.title(r"Comparison: 50x50 Solid and Liquid", fontsize=18)

plt.plot(tpoints1,dis1,'y-', label='Constrained; 15$\%$ empty')

plt.plot(tpoints2,dis2,'y--', label='Unconstrained; 15 $\%$ empty')

plt.plot(tpoints3,dis3, 'b-', label=r'Constrained; 25$\%$ empty')
plt.plot(tpoints4,dis4, 'b--', label=r'Unconstrained; 25$\%$ empty')


plt.legend()
plt.show()