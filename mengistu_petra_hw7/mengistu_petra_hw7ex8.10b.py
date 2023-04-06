#Author Petra Mengistu
from math import sin, cos
from numpy import array,arange
#from pylab import plot,xlabel,show
import matplotlib.pyplot as plt
import numpy as np
#Define the functions to be differentiated

def f(r,t): 
	G=6.67e-11 #gravitational constant, in N kg m/2^2
	M=1.989e30 #mass of the sun
	x = r[0] 
	y = r[1]
	a=np.sqrt(x**2+y**2) #distance from sun
	vx=r[2] #x speed of comet
	vy = r[3]  #y speed of comet
	fx = vx
	fy=vy
	fvx = -(G*M*x/a**3) 
	fvy = -(G*M*y/a**3)
	return array([fx,fy,fvx,fvy],float) #system of ODE

#set the initial and final times as 0 and roughly more than two periods (132 years).
a = 0.0
b = 4.73e9
N = 800000
h = (b-a)/N #define step size
print("Step size:", h)
tpoints = arange(a,b,h) #set the time to range from with steps of h.

xpoints,ypoints=[],[]
vxpoints,vypoints=[],[]

r = array([4.0e12,0,0,500],float) #set initial conditions
for t in tpoints:
    xpoints.append(r[0])
    ypoints.append(r[1])
    vxpoints.append(r[2])
    vypoints.append(r[3])
    k1 = h*f(r,t)#calculate the first guess using Euler's method
    k2 = h*f(r+0.5*k1,t+0.5*h)#approximate the next step at a time halfway between the current time and the next step
    k3 = h*f(r+0.5*k2,t+0.5*h)#repeat above approximation
    k4 = h*f(r+k3,t+h) #Use Euler's method to approximate the final x (using a Taylor expansion)
    r += (k1+2*k2+2*k3+k4)/6#the best approximation is the weighted sum of each approximation

#Set font styles
plt.figure(1)
plt.rc('text',usetex=True)
plt.rc('font', family='serif',serif='Palatino')

plt.plot(tpoints,xpoints) 
plt.xlabel("Time", fontsize=16)
plt.ylabel("X position", fontsize=16)
plt.figure(2)
plt.plot(xpoints,ypoints)
plt.xlabel("x position", fontsize=16)
plt.ylabel("y position", fontsize=16)
plt.show()
