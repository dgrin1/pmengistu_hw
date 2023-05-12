#Author: Petra Mengistu
#Import all the necessary libraries and functions defined in other files
from random import random, randrange
from numpy import arange
import numpy as np
from pylab import plot,xlabel,ylabel,show
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.animation import FuncAnimation
from matplotlib.colors import LinearSegmentedColormap
from mengistu_petra_neighborfunct import neighbor,disatisfied, occupied, pltavg


#define the schelling model function that takes in the inputs of the horizontal and vertical dimensions
#of the city, the numbers of population 1 and 2, and the individual threshold similarity for the system.
def schelling(n,m,npop1,npop2,t):
	print("Starting your round of moves")
	grid=np.zeros([n,m]) #Initialize the grid as a matrix of zeros using the input dimensions
	
	#Randomly assign populations to grids
	while npop1>0:
		row_slot=randrange(n)#generate a random number within the dimensions of the grid to get a pair of indices
		col_slot=randrange(m)
		if grid[row_slot,col_slot]==0: #provided that the slot is empty, assign a member of the population to that location
			grid[row_slot,col_slot]=1
			npop1 -=1
	while npop2>0:
		row2_slot=randrange(n)
		col2_slot=randrange(m)
		if grid[row2_slot,col2_slot]==0:
			grid[row2_slot,col2_slot]=2
			npop2 -=1
	print(grid) #Initial configuration of city
	
	
	rng = np.random.default_rng()
	t_step=0
	#Initialize lists to store the amount of dissatisfied agents, the number of relocations, and the gini coefficient at each round 
	disatisfie=[]
	motion=[]
	gini=[]
	nd=1 #nd refers to the number of dissatisfied agents - to start the loop initially set it to a value of 1
	while nd>0: #run the loop until all agents are satisfied
		nmoves=0 
		#Initialize values for the Gini coefficient calculations
		pop1,pop2,nemp=0,0,0
		pop1q1,pop2q1,pop1q2,pop2q2,pop1q3,pop2q3,pop1q4,pop2q4=0,0,0,0,0,0,0,0
		nempq1,nempq2,nempq3,nempq4=0,0,0,0
		#Determine Python numbering of indices
		n_p,m_p=(n-1),(m-1)
		#Create an array to store the indices of the dissatisfied agents
		dis_sat=np.array([])
		num_dis=0 #initialize the values of the number of dissatisfied agents

		#Identify neighbors by looping over non-empty locations in the grid
		for i in range (0,n):
			for j in range (0,m):
				nbr=[]
				satisfied=0

				if grid[i,j]!=0:
					ind=np.array([i,j])			
					nbr=neighbor(n,m,i,j,grid)#call neighbor function
					num_n=len(nbr)
					
					#Determine satisfaction for given individual
					for a in range(num_n):
						#Count number of satisfied agents
						if ((neighbor(n,m,i,j,grid)[a]==grid[i,j]) or (neighbor(n,m,i,j,grid)[a]==0)):
							satisfied +=1
					#calculate satisfaction factor and compare to the threshold similarity
					sim=satisfied/num_n
					if sim <t: #when satisfaction is less than threshold, increase number of dissatisfied agents and store indices in array
						index=np.array([i,j])
						num_dis +=1
						dis_sat=np.append(dis_sat, index)
					dis_sat=np.resize(dis_sat,(num_dis,2))			
		#Identify all the empty locations on the grid
		empts=np.where(grid==0)
		empty=np.zeros([np.size(empts[0]),2])
		empty[:,0],empty[:,1]=empts
		num_empty,cols=np.shape(empty) #number of empty slots
		
		#Select a sample of dissatisfied agents that can move based on the number of empty slots
		if (num_dis>num_empty) and (num_empty>0):
			can_move=rng.choice(num_dis,num_empty, replace=False, shuffle=True) #use random choice for selection, and shuffle the order of the list
			switch=np.zeros([num_empty,2])#create the matrix that stores the indices of the dissatisfied agents that are going to move.
			for x in range(len(can_move)):
				switch[x]=dis_sat[can_move[x]]
		else:
			switch=dis_sat
		#Identify the ranked order preference of individuals to move towards an empty location. Shuffle the order of the preferences
		pref=np.zeros([len(empty),len(switch)]) #set the preferences as an empty array that will provide the order of preference individuals
		#would like to move to in each column
		for a in range(len(switch)):
			pref[:,a]=np.arange(len(empty))
			rng.shuffle(pref[:,a])
	
		#Allow all agents that have been selected to move to attempt to move to their first order preference
		for c in range (len(switch)):
			g=0
			while g<len(pref):
				move=int(pref[g,c])
				#If an empty slot has been occupied, it will now have indices set to a large number of 1.0e8. If its indices are possible
				#indices for the grid, the slot is still available
				if empty[move,0]!=1.0e8: #check to see if the slot for the first choice of an agent is available
					#If it is, allow the agent to change locations.
					im,jm=int(switch[c,0]),int(switch[c,1])
					ie,je=int(empty[move,0]),int(empty[move,1])
					#Set the values of the grid equal to one another and the index of the slot in the array of all empty slots to 1e8
					grid[im,jm],grid[ie,je]=grid[ie,je],grid[im,jm]
					empty[move]=1.0e8
					nmoves+=1 #increment the number of moves that have occurred
					break
				else:
					g+=1  #if the slot is not available, try the agent's next preference
		
		#Calculating Gini Coefficient
		def ginic(pop1,pop2,nemp):
			tot=pop1+pop2+nemp
			delpop1=pop1/tot
			delpop2=pop2/tot
			gini_coeff=1-delpop1**2-delpop2**2 #implement equation covered in class
			return gini_coeff
		#Divide the grid into quadrants, count the number of population 1 and 2 agents in the grid
		for i in range(0,int(n/2)):
			for j in range(0,int(m/2)):
				if grid[i,j]==1:
					pop1q1+=1
				elif grid[i,j]==1:
					pop2q1+=1
				else:
		 			nempq1+=1
		
		giniq1=ginic(pop1q1,pop2q1,nempq1) #calculate the gini coefficient for each quadrant

		for i in range(0,int(n/2)):
			for j in range(int(m/2),m):
				if grid[i,j]==1:
					pop1q2+=1
				elif grid[i,j]==1:
					pop2q2+=1
				else:
					nempq2+=1
		
		giniq2=ginic(pop1q2,pop2q2,nempq2)
		for i in range(int(n/2),n):
			for j in range(0,int(m/2)):
				if grid[i,j]==1:
					pop1q3+=1
				elif grid[i,j]==1:
					pop2q3+=1
				else:
					nempq3+=1

		giniq3=ginic(pop1q3,pop2q3,nempq3)
		for i in range(int(n/2),n):
			for j in range(int(m/2),m):
				if grid[i,j]==1:
					pop1q4+=1
				elif grid[i,j]==1:
					pop2q4+=1
				else:
					nempq4+=1

		giniq4=ginic(pop1q4,pop2q4,nempq4)
		gini_t=(giniq1+giniq2+giniq3+giniq4)/4 #determine the average gini coefficient for the given round of the entire grid
		gini.append(gini_t) #store it in the initial array

		nd=num_dis #set the number of dissatisfied agents as the number of total dissatisfied agents in the round
		motion.append(nmoves) #store the total number of moves that occurred in the given round
		disatisfie.append(num_dis) #store number of dissatisfied agents
		print(nd)
		t_step+=1
		
		#Stopping Condition
		if t_step>150: #when the code has run for over 150 iterations, check to see if the system is in myopic equilibrium or if the dissatisfied agents are cycling in a loop
			startcheck=len(motion)-100 #look at the last 100 number of moves that have occurred in the system
			
			freezing=[]
			for l in range(startcheck,len(motion)):
				netmove=motion[l]-motion[l-1] #determine  the difference between the number of moves within this round and the prior 
				print(motion[l], motion[l-1])
				print("netmotion", netmove)
				if netmove==0:
					freezing.append(netmove) #append it when the number of moves between two consecutive rounds has not changed
				else:
					freezing=[]
			print('frozen', len(freezing))
			if len(freezing)==100: #if the number of moves between 100 consecutive rounds has not changed, stop the loop
				break
	print("Elapsed time:", t_step)
	return disatisfie #have the function output the number of dissatisfied agents (or alternatively 'gini' for an examination of the gini coefficient)

