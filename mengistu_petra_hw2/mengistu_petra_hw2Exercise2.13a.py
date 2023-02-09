#Author: Petra Mengistu
#Import the required library
import numpy as np

def catalan(n): #define a function that determines the nth Catalan number.
	if (n==0):#following the piecewise function, determine if the term required is the zeroth Catalan number. If so, set the term equal to 1.
		c_n=1
	else:
		c_n= ((4*n-2)/(n+1))*catalan(n-1)#for all other terms in the series, determine the current catalan number by multiplying the previous term by the factor given in Newman
	return c_n

print("The 100th Catalan number is: ", catalan(100))#print the 100th catalan term