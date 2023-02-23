#Author: Petra Mengistu
#Import the necessary libraries
import numpy as np 
import matplotlib.pyplot as plt

def f(t): #Define the expression under the integral as a function
	f=np.e**(-t**2)
	return f

def E(b):
	a=0 #set the lower limit of integration
	Ilist=[] #initialize a list to store the values of the integral approximation for different slices
	for N in np.arange(1,100): #determine the approximation for various numbers of slices (N)
		sum_odd=0 #initialize the sum of the terms representing the values of the function evaluated at odd multiples as zero
		sum_even=0  #initialize the sum of the terms representing the values of the function evaluated at even multiples as zero
		h=(b-a)/N #set the width of each slice
		
		for i in np.arange (1,N/2):
			sum_odd+=f(a+(2*i-1)*h)#add each value of the function at an odd multiple slice from the lower limit to its preceding value
		for j in np.arange (1,N/2-1): #Set the limit to stop before the last two slices.
			sum_even+=f(a+2*j*h)#add each value of the function at an even multiple slice from the lower limit to its preceding value. 
		I=h/3*(f(a)+f(b)+4*sum_odd +2*sum_even) #implement Newman eq 5.10 to determine an approximation of the integral

		Ilist.append(I)#store the approximation of the integral for each N in the initial list
	return Ilist

c=np.array(E(2)) #for the upper limit of x=2, determine the different approximations of the integral for a 100 values of N


errs=[] #initialize the list to store the error on each approximation
for i in range (1,99):
	err=np.abs((c[i]-c[i-1]))/c[i] #determine the error by taking the ratio of the difference of the current and the prior approximation to the current approximation.
	errs.append(err) #store each error in a list
Nlist=[]
for i in range (1,99): #create a list of the number of slices that correspond to each error in the approximation
	Nlist.append(i)

#Set the font styles
plt.rc('text',usetex=True)
plt.rc('font', family='serif',serif='Palatino')

plt.xlabel("Number of Slices (N)",fontsize=16)
plt.ylabel("Error on E(x)",fontsize=16)
plt.plot(np.log10(Nlist),np.log10(errs)) #plot the error on the approximation as a function of the number of slices on a logarithmic scale.
plt.savefig('errorex5.3.jpg',format='jpg',dpi=1000)#save the resulting figure as an image.

	