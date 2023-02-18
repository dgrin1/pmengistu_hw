#Author: Petra Mengistu
#Import the necessary libraries
import numpy as np 
import matplotlib.pyplot as plt
x=0.5 #set initial value of x

#Initialize lists to store values of x and r given from the function 
xlist2=[]
rlist=[]
rlist2=[]
def list(x,r): #create a function that generates the first 2,000 values of x from the Feigenbaum function
	xlist=[]#define an empty list to store the values of x
	for i in range(0,2000):# iterate through the first 2,000 steps of the function
		xlist.append(x)#add the current value of x at each step
		xpr=r*x*(1-x)#define the chaos function from the problem
		x=xpr #set the new value of x to the one just calculated
	return xlist[1000:2000] #output the values after the first thousand values of x

for rpt in np.arange(1.,4.,0.01):#as r ranges between 1-4 in 0.01 step increments
	for a in range(0,1000): #for each value of r, determine the x value by matching an r value to x
 		rlist2.append(rpt) #append each value of r into the initial list
	xpt=list(x,rpt)#use the function to print the second set of thousand values of x
	xlist2.append(xpt) #append each of these values to the initial x-list
#import LaTeX text styles
plt.rc('text',usetex=True)
plt.rc('font', family='serif',serif='Palatino')
plt.title("x vs r: Feigenbaum map")
plt.scatter(rlist2,xlist2,s=0.001, marker='o') #plot x as a function of r
plt.xlabel(r'$r$',fontsize=16) #set the x and y axes to x and r respectively
plt.ylabel(r'$x$',fontsize=16)
plt.savefig('ex3.6.jpg',format='jpg',dpi=1000)#save the resulting figure as an image.
