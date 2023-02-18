#Author:Petra Mengistu
import numpy as np #import the necessary libraries
import matplotlib.pyplot as plt
milikan= np.loadtxt("millikan.txt", float) #load the sample data from Newman containing the frequencies and voltages

x=milikan[:,0] #extract the frequencies (in units of Hertz, Hz) into an array
y=milikan[:,1] #extract the voltages (in units of volts, V) into an array
plt.scatter(x,y) #for part a, plot the voltage as a function of frequency as a function of frequency

#For part b, we calculate the sums given to determine the slope and intercept
N=len(x)#to define the average, we need to divide by the number of datat points
sumx, sumy, sumxy, sumx2 =0,0,0,0 #initialize the sums as zero
for i in range(0,N):
	sumx+=x[i] #to each sum, increment the appropriate term. For the sum of x terms, add each xterm to the previous sum
	sumx2 +=x[i]**2 #for the sum of the square of the x terms, add each xterm squared
	sumy+=y[i] #for the sum of the y terms add each y term
	sumxy += x[i]*y[i] #for the sum of the product of x and y add each consecutive term

#the appropriate averages from Newman are defined below.
Ex=(1/N)*sumx
Ey=(1/N)*sumy
Exy=(1/N)*sumxy
Exx=(1/N)*sumx2

#Determine the slope and intercept using the formula in Newman
m= (Exy- Ex*Ey)/(Exx-Ex**2)
c= (Exx*Ey-Ex*Exy)/(Exx-Ex**2)

e=1.602e-19 #the charge of an electron, in units of Coloumbs
h=m*e #the equation to calculate Planck's constant, as the slope is h/e
print("The slope is ", m, "in units of Js/C and the intercept is ", c, "in units of V. The value of Plancks constant is", h, "in units of Js")

bestfit=[]#initialize list of best fit values determined using the linear model 
for j in range (0,N):
	best_fit=m*x[j]+c#determine the estimated voltage for each frequency
	bestfit.append(best_fit) #append each estimate voltage to the list
#import LaTeX text styles
plt.rc('text',usetex=True)
plt.rc('font', family='serif',serif='Palatino')

plt.plot(x,bestfit) #for part c, overplot the linear trendline
plt.title(r'$Voltage vs. Frequency$')
plt.xlabel(r'$Frequency (Hz)$',fontsize=16)#set the x and y axes to frequency and voltage respectively
plt.ylabel(r'$Voltage (V)$',fontsize=16)
plt.savefig('ex3.8c.jpg',format='jpg',dpi=1000)#save the resulting figure as an image.

