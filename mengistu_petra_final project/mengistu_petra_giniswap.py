#Author: Petra Mengistu
#Import necessary libraries and functions
from random import random, randrange
from numpy import arange
import numpy as np
from pylab import plot,xlabel,ylabel,show
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.animation import FuncAnimation
from matplotlib.colors import LinearSegmentedColormap
from mengistu_petra_neighborfunct import neighbor,disatisfied, occupied, pltavg

#This function is the same as that of the schellings function for swaps, only with the output of the gini array instead the number of dissatisfied agents
def schellingsg(n,m,npop1,npop2,t):
	print("Starting a new set of rounds")
	grid=np.zeros([n,m])

	
	#Randomly assign populations to grids
	while npop1>0:
		row_slot=randrange(n)
		col_slot=randrange(m)
		if grid[row_slot,col_slot]==0:
			grid[row_slot,col_slot]=1
			npop1 -=1
	while npop2>0:
		row2_slot=randrange(n)
		col2_slot=randrange(m)
		if grid[row2_slot,col2_slot]==0:
			grid[row2_slot,col2_slot]=2
			npop2 -=1
	print(grid)


	

	rng = np.random.default_rng()
	t_step=0
	tpoints=[]
	disatisfie=[]
	gini=[]
	motion=[]
	nd=1
	while nd>0:
		nmoves,nswaps=0,0
		n_p,m_p=n-1,m-1
		dis_sat=np.array([])
		num_dis,occ=0,0
		#Initialize parameters to calculate gini coefficient
		pop1,pop2,nemp=0,0,0
		gini_allp=[]
		pop1q1,pop2q1,pop1q2,pop2q2,pop1q3,pop2q3,pop1q4,pop2q4=0,0,0,0,0,0,0,0
		nempq1,nempq2,nempq3,nempq4=0,0,0,0
		#Identify neighbors for each agent
		for i in range (0,n):
			for j in range (0,m):
				nbr=[]
				satisfied=0
				if grid[i,j]!=0:
					ind=np.array([i,j])
					occ+=1
					nbr=neighbor(n,m,i,j,grid)
					num_n=len(nbr)
					
					#Determine satisfaction for each agent
					for a in range(num_n):
						if ((neighbor(n,m,i,j,grid)[a]==grid[i,j]) or (neighbor(n,m,i,j,grid)[a]==0)):
							satisfied +=1
					sim=satisfied/num_n
					if sim <t:
						index=np.array([i,j])
						num_dis +=1
						dis_sat=np.append(dis_sat, index)
					dis_sat=np.resize(dis_sat,(num_dis,2))			
		#Locate all empty spots and store indices in an array
		empts=np.where(grid==0)
		empty=np.zeros([np.size(empts[0]),2])
		empty[:,0],empty[:,1]=empts
		num_empty,cols=np.shape(empty)
		
		#Choose number of dissatisfied agents to relocate that is equal to number of available slots
		if (num_dis>num_empty) and (num_empty>0):
			can_move=rng.choice(num_dis,num_empty, replace=False, shuffle=True)
			switch=np.zeros([num_empty,2])
			for x in range(len(can_move)):
				switch[x]=dis_sat[can_move[x]]
		else:
			switch=dis_sat
		#Generate ranked order preference of available slots for each agent
		pref=np.zeros([len(empty),len(switch)])
		for a in range(len(switch)):
			pref[:,a]=np.arange(len(empty))
			rng.shuffle(pref[:,a])

		#Allow individuals to move to empty locations if satisfaction increases
		if len(pref)!=0:
			c=0
			while ((len(switch))>0) and (c<len(switch)):
				g=0
				while g<len(pref):
					move=int(pref[g,c])
					if empty[move,0]!=1.0e8:
						im,jm=int(switch[c,0]),int(switch[c,1])
						ie,je=int(empty[move,0]),int(empty[move,1])
						grid[im,jm],grid[ie,je]=grid[ie,je],grid[im,jm]
						check=disatisfied(n,m,ie,je,neighbor,grid,t)

						if len(check)==0:			

							empty[move]=1.0e8
							switch=np.delete(switch,c,0)
							pref=np.delete(pref,c,1)
							nmoves+=1

							break
						else:
							grid[im,jm],grid[ie,je]=grid[ie,je],grid[im,jm]
							c+=1

							break
					else:
 						g+=1
 					
		#Identify all occupied slots
		occup=occupied(n,m,grid)
		occ=len(occup)
		#Loop over occupied slots and determine whether any dissatisfied agent swap can have both agents satisfied
		for h in range(occ):
			k=0
			while ((len(switch))>0) and (k<len(switch)):	

				is1,js1=int(switch[k,0]),int(switch[k,1])
				is2,js2=int(occup[h,0]),int(occup[h,1])
				if is1!=is2 or js1!=js2: #don't let agent swap with themselves
					confirm=disatisfied(n,m,is1,js1,neighbor,grid,t)
					if len(confirm)!=0:
						grid[is1,js1],grid[is2,js2]=grid[is2,js2],grid[is1,js1]

						checks2=disatisfied(n,m,is1,js1,neighbor,grid,t)
						checks1=disatisfied(n,m,is2,js2,neighbor,grid,t)

						if len(checks1)==0 and len(checks2)==0:

							switch=np.delete(switch,k,0)
							nswaps+=1
						else:
							grid[is1,js1],grid[is2,js2]=grid[is2,js2],grid[is1,js1]
							k+=1
					else:
						switch=np.delete(switch,k,0)

				else:
					k+=1
		nmotion=nmoves+nswaps
		motion.append(nmotion)
		
		#Calculate Gini coefficient
		#Divide into quadrants, count number of population 1 and 2 in each quadrant	
		for i in range(0,int(n/2)):
			for j in range(0,int(m/2)):
				if grid[i,j]==1:
					pop1q1+=1
				elif grid[i,j]==1:
					pop2q1+=1
				else:
		 			nempq1+=1
		def ginic(pop1,pop2,nemp):
			tot=pop1+pop2+nemp
			delpop1=pop1/tot
			delpop2=pop2/tot
			gini_coeff=1-delpop1**2-delpop2**2
			return gini_coeff
		giniq1=ginic(pop1q1,pop2q1,nempq1)

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
		gini_t=(giniq1+giniq2+giniq3+giniq4)/4
		gini.append(gini_t)
		nd=num_dis
		disatisfie.append(num_dis)
		print(nd)
		if nd==0:
			break
		#Implement stopping condition
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
	return gini		


