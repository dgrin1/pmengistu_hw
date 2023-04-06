#Author: Petra Mengistu
#Import libraries
from numpy import array,arange
import matplotlib.pyplot as plt
import numpy as np
# Constants
m = 9.1094e-31     # Mass of electron
hbar = 1.0546e-34  # Planck's constant over 2*pi
e = 1.6022e-19     # Electron charge

V0=50*e #in ev
a=1.0e-11 #in meters
L=20*a
N = 1000
h = L/N



# Potential function
def V(x):
	return V0*x**4/a**4


def f(r,x,E):
    psi = r[0]
    phi = r[1]
    fpsi = phi
    fphi = (2*m/hbar**2)*(V(x)-E)*psi
    return array([fpsi,fphi],float)

# Calculate the wavefunction for a particular energy
#vaue of the wave function Psi(L)
def solve(E):
    psi = 0.0
    phi = 1.0
    r = array([psi,phi],float)

    for x in arange(-L/2,L/2,h):
        k1 = h*f(r,x,E)
        k2 = h*f(r+0.5*k1,x+0.5*h,E)
        k3 = h*f(r+0.5*k2,x+0.5*h,E)
        k4 = h*f(r+k3,x+h,E)
        r += (k1+2*k2+2*k3+k4)/6
    return r[0]

# Main program to find the energy using the secant method
E1 = 0
E2 = 100*e
psi2=solve(E1)
psi2_l,E1l=[],[]

#To determine the good guesses for E2, we run the code below that plots psi2 for a range of energies
# for i in arange(0,2300*e,5*e):
# 	psi2 = solve(i)
# 	#print(psi2)
# 	psi2_l.append(psi2)
# 	E1l.append(i)
# 
# plt.figure(1)
# plt.rc('text',usetex=True)
# plt.rc('font', family='serif',serif='Palatino')
# plt.plot(E1l,np.log10(np.abs(psi2_l)))
# 
# plt.xlabel('Energy')
# plt.ylabel(r'$\psi (t)$')
# plt.show()


target = e/1000
while abs(E1-E2)>target: #condition that E2 must be zero at boundary
	psi1,psi2 = psi2,solve(E2)
	E1,E2 = E2,E2-psi2*(E2-E1)/(psi2-psi1)
 
print("E =",E2/e,"eV") 