#Values for an 8x8 grid Gini coefficient calculations
quantg=schelling(8,8,18,30,0.9)
quantg2=schelling(8,8,18,30,0.9)
quantg3=schelling(8,8,18,30,0.9)	

quant5g=schelling(8,8,18,30,0.5)
quant5g2=schelling(8,8,18,30,0.5)
quant5g3=schelling(8,8,18,30,0.5)

quant3g=schelling(8,8,18,30,0.3)
quant3g2=schelling(8,8,18,30,0.3)
quant3g3=schelling(8,8,18,30,0.3)

#Values for a 100x100 Grid Gini Coefficient Calculations
# quantg=schelling(100,100,3000,4500,0.7)
# quantg2=schelling(100,100,3000,4500,0.7)
# quantg3=schelling(100,100,3000,4500,0.7)	
# 
# quant3g=schelling(100,100,3000,4500,0.3)
# quant3g2=schelling(100,100,3000,4500,0.3)
# quant3g3=schelling(100,100,3000,4500,0.3)
# 
# quant5g=schelling(100,100,3000,4500,0.5)
# quant5g2=schelling(100,100,3000,4500,0.5)
# quant5g3=schelling(100,100,3000,4500,0.5)

#See attached files for description of pltavg code
segr90=pltavg(quantg,quantg2,quantg3)
segr30=pltavg(quant3g,quant3g2,quant3g3)	
segr50=pltavg(quant5g,quant5g2,quant5g3)

