#Author:Petra Mengistu
#Import the necessary libraries
import numpy as np 
import matplotlib.pyplot as plt
from math import factorial

#Define the function to estimate the Hermite polynomials for a given n and x
def Hermite(n,x):
	if n==0:
		H=1 #set the zeroth order polynomial equal to 1
	elif n==1:
		H=2*x #set the first order polynomial equal to 2x
	else:
		H=2*x*Hermite(n-1,x)-2*(n-1)*(Hermite(n-2,x)) #compute each respective polynomial by using recursion to call the previous two outputs for the function
	return H

#define a function to determine the values of the wave function for a given n and x
def psi(n,x):
	den=2**n*np.sqrt(np.pi)*factorial(n) #calculate the denominator of the expression in Newman
	wave=(np.exp(-0.5*x**2)/np.sqrt(den))*Hermite(n,x) #determine each value of the polynomial as a multiple of the Hermite polynomial for that same x and n.
	return wave

y1,y2,y3,y4=[],[],[],[] #initialize empty lists to store the values of the first four wavefunctions
xlist=[] #initialize a list to store the x values for the given range of -3 to 3
for x in np.linspace (-4,4,1100):
 	#determine the first four harmonics for each value of x
	h1=psi(0,x) #zeroth order harmonic
	h2=psi(1,x) #first order
	h3=psi(2,x) #second order
	h4=psi(3,x) #third order
 	#append the values of each four harmonics to the respective lists as labeled
	y1.append(h1)
	y2.append(h2)
	y3.append(h3)
	y4.append(h4)
	xlist.append(x)

#Plot each harmonic for the given range on the same plot.
plt.rc('text',usetex=True)
plt.rc('font', family='serif',serif='Palatino')

plt.xlabel("x",fontsize=16)
plt.ylabel(r'$\psi(x)$',fontsize=16)
plt.title("Superpostion of n=0-3 Harmonics for Quantum Oscillator")

plt.plot(xlist,y1,label="n=0")
plt.plot(xlist,y2, label="n=1")
plt.plot(xlist,y3, label="n=2")
plt.plot(xlist,y4, label="n=3")
plt.legend()
plt.savefig('ex5.13a.jpg',format='jpg',dpi=1000)#save the resulting figure as an image.