tpoints1,tpoints2,tpoints3,tpoints4,tpoints5,tpoints6=[],[],[],[],[],[]

#Values for gini coefficient of 50x50 grid
quantg=schellingsg(50,50,750,1125,0.7)
quantg2=schellingsg(50,50,750,1125,0.7)
quantg3=schellingsg(50,50,750,1125,0.7)

quant3g=schellingsg(50,50,750,1125,0.3)
quant3g2=schellingsg(50,50,750,1125,0.3)
quant3g3=schellingsg(50,50,750,1125,0.3)

quant5g=schellingsg(50,50,750,1125,0.5)
quant5g2=schellingsg(50,50,750,1125,0.5)
quant5g3=schellingsg(50,50,750,1125,0.5)
	
segr70=pltavg(quantg,quantg2,quantg3)
segr30=pltavg(quant3g,quant3g2,quant3g3)	
segr50=pltavg(quant5g,quant5g2,quant5g3)
for i in range(len(segr70)):
  	tpoints1.append(i)
for i in range(len(tpoints1)-len(segr30)):
  	lastg3=segr30[len(segr30)-1]
  	segr30.append(lastg3)
for i in range(len(tpoints1)-len(segr50)):
  	lastg5=segr50[len(segr50)-1]
  	segr50.append(lastg5)
fig, ax = plt.subplots(figsize=(8, 7))
# 
plt.rc('text',usetex=True)
plt.rc('font', family='serif',serif='Palatino')

plt.plot(tpoints1,segr70,'c-', label='$t=70\%$')
plt.plot(tpoints1,segr50,'m-', label='$t=50\%$')
plt.plot(tpoints1,segr30,'g-', label='$t=30\%$')
plt.ylabel("$G (Gini)$",fontsize=15) #set the x and y axes to x and r respectively
plt.xlabel("$N_{rounds}$",fontsize=15)


plt.title(r"Liquid Model: 50x50 Gini Coefficient", fontsize=18)




plt.legend()
plt.show()