tpoints1,tpoints2,tpoints3,tpoints4,tpoints5,tpoints6=[],[],[],[],[],[]

#Values for plotting number of dissatisfied agents as a function of time
# disc11=schelling(100,100,6500,2000,0.7)
# disc12=schelling(100,100,6500,2000,0.7)
# disc13=schelling(100,100,6500,2000,0.7)
# dis1=pltavg(disc11,disc12,disc13)
# 
# disc21=schelling(100,100,4250,4250,0.7)
# disc22=schelling(100,100,4250,4250,0.7)
# disc23=schelling(100,100,4250,4250,0.7)
# dis2=pltavg(disc21,disc22,disc23)
# 
# disc31=schelling(100,100,5550,1950,0.7)
# disc32=schelling(100,100,5550,1950,0.7)
# disc33=schelling(100,100,5550,1950,0.7)
# dis3=pltavg(disc31,disc32,disc33)
# 
# disc41=schelling(100,100,3750,3750,0.7)
# disc42=schelling(100,100,3750,3750,0.7)
# disc43=schelling(100,100,3750,3750,0.7)
# dis4=pltavg(disc41,disc42,disc43)
# 
# disc51=schelling(100,100,4440,1560,0.7)
# disc52=schelling(100,100,4440,1560,0.7)
# disc53=schelling(100,100,4440,1560,0.7)
# dis5=pltavg(disc51,disc52,disc53)
# 
# disc61=schelling(100,100,3000,3000,0.7)
# disc62=schelling(100,100,3000,3000,0.7)
# disc63=schelling(100,100,3000,3000,0.7)
# dis6=pltavg(disc61,disc62,disc63)
# 
# for i in range(len(dis1)):
# 	tpoints1.append(i)
# for i in range(len(dis2)):
# 	tpoints2.append(i)
# for i in range(len(dis3)):
# 	tpoints3.append(i)
# for i in range(len(dis4)):
# 	tpoints4.append(i)
# for i in range(len(dis5)):
# 	tpoints5.append(i)
# for i in range(len(dis6)):
# 	tpoints6.append(i)



for i in range(len(segr90)):
  	tpoints1.append(i)
for i in range(len(tpoints1)-len(segr30)):
  	lastg3=segr30[len(segr30)-1]
  	segr30.append(lastg3)
for i in range(len(tpoints1)-len(segr50)):
  	lastg5=segr50[len(segr50)-1]
  	segr50.append(lastg5)

#Plot the Gini Coefficient as a function of the number of rounds
fig, ax = plt.subplots(figsize=(8, 7))
# 
plt.rc('text',usetex=True)
plt.rc('font', family='serif',serif='Palatino')

plt.plot(tpoints1,segr90,'c-', label='$t=90\%$')
plt.plot(tpoints1,segr50,'m-', label='$t=50\%$')
plt.plot(tpoints1,segr30,'g-', label='$t=30\%$')
plt.ylabel("$G (Gini)$",fontsize=15) #set the x and y axes to x and r respectively
plt.xlabel("$N_{rounds}$",fontsize=15)


plt.title(r"Liquid Model: 8x8 Gini Coefficient", fontsize=18)

#Alternatively, plot the fraction of dissatisfied agents as a function of time.
# plt.plot(tpoints1,dis1,'c-', label='p=13:5; 15$\%$ empty')
# 
# plt.plot(tpoints2,dis2,'c--', label='p=1:1; 15$\%$ empty')
# 
# plt.plot(tpoints3,dis3, 'm-', label=r'p=13:5; 25$\%$ empty')
# plt.plot(tpoints4,dis4, 'm--', label=r'p=1:1; 25$\%$ empty')
# 
# plt.plot(tpoints5,dis5, 'g-', label=r'p=13:5; 40$\%$ empty')
# plt.plot(tpoints6,dis6, 'g--', label=r'p=1:1; 40$\%$ empty')
# plt.ylabel("Number of Dissatisfied Agents",fontsize=15) #set the x and y axes to x and r respectively
# plt.xlabel("Number of Rounds",fontsize=15)

plt.legend()
plt.show()
