from random import random, randrange
from numpy import arange
import numpy as np
from pylab import plot,xlabel,ylabel,show
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.animation import FuncAnimation
from matplotlib.colors import LinearSegmentedColormap
from neighborfunct import neighbor,disatisfied, occupied
# Constants
n,m=50,50
grid=np.zeros([n,m])
grid_time=np.zeros([n,m,10000])
npop1=1200
npop2=1200

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

t=0.7

nd=1

rng = np.random.default_rng()
t_step=0
#while t_step<1000:
while nd>0:
	n,m=50,50
	n_p,m_p=n-1,m-1
	dis_sat=np.array([])
	num_dis,occ=0,0
	#print("hello")
	for i in range (0,n):
		for j in range (0,m):
			nbr=[]
			satisfied=0
			#print(i,j)
			if grid[i,j]!=0:
				ind=np.array([i,j])

				occ+=1
				nbr=neighbor(n,m,i,j,grid)
				num_n=len(nbr)
				#print(num_n, "Index", i,j)
				#t_step+=1
				for a in range(num_n):
					if ((neighbor(n,m,i,j,grid)[a]==grid[i,j]) or (neighbor(n,m,i,j,grid)[a]==0)):
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
	print("The dissatisfied agenst are:")
	print(dis_sat)
	print("Empty")
	print(empty)
	if (num_dis>num_empty) and (num_empty>0):
		can_move=rng.choice(num_dis,num_empty, replace=False, shuffle=True)
		switch=np.zeros([num_empty,2])
		for n in range(len(can_move)):
			switch[n]=dis_sat[can_move[n]]
	else:
		switch=dis_sat
	dist=[]
	for a in range(len(switch)):
		for b in range(len(empty)):
			d=np.sqrt((switch[a,0]-empty[b,0])**2+(switch[a,1]-empty[b,1])**2)
			dist.append(d)
		#print(d)
	distance=np.array(dist)
	distance=np.transpose(np.resize(distance,(len(switch),len(empty))))
	pref=np.argsort(distance, axis=0)

	print("Preferences:",pref)
	n,m=50,50
	if len(pref)!=0:
		c=0
		while ((len(switch))>0) and (c<len(switch)):
			g=0
			while g<len(pref):
				move=int(pref[g,c])
				if empty[move,0]!=1.0e8:
					print("person", switch[c], "can move to", empty[move])
					im,jm=int(switch[c,0]),int(switch[c,1])
					ie,je=int(empty[move,0]),int(empty[move,1])
					print("Before:",neighbor(n,m,im,jm,grid))
					grid[im,jm],grid[ie,je]=grid[ie,je],grid[im,jm]
					print("After:",neighbor(n,m,ie,je,grid))
					check=disatisfied(n,m,ie,je,neighbor,grid)
					print(check)
					if len(check)==0:			
						print("person", switch[c], "did move to", empty[move])
						#print(grid[im,jm],grid[ie,je])
						#print(grid[im,jm],grid[ie,je])
						empty[move]=1.0e8
						switch=np.delete(switch,c,0)
						pref=np.delete(pref,c,1)
						print('new dissatisfied')
						print(switch)
						print("new pref")
						print(pref)
						break
					else:
						grid[im,jm],grid[ie,je]=grid[ie,je],grid[im,jm]
						c+=1
						print(c)
						break
				else:
 					g+=1
 					
	
	occup=occupied(n,m,grid)
	occ=len(occup)
	print('Swapping',occ)
	print(occup)
	for h in range(occ):
		k=0
		while ((len(switch))>0) and (k<len(switch)):	
			#print('hi')
			#print("person", switch[k], "can swap with", occup[h])
			is1,js1=int(switch[k,0]),int(switch[k,1])
			is2,js2=int(occup[h,0]),int(occup[h,1])
			if is1!=is2 or js1!=js2:
				confirm=disatisfied(n,m,is1,js1,neighbor,grid)
				#print(confirm)
				if len(confirm)!=0:
					#print(grid[is1,js1], grid[is2,js2])
					grid[is1,js1],grid[is2,js2]=grid[is2,js2],grid[is1,js1]
					#print(grid[is1,js1], grid[is2,js2])
					checks2=disatisfied(n,m,is1,js1,neighbor,grid)
					checks1=disatisfied(n,m,is2,js2,neighbor,grid)
					#print("Neighbors 1:",neighbor(n,m,is1,js1,grid))
					#print("Neighbors 2:",neighbor(n,m,is2,js2,grid))
					#print(checks1,checks2)
					if len(checks1)==0 and len(checks2)==0:
						#print("person", switch[k], "swapped with", occup[h])
						switch=np.delete(switch,k,0)
					else:
						grid[is1,js1],grid[is2,js2]=grid[is2,js2],grid[is1,js1]
						k+=1
				else:
					switch=np.delete(switch,k,0)
					#print('switch')
					#print(switch)
			else:
				k+=1
					
	nd=num_dis
	print(nd)
	t_step+=1
	grid_time[:,:,t_step]=grid[:,:]
	
print("Elapsed time:", t_step)

fig, ax = plt.subplots(figsize=(5, 8))

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
	ax.imshow(im_normed, cmap='magma', vmin=0, vmax=2)
	ax.set_title("Schelling Model".format(i), fontsize=20)
	ax.set_axis_off()
anim = FuncAnimation(fig, update, frames=np.arange(0, 20), interval=200)
plt.show()

# anim.save('colour_rotation.gif', dpi=80, writer='imagemagick')
# plt.close()
# 
# global grid
