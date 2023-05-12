#Import necessary libraries
from random import random, randrange
from numpy import arange
import numpy as np
from pylab import plot,xlabel,ylabel,show
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.animation import FuncAnimation
from matplotlib.colors import LinearSegmentedColormap


#Function to identify neighbors for a given agent
def neighbor(n,m,i,j,grid):
	neighbor=[]
	n_p=(n-1)
	m_p=(m-1)
	#Locate where on the grid agent is. If in one of the edge cases, construct number of neighbors as appropriated
	if grid[i,j]!=0:
		if i==0 and j==0: #upper left corner, 3 neighbors
			neighbor=[grid[i,j+1],grid[i+1,j],grid[i+1,j+1]]
		elif i==0 and j==m_p: #upper right corner, 3 neighbors
			neighbor=[grid[i+1,j],grid[i+1,j-1],grid[i,j-1]]
		elif i==n_p and j==0:
			neighbor=[grid[i,j+1],grid[i-1,j],grid[i-1,j+1]]
		elif i==n_p and j==m_p:
			neighbor=[grid[i-1,j],grid[i-1,j-1],grid[i,j-1]]
		elif i==0 and (j>0 and j<m_p): #top row, 5 neighbors
			neighbor=[grid[i,j-1],grid[i,j+1],grid[i+1,j],grid[i+1,j+1],grid[i+1,j-1]]
		elif j==0 and (i>0 and i<n_p): #left column, 5 neighbors
			neighbor=[grid[i,j+1],grid[i+1,j],grid[i-1,j],grid[i+1,j+1],grid[i-1,j+1]]			
		elif j==m_p and (i>0 and i<n_p):
			neighbor=[grid[i,j-1],grid[i+1,j],grid[i-1,j],grid[i+1,j-1],grid[i-1,j-1]]			
		elif i>0 and i<n_p and j>0 and j<m_p:
			neighbor=[grid[i,j+1],grid[i,j-1],grid[i+1,j],grid[i-1,j],grid[i+1,j+1],grid[i+1,j-1],grid[i-1,j+1],grid[i-1,j-1]]
		elif ((i==n_p) and (j>0 and j<m_p)): #non-edge conditions, 8 neighbors
			neighbor=[grid[i-1,j],grid[i-1,j-1],grid[i-1,j+1],grid[i,j-1],grid[i,j+1]]
		
	return neighbor 

#Function to determine dissatisfaction of a given agent
def disatisfied(n,m,i,j,neighbor,grid,t):
	num_n=len(neighbor(n,m,i,j,grid)) #determine total number of neighbors
	index=[]
	satisfied,num_dis=0,0
	for a in range(num_n):
		if neighbor(n,m,i,j,grid)[a]==grid[i,j] or neighbor(n,m,i,j,grid)[a]==0:
			satisfied +=1 #determine number of similar neighbors
	sim=satisfied/num_n #calculate satisfaction factor

	if sim <t:
		index=np.array([i,j])
		num_dis +=1
	return index #output indices of agent if dissatisfied, output an empty array if agent is satisfied

#Function to determine occupied slots
def occupied(n,m,grid):
	occupied=np.array([])
	occ=0	
	for i in range (0,n):
		for j in range (0,m):
			if grid[i,j]!=0:
				ind=np.array([i,j])
				occupied=np.append(occupied,ind) #if the value of the grid is 1 or 2, it is occupied
				occ+=1
	occupied=np.resize(occupied,(occ,2)) # store indices in an array
	return occupied

#Function to determine the average of three lists of potentially different sizes
def pltavg(d11,d12,d13):
	dis=[]
	lengths=[len(d11),len(d12),len(d13)]
	long=np.max(lengths) #choose the longest list, to avoid truncating number of rounds
	#if the length of the list is different from that of the longest
	if len(d11)!=long:
		for i in range(len(d11),long):
			last1=d11[len(d11)-1] #append the last value in the list to make it a list of equal length
			d11.append(last1)
	if len(d12)!=long:
		for i in range(len(d12),long):
			last2=d12[len(d12)-1]
			d12.append(last2)
	if len(d13)!=long:
		for i in range(len(d13),long):
			last3=d12[len(d12)-1]
			d13.append(last3)
	#Once all the lists are of equal length, take the average of the three lists
	for i in range(long):
		x=np.average([d11[i],d12[i],d13[i]])
		dis.append(x)
	return dis #output the list of averages


