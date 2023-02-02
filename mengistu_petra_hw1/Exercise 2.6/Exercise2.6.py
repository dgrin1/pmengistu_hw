#Import the numpy library to do calculations involving square root
import numpy as np
#Defining known constants, where a is the coefficient of v2^2 and G,M, and pi are the values of the
#gravitational constant, mass of the sun, and irrational number pi respectively.
a=1.0
G=6.6738e-11
M=1.9891e30
pi=3.145926535

#Asking User to provide values for the velocity at perihelion and distance.
l1=float(input("Enter the closest distance to the Sun: ")) #distance at perihelion
v1=float(input("Enter the velocity at perihelion: ")) #linear velocity at perihelion

#Defining the coefficient of v2 and the constant in the quadratic equation that solves for aphelion velocity
b=-2*G*M/(l1*v1)
c=2*G*M/l1-v1**2
d=np.sqrt(b**2-4*a*c) #define the determinant

#Check if the determinant is less than zero - if so, then code should not calculate orbital parameters.
if d>=0:
	posbl_v2=(-b - d)/(2*a)#Calculate two possible roots for v2
	posbl2_v2= (-b + d)/(2*a) #second posible root for v2
else:
	print("Invalid entries")

#Choosing the smaller root as the value of v2
if (posbl_v2>posbl2_v2):
	v2=posbl2_v2
else:
	v2=posbl_v2


#Determining the orbital parameters of semi-major and minor axis, orbital period (in seconds), and the eccentricity
l2=v1*l1/v2 #distance at aphelion
print("The velocity at aphelion is:", v2, "and the distance at aphelion is:", l2)

a=0.5*(l1+l2) #semi-major axis
b=np.sqrt(l1*l2) #semi-minor axis
T=2*pi*a*b/(l1*v1) #orbital sidereal period, in seconds
e=(l2-l1)/(l2+l1) #eccentricity

print("The semi-major axis, semi-minor axis, period, and eccentiricty are:", a,b,T,e, "respectively.") #Display output orbital parameters.

#For part c: Testing the code with known parameters for Earth's orbit and that of Halley's Comet agree reasonably well with accepted values.