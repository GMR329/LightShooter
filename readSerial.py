import serial
import re

#over is the light intensity at which we have 2 lights
OVER = 900
UNDER = 300

dev = serial.Serial("COM6", baudrate=9600)

#these are coords passed to game code. -1.0 to 1.0. Percentage
#placement along our xy plane
x = 0.0
y = 0.0

#need point is for when the point is in the same area. Likely
#the person hasn't covered their light yet 
readyCoord = True

#get the percentage across the axis it should be
def makeAxis(orig, ax):
    toRet = 0.0
    if orig > ax:
        toRet = -1.0 + ax / orig
    else:
        toRet = 1.0 - orig / ax

    return toRet

#given light values, make our correct x-y point
def makePoint(vals): 
    #make each point with the origin intensity and axis intensity
    x = makeAxis(vals[0], vals[1])
    y = makeAxis(vals[0], vals[2])

    if x > 1.0:
        x = 1.0
    if y > 1.0: 
        y = 1.0
    if x < -1.0:
        x = 1.0
    if y < -1.0: 
        y = 1.0

# while True:
def getCoord():
    lightVals = dev.readline()
    lightVals = lightVals.decode('ascii')
    lightVals = lightVals.strip()

    values = [0, 0, 0]

    x = 0
    for s in lightVals.split():
        s = int(s)

        #check to see if the light hasn't moved 
        if abs(s - values[x]) < 10:
            return (None, None)
            
        values[x] = s
        x += 1
        
    print(values)

    thresh = 0
    for s in values:
        thresh += s

    #see if 2 lights are detected by looking at total light detected 
    #also see if stuff is turning off 
    if thresh > OVER or thresh < UNDER:
        print("2 LIGHTS DETECTED\n")
        return (None, None)

    makePoint(values)
    
    return (x, y)