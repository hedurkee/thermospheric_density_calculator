class DataPoint:
    def __init__(self, lat, long, alt, time):
        self.lat = lat
        self.long = long
        self.alt = alt
        self.time = time

    def __init__(self):
        self.lat=0.0
        self.long=0.0
        self.alt=0.0
        self.time=0.0

    def __str__(self):
        return "DataPoint(latitude="+str(self.lat)+",longitude="+str(self.long)+",altitude="+\
               str(self.alt)+",time="+str(self.time)+")"

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
    return (p2.alt - p1.alt)/(p2.time - p1.time)  # Assumes alt is in meters and time is in seconds


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
    return ((2*MASS_SATELLITE*a) + (2*GRAV_CONST*MASS_EARTH*MASS_SATELLITE)/(p.alt + RADIUS_EARTH))/(DRAG_COEF*v*v)

'''
Converts incoming data as a string to an array of objects of type DataPoint.
Expected string format: "123519,4807.038,N,01131.000,E,545.4" 
representing "UTCtime,latitude,longitude,altitude"
'''
def parse_data_string(s):
    output = []
    the_point = DataPoint()
    the_var = "x"
    the_number = ""

    a = s.split(',')

    for i in range(int(len(a) / 6)):
        # index 0 = UTC time
        the_point.time = int(a.pop(0))
        # index 1 = lat
        the_point.lat = float(a.pop(0))
        a.pop(0)
        # index 3 = long
        the_point.long = float(a.pop(0))
        a.pop(0)
        # index 5 = alt
        the_point.alt = float(a.pop(0))
        output.append(the_point)
        the_point = DataPoint()
    return output

def main():

    # test data
    s = "123519,4807.038,N,01131.000,E,545.4,123533,4807.038,N,01131.000,E,540.4,123553,4807.038,N,01131.000,E,532.4,"

    output = parse_data_string(s)

    print(density(output[1], output[0], output[2]))

    
        
main()
