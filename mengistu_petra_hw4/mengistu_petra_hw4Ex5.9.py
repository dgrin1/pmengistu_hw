#Author: Petra Mengistu
#Import the necessary libraries
import numpy as np
import matplotlib.pyplot as plt


#Define the integrand given in the problem as a function to apply Simpson's rule
def f(x):
	if x==0: #In the limit that x goes to zero, f also approaches zero. To avoid the issue of dividing the zero and the code halting, set f=0 as x becomes infinitely small
		f=0
	else:
		f=(x**4*np.e**x)/(np.e**x-1)**2 #expression in Integrand
	return f

def cv(T):
	#Define the constants used in the problem
	kb=1.3806e-23 #boltzmann constant, in units of J/K
	V=1000e-6 #where v is the volume, given in cubic centimeters and the factor of 10^-6 is applied to convert to cubic meters
	ro=6.022e28 #number density of aluminum atom used in sample, in inverse cubic meters (m^-3)
	const=9*V*ro*kb
	thetad=428 #the Debye temperature characteristic to aluminum, in Kelvin.
	pre_factor=const*(T/thetad)**3	
	a=0 #set lower limit of integral
	b=thetad/T #set upper limit of integral as the ratio of the Debye temperature to the surface temperature
	N=50 #set the number of slices to be used in Simpson's rule as instructed in the problem
	h=(b-a)/N #define the width of each slice to evaluate each portion of the function
	sum_odd,sum_even=0,0 #initialize the sums of the even and odd k terms in simpson's rule as zero
	#implement the sums given in equation 5.10
	for i in np.arange (1,N/2): 
		sum_odd+=f(a+(2*i-1)*h) #the sums of the odd terms
	for j in np.arange (1,N/2-1):
		sum_even+=f(a+2*j*h) #add each term of the function evaluated at an even multiple slice to the preceding one 
	I=h/3*(f(a)+f(b)+4*sum_odd +2*sum_even) #determine the integral approximation using Simpson's rule
	return I*pre_factor #output the integral multiplied by the pre-factor given in the Exercise prompt.
print("The value of the heat capacity at T=428 is: ", cv(428), "J/K.")

cvlist=[] #initialize a list to store the heat capacity at various temperatures
Tlist=[] #initialize a list to store the temperatures

plt.rc('text',usetex=True)
plt.rc('font', family='serif',serif='Palatino')
plt.title("Heat capacity As a Function of Temperature")
for T in np.arange (5,500): #set the range of temperatures from 5K-500K
	heat_cap=(cv(T))
	cvlist.append(heat_cap) #store the value of the heat capacity for each temperature to the list defined on line 37
	Tlist.append(T)
plt.plot(Tlist,cvlist) #plot the heat capacity as a function of temperature

plt.savefig('ex5.9.jpg',format='jpg',dpi=1000)#save the resulting figure as an image.
	
	