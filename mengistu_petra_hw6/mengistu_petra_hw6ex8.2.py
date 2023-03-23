from math import sin, cos
from numpy import array,arange
#from pylab import plot,xlabel,show
import matplotlib.pyplot as plt
import numpy as np
def f(r,t):
	#define the given constants (units of 1/s)
	G=0.5
	A=1
	B=0.5
	D=2
	x= r[0] #set the number of rabbits to be the first column of vector 'r'
	y = r[1] #set the number of foxes to be the second column of vector 'r'
	fx = A*x-B*x*y #code the given differential equations
	fy = G*x*y-D*y
	return array([fx,fy],float) 

#Set the time to range for 30 seconds
a = 0.0
b = 30.0
N = 2000
h = (b-a)/N #set step size

tpoints = arange(a,b,h)

ypoints = [] #initialize list to store amount of foxes at given time

r = array([2,2],float)
xpoints = [] #initialize list to store amount of rabbits at a given time.
for t in tpoints:
	xpoints.append(r[0])#store the value of the first column of r for each time point
	ypoints.append(r[1])#store the value of the second column of r for each time point
	k1 = h*f(r,t)#calculate the first guess using Euler's method
	k2 = h*f(r+0.5*k1,t+0.5*h)#approximate the next step at a time halfway between the current time and the next step
	k3 = h*f(r+0.5*k2,t+0.5*h)#repeat above approximation
	k4 = h*f(r+k3,t+h) #Use Euler's method to approximate the final x (using a Taylor expansion)
	r += (k1+2*k2+2*k3+k4)/6#the best approximation is the weighted sum of each approximation

plt.figure(1)
#Set the font styles
plt.rc('text',usetex=True)
plt.rc('font', family='serif',serif='Palatino')

plt.plot(tpoints,xpoints, label="Rabbits") 
plt.plot(tpoints,ypoints, label="Foxes")
plt.title("Predator-Prey Relationship")
plt.xlabel("Time",fontsize=16)
plt.ylabel("Populations of Species",fontsize=16)

plt.legend()
plt.show()