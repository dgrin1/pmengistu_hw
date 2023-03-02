#Author: Petra Mengistu
#Import the necessary libraries
import numpy as np 
from gaussxw import gaussxw
import matplotlib.pyplot as plt

def f(t): #Define the expression under the integral as a function
	f=np.e**(-t**2)
	return f

def Esimp(b,N):
	a=0 #set the lower limit of integration
	sum_odd=0 #initialize the sum of the terms representing the values of the function evaluated at odd multiples as zero
	sum_even=0  #initialize the sum of the terms representing the values of the function evaluated at even multiples as zero
	h=(b-a)/N #set the width of each slice
	for i in np.arange (1,N/2):
		sum_odd+=f(a+(2*i-1)*h)#add each value of the function at an odd multiple slice from the lower limit to its preceding value
	for j in np.arange (1,N/2-1): #Set the limit to stop before the last two slices.
		sum_even+=f(a+2*j*h)#add each value of the function at an even multiple slice from the lower limit to its preceding value. 
	I=h/3*(f(a)+f(b)+4*sum_odd +2*sum_even) #implement Newman eq 5.10 to determine an approximation of the integral
	return I


	
def Egauss(b,N):
	a=0 #set the lower limit of integration
	x,w = gaussxw(N) #determine sample points and weights 
	xp = 0.5*(b-a)*x + 0.5*(b+a) #map points and weights onto region of integration
	wp = 0.5*(b-a)*w
	s = 0.0 #initialize value of integral as zero
	for k in range(N):
		s += wp[k]*f(xp[k]) #integral is approximated by the sum of the function evaluated at a given point scaled by the corresponding weight for all points in the sample
	return s #output the approximation of integral

errs_simp=[] #initialize the list to store the error on each approximation
errs_gauss=[] #initialize the list to store the error on each approximation
Nlist=[] #initialize empty list to store number of slices tested
for N in range (2,100): #create a list of the number of slices that correspond to each error in the approximation
	Nlist.append(N)
	err_gauss=np.abs(Egauss(1,2*N)-Egauss(1,N))/Egauss(1,N) #determine the error on the Gaussian quadrature approximation by taking the relative convergence approach
	errs_gauss.append(err_gauss) #store each computed error in the list for gaussian errors
	err_simp=np.abs(Esimp(1,2*N)-Esimp(1,N))/Esimp(1,N) #determine the error by taking the ratio of the difference of the current and the approximation at twice the number of slices to the current approximation.
	errs_simp.append(err_simp) #store each error in a list






#Set the font styles
plt.rc('text',usetex=True)
plt.rc('font', family='serif',serif='Palatino')

plt.xlabel("Number of Slices (N)",fontsize=16)
plt.ylabel("Error on E(x)",fontsize=16)
plt. title("Error as a function of N")
#Plot the errors on a Logarithmic scale
plt.plot(np.log10(Nlist),np.log10(errs_gauss),'b--',label="Error on Gaussian Quadrature")
plt.plot(np.log10(Nlist),np.log10(errs_simp),'g-', label="Error on Simpson's Rule")
plt.legend()
plt.savefig('error2ex5.3.jpg',format='jpg',dpi=1000)#save the resulting figure as an image.