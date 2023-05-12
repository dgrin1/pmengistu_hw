#Author: Petra Mengistu
#Import necessary libraries
from random import random, randrange
from numpy import arange
import numpy as np
from pylab import plot,xlabel,ylabel,show
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.animation import FuncAnimation
from matplotlib.colors import LinearSegmentedColormap
from mengistu_petra_neighborfunct import neighbor,disatisfied, occupied, pltavg

#Set initial conditions
n,m=100,100
t=0.3
grid=np.zeros([n,m])
grid_time=np.zeros([n,m,10000])
npop1=3000
npop2=4500


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

nd=1

#Initialize arrays to store number of moves for stopping condition
disatisfie=[]
motion=[]
while nd>0:
	#Initialize values that are updated at each round (dissatisfied agents, number of moves)
	nmoves,nswaps=0,0
	n_p,m_p=(n-1),(m-1)
	dis_sat=np.array([])
	num_dis,occ=0,0
	#Identify neighbors
	for i in range (0,n):
		for j in range (0,m):
			nbr=[]
			satisfied=0
			if grid[i,j]!=0:
				ind=np.array([i,j])
				occ+=1
				nbr=neighbor(n,m,i,j,grid)
				num_n=len(nbr)
				
				#Determine agent satisfaction
				for a in range(num_n):
					if ((neighbor(n,m,i,j,grid)[a]==grid[i,j]) or (neighbor(n,m,i,j,grid)[a]==0)):
						satisfied +=1
				sim=satisfied/num_n
				if sim <t:
					index=np.array([i,j])
					num_dis +=1
					dis_sat=np.append(dis_sat, index)
				dis_sat=np.resize(dis_sat,(num_dis,2))			
	#Identify empty locations
	empts=np.where(grid==0)
	empty=np.zeros([np.size(empts[0]),2])
	empty[:,0],empty[:,1]=empts
	num_empty,cols=np.shape(empty)
	#Choose a number of dissatisfied agents that can move that corresponds to the number of empty slots
	if (num_dis>num_empty) and (num_empty>0):
		can_move=rng.choice(num_dis,num_empty, replace=False, shuffle=True)
		switch=np.zeros([num_empty,2])
		for x in range(len(can_move)):
			switch[x]=dis_sat[can_move[x]]
	else:
		switch=dis_sat
	#Rank the individual preference to move to the available locations randomly
	pref=np.zeros([len(empty),len(switch)])
	for a in range(len(switch)):
		pref[:,a]=np.arange(len(empty))
		rng.shuffle(pref[:,a])
	
	#Begin moving stage
	if len(pref)!=0:
		c=0
		#If there are empty slots to move to, allow individuals to move to their preferred slot provided that the move increases their satisfaction
		while ((len(switch))>0) and (c<len(switch)):
			g=0
			while g<len(pref):
				move=int(pref[g,c])
				if empty[move,0]!=1.0e8: #if their preferred slot is empty, the agent can consider making a relocation
					im,jm=int(switch[c,0]),int(switch[c,1])
					ie,je=int(empty[move,0]),int(empty[move,1])
					#Determine the satisfaction of a member of the same population identity as the agent in the new location
					grid[im,jm],grid[ie,je]=grid[ie,je],grid[im,jm]
					check=disatisfied(n,m,ie,je,neighbor,grid,t)
					if len(check)==0:
						#if the agent is satisfied, allow them to remain in the switched position				
						empty[move]=1.0e8
						switch=np.delete(switch,c,0)
						pref=np.delete(pref,c,1)
						nmoves+=1
						break
					else:
						grid[im,jm],grid[ie,je]=grid[ie,je],grid[im,jm]
						c+=1
						#if the agent is not satisfied following the move, have them remain in their location
						break
				else:
 					g+=1
 					
	occup=occupied(n,m,grid)
	occ=len(occup)
#id#Identify the indicies of all the occupied slots on the grid
	for h in range(occ):
		k=0
		while ((len(switch))>0) and (k<len(switch)):	
			is1,js1=int(switch[k,0]),int(switch[k,1])
			is2,js2=int(occup[h,0]),int(occup[h,1])
			if is1!=is2 or js1!=js2: 
				confirm=disatisfied(n,m,is1,js1,neighbor,grid,t)
				#check that they are still dissatisfied
				if len(confirm)!=0:
					#Check the satisfaction of members of the agents' population if they were to switch locations
					grid[is1,js1],grid[is2,js2]=grid[is2,js2],grid[is1,js1]

					checks2=disatisfied(n,m,is1,js1,neighbor,grid,t)
					checks1=disatisfied(n,m,is2,js2,neighbor,grid,t)

					if len(checks1)==0 and len(checks2)==0: #both satisfied

						switch=np.delete(switch,k,0)
						nswaps+=1
					else:
						grid[is1,js1],grid[is2,js2]=grid[is2,js2],grid[is1,js1]
						k+=1
				else:
					switch=np.delete(switch,k,0)

			else:
				k+=1
	nmotion=nmoves+nswaps #total moves
	nd=num_dis
	motion.append(nmoves)
	disatisfie.append(num_dis)
	print(nd)
	if nd==0:
		break
	t_step+=1
	#Store grid configuration for that round in 3d array to make animation later
	grid_time[:,:,t_step]=grid[:,:]
	#Insert stopping condition
	if t_step>127:
		startcheck=len(motion)-125
			
		freezing=[]
		for l in range(startcheck,len(motion)):
			netmove=motion[l]-motion[l-1]
			print(motion[l], motion[l-1])
			print("netmotion", netmove)
			if netmove==0:
				freezing.append(netmove)
			else:
				freezing=[]
		print('frozen', len(freezing))
		if len(freezing)==125:
			break
	
print("Elapsed time:", t_step)

#Make the animation
fig, ax = plt.subplots(figsize=(5, 7))

plt.rc('text',usetex=True)
plt.rc('font', family='serif',serif='Palatino')
def update(i):
	im_normed =grid_time[:,:,i] #at each time step, show the image of the grid for that round
	ax.imshow(im_normed, cmap='magma', vmin=0, vmax=2)
	ax.set_title("{:} $t$; Number of Rounds: {:}".format(t,t_step), fontsize=20)
	ax.set_axis_off()
anim = FuncAnimation(fig, update, frames=np.arange(0, t_step), interval=500, repeat=False)
plt.show()


