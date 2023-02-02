#Define known constants 
M=5.97e24 #mass of sun in kg
G=6.67e-11 #gravitational constant
R=6371000 #Radius of Earth in meters
pi=3.1451926535897 #value of irrational number pi

#Read in values for the period
T1=float(input("Please enter a value for period equal to a sidereal day in seconds: ")) #Ask user to enter the period of a sidereal day in seconds
T=float(input("Please enter a value for period equal to 24 hours in seconds: ")) #Ask user to enter the period for a 24 hour day.
h=(G*M*T**2/(4*pi**2))**(1/3) - R #Calculate the altitude with expression derived using Kepler's 3rd Law for a period with 24 hours.
h1=(G*M*T1**2/(4*pi**2))**(1/3) - R   #Calculate the altitude with expression derived using Kepler's 3rd Law for the period entered for a sidereal day.
d=h-h1 #Calculate the difference in the altitudes estimated using the period for a 24hr day and that of a sidereal day
print("The altitude for a sidereal day length period is : ", h1) #print altitude for period of sidereal day
print("The difference in altitude for a sidereal day and a full 24 hour day is: ", d) #print calculated difference in altitude.