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

#define the schelling model function with swaps that takes in the inputs of the horizontal and vertical dimensions
#of the city, the numbers of population 1 and 2, and the individual threshold similarity for the system.
def schellings(n,m,npop1,npop2,t):
	print("Starting a new set of rounds")
	grid=np.zeros([n,m]) #Initialize the grid as a matrix of zeros using the input dimensions


	#Randomly assign populations to grids
	while npop1>0:
		row_slot=randrange(n)
		col_slot=randrange(m)
		if grid[row_slot,col_slot]==0:
			grid[row_slot,col_slot]=1
			npop1 -=1
	while npop2>0:
		row2_slot=randrange(n)#generate a random number within the dimensions of the grid to get a pair of indices
		col2_slot=randrange(m)
		if grid[row2_slot,col2_slot]==0:#provided that the slot is empty, assign a member of the population to that location
			grid[row2_slot,col2_slot]=2
			npop2 -=1 
	print(grid) #Initial configuration of city


	

	rng = np.random.default_rng()
	t_step=0
	#Initialize lists to store the amount of dissatisfied agents, the number of relocations over all rounds
	disatisfie=[]
	motion=[]
	tpoints=[]
	nd=1 #nd refers to the number of dissatisfied agents - to start the loop initially set it to a value of 1
	while nd>0:
		nmoves,nswaps=0,0
		#Determine Python numbering of indices
		n_p,m_p=n-1,m-1
		dis_sat=np.array([]) #array to store dissatisfied agents within a given round
		#Set number of dissatisfied agents and occupied slots to zero
		num_dis,occ=0,0
		#Identify neighbors by looping over non-empty locations in the grid
		for i in range (0,n):
			for j in range (0,m):
				nbr=[]
				satisfied=0
				if grid[i,j]!=0:
					ind=np.array([i,j])
					occ+=1 #increase to determine number of occupied slots
					nbr=neighbor(n,m,i,j,grid)
					num_n=len(nbr)
					
					#Determine satisfaction for given individual
					for a in range(num_n):
						if ((neighbor(n,m,i,j,grid)[a]==grid[i,j]) or (neighbor(n,m,i,j,grid)[a]==0)):
							satisfied +=1
					sim=satisfied/num_n
					if sim <t:
						index=np.array([i,j])
						num_dis +=1
						dis_sat=np.append(dis_sat, index) #store indices of dissatisfied individuals in initial array
					dis_sat=np.resize(dis_sat,(num_dis,2))			
		#Identify the available locations
		empts=np.where(grid==0)
		empty=np.zeros([np.size(empts[0]),2])
		empty[:,0],empty[:,1]=empts
		num_empty,cols=np.shape(empty)
		
		#Select all or a random sample of dissatisfied agents that can move  
		if (num_dis>num_empty) and (num_empty>0):
			can_move=rng.choice(num_dis,num_empty, replace=False, shuffle=True) #shuffle agents for unbiased sampling
			switch=np.zeros([num_empty,2])
			for x in range(len(can_move)):
				switch[x]=dis_sat[can_move[x]]
		else:
			switch=dis_sat
		#Determine the ranked order preference of each agent to move to an available slot in a matrix. Each column is each agent's list of 
		#preferences
		pref=np.zeros([len(empty),len(switch)])
		for a in range(len(switch)):
			pref[:,a]=np.arange(len(empty))
			rng.shuffle(pref[:,a])

		#Begin Moving stage
		#If there are empty slots to move to, allow individuals to move to their preferred slot provided that the move increases their satisfaction
		if len(pref)!=0:
			c=0
			while ((len(switch))>0) and (c<len(switch)):
				g=0
				while g<len(pref):
					move=int(pref[g,c])
					if empty[move,0]!=1.0e8: #if their preferred slot is empty, the agent can consider making a relocation
						
						im,jm=int(switch[c,0]),int(switch[c,1])
						ie,je=int(empty[move,0]),int(empty[move,1])
						#Determine the satisfaction of a member of the same population identity as the agent in the new location
						grid[im,jm],grid[ie,je]=grid[ie,je],grid[im,jm]
						check=disatisfied(n,m,ie,je,neighbor,grid,t) #if the agent is satisfied, this should output an empty array

						if len(check)==0:	
							#if the agent is satisfied, allow them to remain in the switched position		

							empty[move]=1.0e8 #indicate the empty slot is now occupied
							switch=np.delete(switch,c,0) #remove the agent from the list of dissatisfied agents
							pref=np.delete(pref,c,1)
							nmoves+=1
							break
						else:
							#if the agent is not satisfied following the move, have them remain in their location
							grid[im,jm],grid[ie,je]=grid[ie,je],grid[im,jm]
							c+=1
							break
					else:
 						g+=1
 					

		#identify the indicies of all the occupied slots on the grid
		occup=occupied(n,m,grid)
		occ=len(occup)
		#Begin swapping stage
		for h in range(occ):
			k=0
			while ((len(switch))>0) and (k<len(switch)):	
			
				is1,js1=int(switch[k,0]),int(switch[k,1])
				is2,js2=int(occup[h,0]),int(occup[h,1])
				if is1!=is2 or js1!=js2: # do not allow person to swap with themselves
					confirm=disatisfied(n,m,is1,js1,neighbor,grid,t) #check to see that the person is still dissatisfied
					
					if len(confirm)!=0:
						#Check the satisfaction of members of the agents' population if they were to switch locations
						grid[is1,js1],grid[is2,js2]=grid[is2,js2],grid[is1,js1]
						checks2=disatisfied(n,m,is1,js1,neighbor,grid,t)
						checks1=disatisfied(n,m,is2,js2,neighbor,grid,t)
						
						if len(checks1)==0 and len(checks2)==0:
							#Provided both are satisfied, implement the switch and delete the person from the list of dissatisfied agents
							switch=np.delete(switch,k,0)
							nswaps+=1
						else:
							grid[is1,js1],grid[is2,js2]=grid[is2,js2],grid[is1,js1] #if not, require that they remain in positions for the round
							k+=1
					else:
						switch=np.delete(switch,k,0)
						
				else:
					k+=1
		nmotion=nmoves+nswaps #determine the total number of swaps in a round 
		motion.append(nmotion)	
		nd=num_dis
		disatisfie.append(num_dis) #store number of dissatisfied agents at each round
		print(nd)
		#Implement stopping conditions if the number of moves has not changed in over 125 iterations
		if t_step>127:
			startcheck=len(motion)-125
			freezing=[]
			for l in range(startcheck,len(motion)):
				netmove=motion[l]-motion[l-1]
				if netmove==0:
					freezing.append(netmove)
			if len(freezing)==125:
				break
		t_step+=1
		tpoints.append(t_step)
		print("Elapsed time:", t_step)
	return disatisfie		#have the function output the number of dissatisfied agents over all rounds

