#Author: Petra Mengistu
#Import the necessary libraries
import numpy as np 
import matplotlib.pyplot as plt

def f(t):#Define the expression under the integral as a function
	f=np.e**(-t**2)
	return f

def E(b):
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
Elist=[] #initialize a list to store the approximated values of the integral for different values of x
xlist=[] #initialize a list to store the values of x
for b in np.arange (0,3,0.1): #set x to range from 0-3 with 0.1 increments
 	Elist.append(E(b)) #store the approximated values of the integral at each value of x
 	xlist.append(b)
#Set the font styles
plt.rc('text',usetex=True)
plt.rc('font', family='serif',serif='Palatino')

plt.xlabel("Values of X",fontsize=16)
plt.ylabel("Approximation of Integral E(x)",fontsize=16)
plt.plot(xlist,Elist) #plot the value of the integral as a function of x
plt.savefig('ex5.3.jpg',format='jpg',dpi=1000)#save the resulting figure as an image.
	