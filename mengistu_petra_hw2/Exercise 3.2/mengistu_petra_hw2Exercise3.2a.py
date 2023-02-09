#Author:Petra Mengistu

#Import the necessary libraries
import matplotlib.pyplot as plt
from numpy import linspace
from math import sin, cos, pi
#Initialize x and y values as empty lists to have the appropriate data points appended to them
x = []
y=[]
for theta in linspace(0,2*pi, 100):#set theta to range from 0-2*pi
	xpoint=2*cos(theta)+cos(2*theta)#individual calculation of the parametric expression for x
	x.append(xpoint)#append each calculation to the initial list
	ypoint=2*sin(theta)-sin(2*theta) #individual calculation of the parametric expression for y
	y.append(ypoint)#append each calculation to the initial list for y

plt.rc('text',usetex=True)#import LaTeX text styles
plt.rc('font', family='serif',serif='Palatino')


plt.plot(x,y)#plot all values of y against all values of x
plt.title("Deltoid Curve")#set title of figure
plt.xlabel(r'$x=2\cos\theta + \cos 2\theta$',fontsize=16)#Define the labels as the x and y parametric equations
plt.ylabel(r'$y=2\sin\theta - \sin 2\theta$',fontsize=16)#save the resulting figure as an image.
plt.savefig('ex3.2.jpg',format='jpg',dpi=1000)
