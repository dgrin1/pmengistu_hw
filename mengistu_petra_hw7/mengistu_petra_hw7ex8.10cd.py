#Author:Petra Mengistu
#Import libraries
from math import sin,pi
from numpy import array,arange, copy,abs,sqrt
import numpy as np
import matplotlib.pyplot as plt
G=6.67e-11 #Gravitational constant, in N/kg,m^-1
M=1.989e30 #Mass of the sun in kg



#Define the system of first order differential equations
def f(r,t):
    x = r[0] #for a vector 'r' containing the solutions to the four differential equations, set the displacements as the first two columns of 'r'
    y = r[1]
    a=np.sqrt(x**2+y**2) #define the radius, distance from the sun, to a position on the orbit
    vx=r[2] #set velocities as the last two columns of r
    vy = r[3] 
    fx = vx
    fy=vy
    fvx = -(G*M*x/a**3) 
    fvy = -(G*M*y/a**3)
    return array([fx,fy,fvx,fvy],float)

#Initial values and initial step size
a = 0.0
b = 2.397e9 #in seconds
N = 1000000 #determined using trial and error to make the step size small enough
h0 = (b-a)/N #initial step size
#print(h0)
h=h0
i=0 #counter for number of steps taken
t=a #start time at leftmost boundary
#delta=0.00003170577
delta=0.003

#points
xpoints = []
ypoints = []
vxpoints,vypoints = [],[]
tpoints=[]
dxarr=[] #error array

#arrays for different guesses
r = array([4.0e12,0,0,500.e0],float)
r1= copy(r)
r2= copy(r)

#grab first value
xpoints.append(r[0])
ypoints.append(r[1])
vxpoints.append(r[2])
vypoints.append(r[3])
tpoints.append(t)
dxarr.append(0)

while t<b/1.5: #condition on time
	i+=1 #increment to count steps
	#RK4 used throughout
	#One large step
	k1 = 2.e0*h*f(r,t)
	k2 = 2.e0*h*f(r+0.5e0*k1,t+h)
	k3 = 2.e0*h*f(r+0.5e0*k2,t+h)
	k4 = 2.e0*h*f(r+k3,t+2.e0*h)
	r1 += (k1+2.e0*k2+2.e0*k3+k4)/6.e0
	
	# Two small steps, of h each
	#print(r1)
	k1 = h*f(r,t)
	k2 = h*f(r+0.5e0*k1,t+0.5e0*h)
	k3 = h*f(r+0.5e0*k2,t+0.5e0*h)
	k4 = h*f(r+k3,t+h)
	r2 += (k1+2.0e0*k2+2.0e0*k3+k4)/6.0e0
	
	k1 = h*f(r2,t)
	k2 = h*f(r2+0.5e0*k1,t+0.5e0*h)
	k3 = h*f(r2+0.5e0*k2,t+0.5e0*h)
	k4 = h*f(r2+k3,t+h)
	r2 += (k1+2.e0*k2+2.e0*k3+k4)/6.e0
	#print("R2 full k1:", k1,k2,k3,k4)


	dx=r1[0]-r2[0] #rho will be calculated based on the error in the x term
	dy=r1[1]-r2[1] #rho will be based on the error in the y term
	#print(dx,dy)
	print("h:",h) #printing step size

	if dx==0 or dy==0: #if the error is zero due to convergence, then we must alter the step size or rho will be infinity
		h*=1.000000002 #alter the step size, only a little as the scale is very sensitive
	else:
		rhox=30.*h*delta/abs(dx) #if the errors are non-negligible, we can calculate the rho for the x and y components
		rhoy=30.*h*delta/abs(dy)
		rho=min(rhox,rhoy) #to ensure we don't take a larger step size that ignores the rapidly changing y or x, take the smaller rho
		#print(rho)
	#adjust step size
		if rho>=1.0:
			t+=2*h #If rho is greater than 1, we increase the step size
			h*=min(rho**0.25,1.000000002) #we must put a cao on how much it can zoom out, or it will zoom out too quickly and lose the trajectory of orbit
			r=r2 # change the initial conditions
			xpoints.append(r[0])
			ypoints.append(r[1])
			vxpoints.append(r[2])
			vypoints.append(r[3])
			tpoints.append(t)
			dxarr.append(dx)
		else:
			h*=rho**0.25 #decrease the step size accordingly
			t+=2*h
			r=r2
			#print('betterstep')
			xpoints.append(r[0])
			ypoints.append(r[1])
			vxpoints.append(r[2])
			vypoints.append(r[3])
			tpoints.append(t)
			dxarr.append(dx)

#make a nice plot
print(i,max(abs(dxarr))) #number of steps and error on x
plt.figure(2)
plt.plot(xpoints,ypoints,'k.') #scatter plot of trajectory
plt.rc('text',usetex=True)
plt.rc('font', family='serif',serif='Palatino')


plt.xlabel("x position", fontsize=16)
plt.ylabel("y position", fontsize=16)

#plt.ion()
plt.show()
