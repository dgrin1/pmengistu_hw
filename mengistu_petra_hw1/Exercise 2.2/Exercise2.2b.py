#Define known constants 
M=5.97e24 #mass of sun in kg
G=6.67e-11 #gravitational constant
R=6371000 #Radius of Earth in meters
pi=3.1451926535897 #value of irrational number pi

#Read in values for the period
T=float(input("Please enter a value for the period of the satellite: ")) #Ask user to enter the period of the satellite of their choosing.
h=(G*M*T**2/(4*pi**2))**(1/3) - R #Calculate the altitude with expression derived using Kepler's 3rd Law for given period

print("The altitude for your chosen period is : ", h) #print altitude for given period.
