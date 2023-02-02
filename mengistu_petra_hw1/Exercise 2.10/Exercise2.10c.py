#Define known constants from the problem
a1=15.67
a2=17.23
a3=0.75
a4=93.2

#Ask user to input a value for the atomic number
Z=float(input("Please enter the atomic number: "))
c=Z #Set testing value of Z to determine best possible A for each Z
Atest=Z  #Define variable that tests possible values of A (mass number) for which the most stable binding energy is chosen.
maxE=-100000 #Initialize binding energy value as an arbitrary very negative number to establish minimum threshold.
while (Atest<=3*c): #Check values of A ranging from initial Z to 3Z
	#Determine value of a5 depending on whether A and Z are even or odd.
	if (Atest%2==1):
		a5=0
	elif (Atest%2==0 and Z%2==0):
		a5=12
	else:
		a5=-12
	#Calculate the vale of the binding energy using the semi-empirical mass formula
	Btest=a1*Atest - a2*Atest**(2/3) - a3*(Z**2)/(Atest**(1/3)) - a4*(Atest-2*Z)**2/Atest + a5/(Atest**0.5)	
	if Btest>maxE:#test if current value of binding energy is greater than maximum
		A_maxE=Atest #if true, save the value of A that results in the more stable energy and the corresponding energy
		maxE=Btest #most stable value of energy for the current chosen value of A
	print(Atest,Btest) #Print best value of A for a given Z, and the corresponding maximum binding energy
	Atest+=1 #increase the value of A until it hits 3Z and to check if there are more stable values of energy.
	
BPN=maxE/A_maxE #Binding energy per nucleon
print("The most stable binding energy and the mass number at which this energy is obtained is ", maxE, "MeV and", A_maxE, "respectively")
print("The corresponding binding energy per nucleon is ", BPN)