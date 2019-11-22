class DataPoint:
    def __init__(self, x, y, z, t):
        self.x = x
        self.y = y
        self.z = z
        self.t = t

    def __init__(self):
        self.x=0
        self.y=0
        self.z=0
        self.t=0

    def __str__(self):
        return "DataPoint(x="+str(self.x)+",y="+str(self.y)+",z="+\
               str(self.z)+",t="+str(self.t)+")"

# Constants:
MASS_EARTH = 5.972 * (10**24) # kg
MASS_SATELLITE = 0.555448 # kg
RADIUS_EARTH = 6371000 # m
GRAV_CONST = 6.67408 * 10**-11 # m^3/(kg*s^2)
DRAG_COEF = 1.8

'''
Computes the velocity at the midpoint of p1 and p2 given two DataPoints
'''
def getVelocity(p1, p2):
    return (p2.z - p1.z)/(p2.t - p1.t)  # Assumes z is in meters and t is in seconds


'''
Approximates the velocity at p2 given three DataPoints
'''
def getVelocity3(p1, p2, p3):
    v1 = getVelocity(p1, p2)
    v2 = getVelocity(p2, p3)
    return (v1 + v2)/2

'''
Computes the acceleration at p2 given three DataPoints
'''
def getAcceleration(p1, p2, p3):
    v1 = getVelocity(p1, p2)
    v2 = getVelocity(p2, p3)
    return v2 - v1

'''
Computes the density at a given point using its predecessor and successor
'''
def density(p, prev, next):
    a = getAcceleration(prev, p, next)
    v = getVelocity3(prev, p, next)
    return ((2*MASS_SATELLITE*a) + (2*GRAV_CONST*MASS_EARTH*MASS_SATELLITE)/(p.z + RADIUS_EARTH))/(DRAG_COEF*v*v)

'''
Converts incoming data as a string to an array of objects of type DataPoint.
Expected string format: "x=_,y=_,z=_,t=_,"

Updated sample input: "123519,4807.038,N,01131.000,E,545.4" 
representing "UTCtime,latitude,longitude,altitude"
(code not yet updated to expect this input)
'''
def parse_data_string(s):
    output = []
    the_point = DataPoint()
    the_var = "x"
    the_number = ""

    for i in range(len(s)):
        current_char = s[i]
        
        if current_char == ',':
            ## convert the string we're working on into a number value
            ## assign to x, y, z, or t
            if the_var == "x":
                the_point.x = float(the_number)
                the_number=""
            elif the_var == "y":
                the_point.y = float(the_number)
                the_number=""
            elif the_var == "z":
                the_point.z = float(the_number)
                the_number=""
            elif the_var == "t":
                the_point.t = float(the_number)
                the_number=""
                output.append(the_point)
                the_point = DataPoint()
        elif current_char == "x" or current_char == "y" or \
             current_char == "z" or current_char == "t":
            the_var = current_char
        elif current_char == "=":
            1
        else:
            the_number += current_char
    return output

def main():

    # test data
    s = "x=0,y=0,z=100000,t=123519,x=0,y=0,z=99500,t=123550,x=0,y=0,z=99000,t=123585,"

    output = parse_data_string(s)

    print(density(output[1], output[0], output[2]))

    
        
main()
