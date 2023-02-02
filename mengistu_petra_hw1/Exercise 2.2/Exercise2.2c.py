#Define known constants 
M=5.97e24 #mass of sun in kg
G=6.67e-11 #gravitational constant
R=6371000 #Radius of Earth in meters
pi=3.1451926535897 #value of irrational number pi

#Read in values for the period
T1=90*60 #set period equal to 90 minutes
T2=45*60 #set period equal to 45 minutes

#Determine altitudes for the two periods with expression derived using Kepler's 3rd Law
h1=(G*M*T1**2/(4*pi**2))**(1/3) - R #altitude for 90 minute period
h2=(G*M*T2**2/(4*pi**2))**(1/3) - R #altitude for 45 minute period


print("The altitude for a 90 minute period is : ", h1, "meters") #print altitude for 90 min period.
print("The altitude for a 45 minute period is : ", h2, "meters. The altitude is negative, indicating that the satellite would be below the Earth's surface. This, however, is not possible, so the period of 45 minutes is too short to be a potential orbit for the satellite.") #print altitude for 45 min period.