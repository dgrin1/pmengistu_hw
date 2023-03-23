#Author: Petra Mengistu
#Import the necessary libraries
from math import sin, cos
from numpy import array,arange
import matplotlib.pyplot as plt
import numpy as np

def f(r,t):
	om=5 #driving frequency in rad/sec - for part b, change this number to 9.479 rad/sec
	g=9.81 #gravity, in m/s^2
	l=0.1 #length of the pendulum, in meters
	C=2 #given constant, in inverse seconds squared
	theta = r[0] #for a vector 'r' containing the solutions to the two differential equations, set the angles as the first column of 'r'
	w = r[1] #set the angular velocity (second differential equation solution) equal to the second column of vector 'r'
	ftheta = w #code first differential equation, definition, of angular velocity
	fw = -(g/l)*sin(theta) +C*cos(theta)*sin(om*t) #code second differential equation, where 'om ' is the driving frequency of the pendulum
	return array([ftheta,fw],float) #output the vector

#set the initial and final times as 0 and a 100.
a = 0.0
b = 100.0
N = 80000
h = (b-a)/N #define step size

tpoints = arange(a,b,h) #set the time to range from 0-100 with steps of h.

ypoints = [] #initialize the list to store the values of the angular velocities

r = array([0,0],float) #set the initial conditions
xpoints = [] #initialize the list to store the angles at each point in time
for t in tpoints:
	xpoints.append(r[0])#store the value of the first column of r for each time point
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
plt.title(r'$\theta (t) \mathrm{vs Time}$')
plt.xlabel("Time", fontsize=16)
plt.ylabel(r'$\theta (t)$',fontsize=16)
plt.show()