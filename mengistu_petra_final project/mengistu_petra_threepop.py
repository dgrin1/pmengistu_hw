from random import random, randrange
from numpy import arange
import numpy as np
from pylab import plot,xlabel,ylabel,show
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.animation import FuncAnimation
from matplotlib.colors import LinearSegmentedColormap
from mengistu_petra_neighborfunct import neighbor,disatisfied, occupied
# Constants
n,m=50,50
grid=np.zeros([n,m])
grid_time=np.zeros([n,m,100000])
npop1=1000
npop2=700
npop3=300

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
while npop3>0:
	row3_slot=randrange(n)
	col3_slot=randrange(m)
	if grid[row3_slot,col3_slot]==0:
		grid[row3_slot,col3_slot]=3
		npop3 -=1
print(grid)

t=0.7

nd=1

rng = np.random.default_rng()
t_step=0
motion=[]
disatisfie=[]
#while t_step<1000:
while nd>0:
	nmoves=0
	n_p,m_p=(n-1),(m-1)
	dis_sat=np.array([])
	num_dis,occ=0,0
	for i in range (0,n):
		for j in range (0,m):
			nbr=[]
			satisfied=0
			if grid[i,j]!=0:
				ind=np.array([i,j])
				occ+=1
				nbr=neighbor(n,m,i,j,grid)
				num_n=len(nbr)
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
	if (num_dis>num_empty) and (num_empty>0):
		can_move=rng.choice(num_dis,num_empty, replace=False, shuffle=True)
		switch=np.zeros([num_empty,2])
		for x in range(len(can_move)):
			switch[x]=dis_sat[can_move[x]]
	else:
		switch=dis_sat
	pref=np.zeros([len(empty),len(switch)])
	for a in range(len(switch)):
		pref[:,a]=np.arange(len(empty))
		rng.shuffle(pref[:,a])

	for c in range (len(switch)):
		g=0
		while g<len(pref):
			move=int(pref[g,c])
			if empty[move,0]!=1.0e8:
				im,jm=int(switch[c,0]),int(switch[c,1])
				ie,je=int(empty[move,0]),int(empty[move,1])
				#print(grid[im,jm],grid[ie,je])
				grid[im,jm],grid[ie,je]=grid[ie,je],grid[im,jm]
				empty[move]=1.0e8
				nmoves+=1
				break
			else:
				g+=1
	nd=num_dis
	motion.append(nmoves)
	disatisfie.append(num_dis)
	print(nd)
	if nd==0:
		break
	t_step+=1
	grid_time[:,:,t_step]=grid[:,:]
	if t_step>500:
		startcheck=len(motion)-300
			
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
		if len(freezing)==300:
			break
	
print("Elapsed time:", t_step)

fig, ax = plt.subplots(figsize=(5, 7))
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

plt.rc('text',usetex=True)
plt.rc('font', family='serif',serif='Palatino')
def update(i):
	im_normed =grid_time[:,:,i]
	ax.imshow(im_normed, cmap='magma', vmin=0, vmax=3)
	ax.set_title("{:} $t$; Number of Rounds: {:}".format(t,t_step), fontsize=20)
	ax.set_axis_off()
anim = FuncAnimation(fig, update, frames=np.arange(0, t_step), interval=400, repeat=False)
plt.show()

#anim.save('colour_rotation.gif', dpi=80, writer='imagemagick')
#plt.close()

#global grid

