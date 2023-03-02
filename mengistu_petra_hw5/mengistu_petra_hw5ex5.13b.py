#Author: Petra Mengistu

#Import the necessary libraries
import numpy as np 

import matplotlib.pyplot as plt
from math import factorial



x =np.linspace(-10,10,1100)
wf=np.zeros((31,len(x)))  #create an array to store the first 30 harmonics over the range of x
herm=np.zeros((31,len(x))) #create an array to store the first 30 Hermite polynomials for the given range of x

for n in range(31):
	if n==0:
		herm[n,:]=1 #set the zeroth order harmonic as 1
	elif n==1:
		herm[n,:]=2*x #set the first order harmonic as 2x
	else:
		herm[n,:]=2*x*herm[n-1,:]-2*(n-1)*herm[n-2,:] #compute each respective polynomial by using the previous two rows in the array


for n in range (31):
	den=2**n*np.sqrt(np.pi)*factorial(n)  #define the denominator of the prefactor multiplying the hermite polynomial
	prefactor=(np.exp(-0.5*x**2)/np.sqrt(den))   #collect the terms multiplying the Hermite polynomial into one common prefactor
	wf[n,:]=prefactor*herm[n,:]  #compute each nth order harmonic by scaling the corresponding hermite polynomial by this prefactor

y=(wf[30,:]) #define the y values as the wavefunction of the 30th order harmonic over the entire range of x from -10 to 10.




plt.rc('text',usetex=True)
plt.rc('font', family='serif',serif='Palatino')

plt.xlabel("x",fontsize=16)
plt.ylabel(r'$\psi(x)$',fontsize=16)
plt.title("n=30 Harmonic for Quantum Oscillator")
plt.plot(x,y)
plt.savefig('ex5.13.jpg',format='jpg',dpi=1000)#save the resulting figure as an image.