#Define known constants from the problem
a1=15.67
a2=17.23
a3=0.75
a4=93.2

#Ask user to input a value for the atomic number Z and mass number A
A=float(input("Please enter the mass number: "))
Z=float(input("Please enter the atomic number: "))

#Determine the appropriate value to use depending on whether the mass numbers are even or odd.
if (A%2==1):
	a5=0 #If A is odd set a5 equal to zero
elif (A%2==0 and Z%2==0):
	a5=12 #set a5 equal to 12 if both are even
else:
	a5=-12 #set a5 equal to -12 if Z is odd.

#Calculate the binding energy using the semi-empirical mass formula.
B=a1*A - a2*A**(2/3) - a3*(Z**2)/(A**(1/3)) - a4*(A-2*Z)**2/A + a5/(A**0.5)

BPN=B/A #calculate the binding energy per nucleon using the formula given.
print("The binding energy is ", B, "Mev.")
print("The binding energy per nucleon is ", BPN)