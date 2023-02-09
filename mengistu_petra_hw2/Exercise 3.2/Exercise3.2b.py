#Author:Petra Mengistu

#Import the necessary libraries, and functions from these libraries
import matplotlib.pyplot as plt
from numpy import linspace
from math import sin, cos, pi,exp
#Initialize x and y values as empty lists to have the appropriate data points appended to them
x = []
y = []
for theta in linspace(0,10*pi, 5000): #set theta to range from 0 to 24pi, while choosing an appropriately small set of separation values using the linspace function
	r=theta**2 #polar form of Galileo's spiral
	xpoint,ypoint=r*cos(theta),r*sin(theta)#determine the x and y values in coordinate form and append them to the initial lists for each value of theta
	x.append(xpoint)
	y.append(ypoint)
plt.plot(x,y,'-')#Plot all values of y against all values of x.
plt.title("Galileo's Spiral")#set title of figure
plt.xlabel(r'$x=r\cos \theta$',fontsize=16)#Define the labels as the polar form of x and y Cartesian coordinates.
plt.ylabel(r'$y=r\sin \theta$',fontsize=16)
plt.savefig('ex3.2b.jpg',format='jpg',dpi=1000)#save the resulting figure as an image.
