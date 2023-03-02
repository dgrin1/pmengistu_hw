#Author: Petra Mengistu
#Import the necessary libraries
import numpy as np 
from gaussxw import gaussxw
import matplotlib.pyplot as plt

def f(t):#Define the expression under the integral as a function
	f=np.e**(-t**2)
	return f

def Esimp(b):
	a=0#set the lower limit of integration
	N=63 #use the value of N determined from observing error convergence
	h=(b-a)/N #set the width of each slice
	sum_odd,sum_even=0,0 #initialize the sum of the terms representing the values of the function evaluated at odd and even multiples as zero
	for i in np.arange (1,N/2):
		sum_odd+=f(a+(2*i-1)*h)#add each value of the function at an odd multiple slice from the lower limit to its preceding value
	for j in np.arange (1,N/2-1):
		sum_even+=f(a+2*j*h)#add each value of the function at an even multiple slice from the lower limit to its preceding value
	I=h/3*(f(a)+f(b)+4*sum_odd +2*sum_even) #implement Newman eq 5.10 to determine an approximation of the integral

	return I #output the approximation using Simpson's rule

def Egauss(b):
	a=0 #set the lower limit of integration
	N=63 #use the same number of points as simpson for comparison
	x,w = gaussxw(N) #determine sample points and weights 
	xp = 0.5*(b-a)*x + 0.5*(b+a) #map points and weights onto region of integration
	wp = 0.5*(b-a)*w
	s = 0.0 #initialize value of integral as zero
	for k in range(N):
		s += wp[k]*f(xp[k]) #integral is approximated by the sum of the function evaluated at a given point scaled by the corresponding weight for all points in the sample
	return s #output the approximation of integral
	
Elgauss,Elsimp=[],[] #initialize a list to store the approximated values of the integral for different values of x
xlist=[] #initialize a list to store the values of x
for b in np.arange (0,3,0.1): #set x to range from 0-3 with 0.1 increments
 	Elgauss.append(Egauss(b)) #store the approximated values of the integral at each value of x
 	Elsimp.append(Esimp(b)) #store the approximated values of the integral at each value of x
 	xlist.append(b)
#Set the font styles
plt.rc('text',usetex=True)
plt.rc('font', family='serif',serif='Palatino')

plt.xlabel("Values of X",fontsize=16)
plt.ylabel("Approximation of Integral E(x)",fontsize=16)
plt.plot(xlist,Elgauss, label="Gaussian Quadrature Approximation") #plot the value of the integral as a function of x
plt.plot(xlist,Elsimp, label="Simpson's Rule Approximation") #plot the value of the integral as a function of x
plt.legend()
plt.savefig('ex25.3.jpg',format='jpg',dpi=1000)#save the resulting figure as an image.
	