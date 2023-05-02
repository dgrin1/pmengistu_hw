from random import random, randrange
from numpy import arange
import numpy as np
from pylab import plot,xlabel,ylabel,show
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.animation import FuncAnimation
# Constants
n,m=25,25
grid=np.zeros([n,m])
grid_time=np.zeros([n,m,10000])
npop1=400
npop2=200

p=0.5
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

t=0.9

nd=1


rng = np.random.default_rng()
t_step=0
while t_step<1000:
#while nd>0:
	n,m=25,25
	n_p,m_p=n-1,m-1
	dis_sat=np.array([])
	num_dis=0
	#print("hello")
	for i in range (0,n):
		for j in range (0,m):
			neighbor=[]
			satisfied=0
			#print(i,j)
			if grid[i,j]!=0:
				if i==0 and j==0:
					neighbor=[grid[i,j+1],grid[i+1,j],grid[i+1,j+1]]
				elif i==0 and j==m_p:
					neighbor=[grid[i+1,j],grid[i+1,j-1],grid[i,j-1]]
				elif i==n_p and j==0:
					neighbor=[grid[i,j+1],grid[i-1,j],grid[i-1,j+1]]
					#print("Hello")
				elif i==n_p and j==m_p:
					neighbor=[grid[i-1,j],grid[i-1,j-1],grid[i,j-1]]
				elif i==0 and (j>0 and j<m_p):
					neighbor=[grid[i,j-1],grid[i,j+1],grid[i+1,j],grid[i+1,j+1],grid[i+1,j-1]]
				elif j==0 and (i>0 and i<n_p):
					neighbor=[grid[i,j+1],grid[i+1,j],grid[i-1,j],grid[i+1,j+1],grid[i-1,j+1]]			
				elif j==m_p and (i>0 and i<n_p):
					neighbor=[grid[i,j-1],grid[i+1,j],grid[i-1,j],grid[i+1,j-1],grid[i-1,j-1]]			
				elif i>0 and i<n_p and j>0 and j<m_p:
					neighbor=[grid[i,j+1],grid[i,j-1],grid[i+1,j],grid[i-1,j],grid[i+1,j+1],grid[i+1,j-1],grid[i-1,j+1],grid[i-1,j-1]]
				elif i==n_p and (j>0 and j<m_p):
					neighbor=[grid[i-1,j],grid[i-1,j-1],grid[i-1,j+1],grid[i,j-1],grid[i,j+1]]
				
				num_n=len(neighbor)
				#print(num_n, "Index", i,j)
				#t_step+=1
				for a in range(num_n):
					if neighbor[a]==grid[i,j] or neighbor[a]==0:
						satisfied +=1
				sim=satisfied/num_n
				if sim <t:
					index=np.array([i,j])
					num_dis +=1
				#print(num_dis)
					dis_sat=np.append(dis_sat, index)
				dis_sat=np.resize(dis_sat,(num_dis,2))		
	empty=np.array([])
	num_empty=0
	#print("The dissatisfied agenst are:")
	#print(dis_sat)
	for i in range (0,n):
		for j in range (0,m):
			if grid[i,j]==0:
				spot=np.array([i,j])
				empty=np.append(empty,spot)
				num_empty +=1
	empty=np.resize(empty, (num_empty,2))
# 	print("Empty")
# 	print(empty)
	switch=np.array([])
	if num_dis>num_empty:
		can_move=rng.choice(num_dis,num_empty, replace=False, shuffle=True)
	#print("Index", can_move)
		for n in range(len(can_move)):
			switch=np.append(switch,dis_sat[can_move[n]])
		switch=np.resize(switch,(len(can_move),2))
	#print("these will movee:", switch)
	else:
		switch=dis_sat
# #Calculate the distances
# 
	dist=[]
	for a in range(len(switch)):
		for b in range(len(empty)):
			d=np.sqrt((switch[a,0]-empty[b,0])**2+(switch[a,1]-empty[b,1])**2)
			dist.append(d)
		#print(d)
	distance=np.array(dist)
	distance=np.transpose(np.resize(distance,(len(switch),len(empty))))
	pref=np.argsort(distance, axis=0)

	distance=np.sort(distance,axis=0)

	available=np.array(np.arange(num_empty))
# #print(distance)	
# 	print("Preferences")
# 	print(pref)	
# 
# 
	for c in range (len(switch)):
		g=0
		while g<len(pref):
			move=pref[g,c]
			if empty[move,0]!=1.0e8:
				#print("person", switch[c], "will move to", empty[move])
				im,jm=np.int(switch[c,0]),np.int(switch[c,1])
				ie,je=np.int(empty[move,0]),np.int(empty[move,1])
				#print(grid[im,jm],grid[ie,je])
				grid[im,jm],grid[ie,je]=grid[ie,je],grid[im,jm]
				#print(grid[im,jm],grid[ie,je])
				empty[move]=1.0e8
				break
			else:
				g+=1
	nd=num_dis
	print(nd)
	t_step+=1
	grid_time[:,:,t_step]=grid[:,:]
	
print("Elapsed time:", t_step)

fig, ax = plt.subplots(figsize=(5, 8))

def update(i):
	im_normed =grid_time[:,:,i]
	ax.imshow(im_normed)
	ax.set_title("Schelling Model".format(i), fontsize=20)
	ax.set_axis_off()
anim = FuncAnimation(fig, update, frames=np.arange(0, 20), interval=200)
plt.show()

#anim.save('colour_rotation.gif', dpi=80, writer='imagemagick')
#plt.close()

#global grid
