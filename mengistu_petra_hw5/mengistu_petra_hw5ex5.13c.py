#Author: Petra Mengistu

#Import the necessary libraries
import numpy as np 
from gaussxw import gaussxw
import matplotlib.pyplot as plt
from math import factorial

N=100 #define the number of points used for Gaussian quadrature
a=-10 #set the lower limit of the integral as the maximum leftmost boundary of the x range
b=10 #set the upper limit of the integral as the maximum rightmost boundary of the x range
x,w = gaussxw(N) #define range of x and weights in Gaussian quadrature


xp = 0.5*(b-a)*x + 0.5*(b+a) #map the weights and x points according to the limits of integration
wp = 0.5*(b-a)*w
s = 0.0 #set the initial value of the integral equal to zero

wf=np.zeros((31,N)) #create an array to store the first 30 harmonics over the range of x
herm=np.zeros((31,N)) #create an array to store the first 30 Hermite polynomials for the given range of x
for n in range (31):
	if n==0:
		herm[n,:]=1 #set the zeroth order harmonic equal to 1
	elif n==1:
		herm[n,:]=2*xp #set the first order harmonic equal to 2x
	else:
		herm[n,:]=2*xp*herm[n-1,:]-2*(n-1)*herm[n-2,:] #compute each respective polynomial by using the previous two rows in the array


for n in range (31):
	den=2**n*np.sqrt(np.pi)*factorial(n) #define the denominator of the prefactor multiplying the hermite polynomial
	prefactor=(np.exp(-0.5*xp**2)/np.sqrt(den)) #collect the terms multiplying the Hermite polynomial into one common prefactor
	wf[n,:]=prefactor*herm[n,:] #compute each nth order harmonic by scaling the corresponding hermite polynomial by this prefactor



for k in range(N):
	s += wp[k]*xp[k]**2*(np.abs(wf[5,k]))**2 #determine the integral by summing over each product of the x terms scaled by the weights and the value of the integrand evaluated at each xterm.
print("Uncertainty:",np.sqrt(s))	#output the uncertainty, which is defined in Newman as the square root of the integral.

	
