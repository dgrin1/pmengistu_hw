from math import sin, cos
from numpy import array,arange
#from pylab import plot,xlabel,show
import matplotlib.pyplot as plt
import numpy as np
#Define the functions to be differentiated
def f(om,r,t): #take in driving frequency as an input
	g=9.81 #gravity, in m/s^2
	l=0.1 #length of the pendulum, in meters
	C=2 #given constant, in inverse seconds squared
	theta = r[0] #for a vector 'r' containing the solutions to the two differential equations, set the angles as the first column of 'r'
	w = r[1] #set the angular velocity (second differential equation solution) equal to the second column of vector 'r'
	ftheta = w #code first differential equation, definition, of angular velocity
	fw = -(g/l)*sin(theta) +C*cos(theta)*sin(om*t) #code second differential equation, where 'om ' is the driving frequency of the pendulum
	return array([ftheta,fw],float)

#set the initial and final times as 0 and a 100.
a = 0.0
b = 100.0
N = 80000
h = (b-a)/N #define step size

tpoints = arange(a,b,h) #set the time to range from 0-100 with steps of h.

freq=[] #initialize lists to store the frequencies and maximum amplitudes to determine where the system achieves resonance
amps=[]


for i in arange(7,11,0.01): #set a range of driving frequencies
	om=i 
	freq.append(om)#store the value of each frequency
	xpoints = [] #initialize a list to store the amplitudes of oscillation for each time point.
	ypoints = [] #initialize a list to store the velocities for each time point
	r = array([0,0],float) #set the initial conditions
	for t in tpoints:
		xpoints.append(r[0]) #store the value of the first column of r for each time point
		ypoints.append(r[1]) #store the value of the second column of r for each time point
		k1 = h*f(om,r,t) #calculate the first guess using Euler's method
		k2 = h*f(om,r+0.5*k1,t+0.5*h) #approximate the next step at a time halfway between the current time and the next step
		k3 = h*f(om,r+0.5*k2,t+0.5*h) #repeat above approximation
		k4 = h*f(om,r+k3,t+h) #Use Euler's method to approximate the final x (using a Taylor expansion)
		r += (k1+2*k2+2*k3+k4)/6 #the best approximation is the weighted sum of each approximation
	amps.append(np.max(xpoints)) #store the maximum amplitude for each x(t) determined at a given driving frequency 

#Set font styles
plt.figure(1)
plt.rc('text',usetex=True)
plt.rc('font', family='serif',serif='Palatino')

plt.plot(freq,amps) #plot amplitudes over the range frequencies and select frequency at which amplitude is largest as the resonant frequency.

plt.title("Amplitude against Driving Frequency")
plt.ylabel("Max. amplitude of oscillation (rad)",fontsize=16)
plt.xlabel("Driving frequency (rad/s)", fontsize=16)
plt.show()
