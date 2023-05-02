from random import random, randrange
from numpy import arange
import numpy as np
from pylab import plot,xlabel,ylabel,show
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.animation import FuncAnimation
from matplotlib.colors import LinearSegmentedColormap
# Constants
n,m=30,30
grid=np.zeros([n,m])
grid_time=np.zeros([n,m,10000])
npop1=600
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

t=0.63

nd=1


rng = np.random.default_rng()
t_step=0
#while t_step<1000:
while nd>0:
	n,m=30,30
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
					dis_sat=np.append(dis_sat, index)
				dis_sat=np.resize(dis_sat,(num_dis,2))		
	empts=np.where(grid==0)
	empty=np.zeros([np.size(empts[0]),2])
	empty[:,0],empty[:,1]=empts
	num_empty,cols=np.shape(empty)
	print(num_empty, cols)
	#print("The dissatisfied agenst are:")
	#print(dis_sat)

# 	print("Empty")
# 	print(empty)
	switch=np.zeros([num_empty,2])
	if num_dis>num_empty:
		can_move=rng.choice(num_dis,num_empty, replace=False, shuffle=True)
		for n in range(len(can_move)):
			switch[n]=dis_sat[can_move[n]]
	else:
		switch=dis_sat
	pref=np.zeros([len(empty),len(switch)])
	print(pref)
	for a in range(len(switch)):
		pref[:,a]=np.arange(len(empty))
		rng.shuffle(pref[:,a])
	print(pref)

 
	for c in range (len(switch)):
		g=0
		while g<len(pref):
			move=np.int(pref[g,c])
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
color_map = {1: np.array([255, 0, 0]), # red
             0: np.array([255, 255, 255]), # white
             2: np.array([0, 0, 255])} # blue 
color_map2 = {1: (np.array([255, 0, 0])), # red
             0: (np.array([255, 255, 255])), # white
             2: (np.array([0, 0, 255]))} # blue 
# grid_4d = np.ndarray(shape=(grid_time.shape[0], grid_time.shape[1], grid_time.shape[2],4), dtype=int)
# for i in range(0, grid_time.shape[0]):
#     for j in range(0, grid_time.shape[1]):
#     	for c in range (0,grid_time.shape[2]):
#         	grid_4d[i][j][c] = color_map[grid_time[i][j][c]]
# colors = {((1, 0, 0)), 
# 		((1, 1, 1)), 
# 		((0, 0, 1))}  # R -> G -> B
# 
# cmap_name = 'my_list'
# cmap = LinearSegmentedColormap.from_list(cmap_name, colors)


def update(i):
	im_normed =grid_time[:,:,i]
	ax.imshow(im_normed, cmap='gist_gray', vmin=0, vmax=2)
	ax.set_title("Schelling Model".format(i), fontsize=20)
	ax.set_axis_off()
anim = FuncAnimation(fig, update, frames=np.arange(0, 20), interval=200, repeat=False)
plt.show()

#anim.save('colour_rotation.gif', dpi=80, writer='imagemagick')
#plt.close()

#global grid
