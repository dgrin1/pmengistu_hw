#Author: Petra Mengistu
#Import the necessary libraries
from math import sin
from numpy import array,arange
import matplotlib.pyplot as plt
import numpy as np

def f(r,theta):
	g=9.81 #gravity, im m/s^2
	l=0.1 #length of pendulum, in meters
	theta = r[0] #for a vector 'r' containing the solutions to the two differential equations, set the angles as the first column of 'r'
	w = r[1] #set the angular velocity (second differential equation solution) equal to the second column of vector 'r'
	ftheta = w #code first differential equation, definition of angular velocity
	fw = -(g/l)*sin(theta) #define second differential equation, equivalent of angular acceleration
	return array([ftheta,fw],float)
#set the initial and final times as 0 and 100.
a = 0.0
b = 10.0
N = 1000
h = (b-a)/N

tpoints = arange(a,b,h) #set the time to range from 0-100 with steps of h.
 #initialize lists to store the values of the angular velocities and displacements
ypoints = []
xpoints = []


r = array([np.pi*(179/180),0],float) #set initial conditions
for t in tpoints:
    xpoints.append(r[0])
    ypoints.append(r[1])#store the value of the second column of r for each time point
    k1 = h*f(r,t)#calculate the first guess using Euler's method
    k2 = h*f(r+0.5*k1,t+0.5*h)#approximate the next step at a time halfway between the current time and the next step
    k3 = h*f(r+0.5*k2,t+0.5*h)#repeat above approximation
    k4 = h*f(r+k3,t+h) #Use Euler's method to approximate the final x (using a Taylor expansion)
    r += (k1+2*k2+2*k3+k4)/6#the best approximation is the weighted sum of each approximation

#Set the font styles
plt.rc('text',usetex=True)
plt.rc('font', family='serif',serif='Palatino')

plt.figure(1)
plt.plot(tpoints,xpoints) #Plot the angles as a function of time


plt.xlabel("Time",fontsize=16)
plt.ylabel(r'$\theta (t)$',fontsize=16)

plt.xlabel("t")
plt.show()
