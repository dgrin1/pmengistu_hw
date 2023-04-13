
#Author: Petra Mengistu
#Import necessary libraries
from numpy.linalg import solve
import numpy as np
#define matrix for coefficients of V1, V2, V3, and V4 for the system of linear equations
A=np.array([[4,-1,-1,-1],[-1,0,3,-1],[-1,3,0,-1],[-1,-1,-1,4]])
#define matrix for the right hand sides of each of the linear equations in the system
v=np.array([5,5,0,0])
x=solve(A,v) #implement the solve command
print("V1 is:", x[0], "in volts")
print("V2 is:", x[1], "in volts")
print("V3 is:", x[2], "in volts")
print("V4 is:", x[3], "in volts")