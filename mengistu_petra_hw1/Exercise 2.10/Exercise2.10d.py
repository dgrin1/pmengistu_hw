#Define known constants from the problem
a1=15.67
a2=17.23
a3=0.75
a4=93.2


Z=1 #Set starting value of Z
Z_best=0 #Define variable that represents atomic number that corresponds to the most stable binding energy

Atest=Z #Define variable that tests possible values of A (mass number) for which the most stable binding energy is chosen.
B_best=-10000 #Initialize binding energy value as an arbitrary very negative number to establish minimum threshold.
maxE=-100000 #Initialize binding energy value as an arbitrary very negative number to establish minimum threshold.
for Z in range (1,101):
	c=Z #Set testing value of Z to determine best possible A for each Z
	while (Atest<=3*c): #Check values of A ranging from initial Z to 3Z
		#Determine value of a5
		if (Atest%2==1):
			a5=0
		elif (Atest%2==0 and Z%2==0):
			a5=12
		else:
			a5=-12
		#Calculate the value of the binding energy using the semi-empirical mass formula
		Btest=a1*Atest - a2*Atest**(2/3) - a3*(Z**2)/(Atest**(1/3)) - a4*(Atest-2*Z)**2/Atest + a5/(Atest**0.5)	
		if Btest>maxE:#test if current value of binding energy is greater than maximum
			A_maxE=Atest #if true, save the value of A that results in the more stable energy and the corresponding energy
			maxE=Btest #most stable value of energy for the current chosen value of A
		Atest+=1 #increase the value of A until it hits 3Z and to check if there are more stable values of energy.
	print(A_maxE,Z,maxE) #Print best value of A for a given Z, and the corresponding maximum binding energy
	#Check if the maximum binding energy for a given Z is greater than that of the next consecutive value for Z.
	if maxE>B_best:
		A_maxEbest=A_maxE #If true, define the value of mass number that produces the most stable binding energy for ALL Z
		B_best=maxE #Define the most stable energy
		Z_best=Z #Store value that produces most stable energy

print("Most stable values of mass number, atomic number, and binding energy: ", A_maxEbest, Z_best, B_best) #Print the most stable energy and the mass and atomic numbers that result in this energy.