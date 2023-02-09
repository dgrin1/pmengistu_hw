#Author: Petra Mengistu
#To run the code, we need to import the necessary libraries 
import matplotlib.pyplot as plt
import numpy as np

#Load in the sunspot file containing the data on the number of sunspots observed each month since 1749.
sunspot= np.loadtxt("sunspots.txt", float)

#Define two new arrays corresponding to the time of observed sunspots and the number of sunspots
#observed each month to use as independent variables when plotting sunspot number as a function of time.
t=sunspot[:1000,0] #time corresponding to each month number of sunspots were recorded. Represents the first thousand months since January 1749
s=sunspot[:1000,1] #number of sunspots recorded each month for the first 1000 months after Jan 1749.
#k=np.empty[1000,1]


m=5 #limit used to determine the boxcar average (index determining size of each bin used to calculate an average)
avg=[] #initialize the average values as an empty list
for k in range (0,1000): #Calculate the average with each sunspot number at the center of a consecutive bin.
	bins=s[k-m:k+m]#Define the set of data for which the average sunspot number is calculated with a bin of 10 data points.
	avg.append(sum(bins)/(2*m))#Determine the average of each bin according to the formula in Newman.

#import LaTeX text styles
plt.rc('text',usetex=True)
plt.rc('font', family='serif',serif='Palatino')


plt.plot(t,s)#Plot the initial result of sunspots as a function of time
plt.plot(t,avg) #Plot the "smoothed" result of the average sunspot number per month as a function of time.
plt.title('Sunspots as a function of Time')
plt.ylabel(r'Number of Sunspots',fontsize=16)#Define the labels as for the independent (number of sunspots) and dependent (time) variables.
plt.xlabel(r'Months since 01/1749',fontsize=16)
plt.savefig('ex3.1c.jpg',format='jpg',dpi=1000)#save the resulting figure as an image.