#values for the 50x50 grid
tpoints1,tpoints2,tpoints3,tpoints4,tpoints5,tpoints6=[],[],[],[],[],[]
disc11=schellings(50,50,553,1572,0.5)
disc12=schellings(50,50,553,1572,0.5)
disc13=schellings(50,50,553,1572,0.5)
dis1=pltavg(disc11,disc12,disc13)

disc21=schellings(50,50,1063,1062,0.5)
disc22=schellings(50,50,1063,1062,0.5)
disc23=schellings(50,50,1063,1062,0.5)
dis2=pltavg(disc21,disc22,disc23)

disc31=schellings(50,50,488,1387,0.5)
disc32=schellings(50,50,488,1387,0.5)
disc33=schellings(50,50,488,1387,0.5)
dis3=pltavg(disc31,disc32,disc33)

disc41=schellings(50,50,938,937,0.5)
disc42=schellings(50,50,938,937,0.5)
disc43=schellings(50,50,938,937,0.5)
dis4=pltavg(disc41,disc42,disc43)

disc51=schellings(50,50,390,1110,0.5)
disc52=schellings(50,50,390,1110,0.5)
disc53=schellings(50,50,390,1110,0.5)
dis5=pltavg(disc51,disc52,disc53)

disc61=schellings(50,50,750,750,0.5)
disc62=schellings(50,50,750,750,0.5)
disc63=schellings(50,50,750,750,0.5)
dis6=pltavg(disc61,disc62,disc63)



for i in range(len(dis1)):
	tpoints1.append(i)
for i in range(len(dis2)):
	tpoints2.append(i)
for i in range(len(dis3)):
	tpoints3.append(i)
for i in range(len(dis4)):
	tpoints4.append(i)
for i in range(len(dis5)):
	tpoints5.append(i)
for i in range(len(dis6)):
	tpoints6.append(i)


fig, ax = plt.subplots(figsize=(8, 7))



plt.rc('text',usetex=True)
plt.rc('font', family='serif',serif='Palatino')
plt.ylabel("Number of Dissatisfied Agents",fontsize=15) #set the x and y axes to x and r respectively
plt.xlabel("Number of Rounds",fontsize=15)
plt.title(r"Solid Model: 50x50 Grid; $t=0.5$", fontsize=18)
plt.plot(tpoints1,dis1,'c-', label='p=13:5; 15$\%$ empty')
plt.plot(tpoints2,dis2,'c--', label='p=1:1; 15$\%$ empty')
plt.plot(tpoints3,dis3, 'm-', label=r'p=13:5; 25$\%$ empty')
plt.plot(tpoints4,dis4, 'm--', label=r'p=1:1; 25$\%$ empty')
plt.plot(tpoints5,dis5, 'g-', label=r'p=13:5; 40$\%$ empty')
plt.plot(tpoints6,dis6, 'g--', label=r'p=1:1; 40$\%$ empty')


plt.legend()
plt.show()
