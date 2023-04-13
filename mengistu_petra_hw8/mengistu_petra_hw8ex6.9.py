#Author: Petra Mengistu
from numpy.linalg import solve, eigvalsh, eigh
from math import pi, sin
import numpy as np
from gaussxw import gaussxw
import matplotlib.pyplot as plt

#Define constants
a=1.6022e-18 #in units of electron volts
M=9.1094e-31 #mass of electron, in kg
hbar=1.056e-34 #Planck's constant in J s
L=5.0e-10 #in meters
e=1.6022e-19 #in Coloumbs

#Define the size of the matrix using for an nmax X mmax sized matrix (for part c, set equal to 10x10)
nmax=100
mmax=100


diag=(hbar*pi)**2/(2*M*L**2) #part of the condition for when n=m, comprising of the constants without n dependence
diag2=a/2 #potential contribution to Hamiltonian for n=m case
offdiag=-(2*a/L**2)*(2*L/pi)**2 #portion of condition when n and m are odd and the other is even without n and m dependence
H=np.zeros([nmax,mmax]) #Initialize the Hamiltonian as a matrix of zeros

#Iterate over the possible entries in the matrix
for n in range (nmax): 
	for m in range (mmax):
		nh=n+1 #define the human numbering version of the n and m indices used to indicate the states
		mh=m+1
		if nh==mh:
			H[m,n]=diag*nh**2+diag2 #for the case that n is equal to m, use analytical solution determined
		#When both m and n are odd or even, set that entry equal to zero
		else:
			if nh%2==0 and mh%2==0:
				H[m,n]=0 
			elif nh%2!=0 and mh%2!=0:
				H[m,n]=0
			else: #For the case that n is even and m is odd or vice versa, use analytic solution
				H[m,n]=offdiag*mh*nh/(mh**2-nh**2)**2


eval=eigvalsh(H) #determine eigen values using built-in function
print("The set of eigen values, in electron volts eV, are:", eval/e)


#Part e
eigvals, eigsys=eigh(H) #determine set of eigen vectors using built in command

#Extract the first three eigen vectors
ground=eigsys[0,:]
first=eigsys[1,:]
second=eigsys[2,:]

#Define functions that determine each of the wavefunctions for the three states
def psig(x): #wavefunction for ground state
	psigr=0#set initial value to zero
	for n in range (nmax):
		terms= ground[n]*sin((n+1)*pi*x/L)#for each n, determine the Fourier coefficient (determined by the coefficient of the eigen vector
		#and multiply it by the sine function with the corresponding n value in its argument)
		psigr+=terms #add each term of the Fourier series
	return 4.0e9*psigr**2 #determine the probability density by taking the magnitude squared of and normalize using constant determined from Gaussian quadrature below
#Repeat above procedure for the first excited and second states, using the Fourier coefficients for each respective states
def psi1(x): #probability density for first excited state
	psift=0
	for n in range (nmax):
		terms= first[n]*sin((n+1)*pi*x/L)
		psift+=terms
	return 4.0e9*psift**2
def psi2(x): # probability density for second excited states
	psisd=0
	for n in range (nmax):
		terms= second[n]*sin((n+1)*pi*x/L)
		psisd+=terms
	return 4.0e9*psisd**2

#Initialize list to store values of the wave function at different values of x to plot as a function of x
psigl,psifl, psisl=[],[],[]
x=[]
#Calculate the wave function over the range of x where the potential is not infinite (i.e. the wavefunction is non zero)
for xpt in np.arange (0,L,1e-12):
	psigl.append(psig(xpt))#store the values of wave functions in a list
	psifl.append(psi1(xpt))
	psisl.append(psi2(xpt))
	x.append(xpt)

		

#Make plots of the probability density for each state

plt.plot(x,psigl, label='Ground state')
plt.plot(x,psifl, label='First excited state')
plt.plot(x,psisl, label='Second excited state')
plt.xlabel('x position', fontsize=16)
plt.ylabel('Probability density',fontsize=16)
plt.legend()
plt.show()


#Check normalization using Gaussian quadrature procedure
N=1000
#determine the weights
x,w = gaussxw(N)
xp = 0.5*(L)*x + 0.5*(L) #use a range equal to the width of potential
wp = 0.5*(L)*w

#Perform the integration
s = 0.0
for k in range(N):
      s += wp[k]*psi1(xp[k]) #can substitute other states for ground state or first excited state
print(s)
