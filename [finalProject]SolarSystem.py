import cv2
import numpy as np

screen = np.zeros((1000, 1000, 3), np.uint8)
pyList = []
def drawImage(screen, ptList, color):

    n = len(ptList)-1

    for i in range(0, n):

        cv2.line(screen, ptList[i], ptList[i+1], color)

#draw planets 

stPoint = (0,0)
def getPlanetList(k, stpoint):

    ptList = []
    n = 100
    angle = 360 / n

    #t is radius

    for t in range(k):

        for i in range(n):

            th = i * angle / 360 * (2 * np.pi)

            x = int(0 + t * np.cos(th))

            y = int(0 + t * np.sin(th))

            ptList.append((x, y))

    ptList = np.array(ptList)

    return ptList

#draw circle for planet's orbit

def getCircleList(k, stPoint):
    ptList = []

    angle = 360 / 100

    for i in range(100):

        th = i * angle /360 * (2 * np.pi)

        x = int(0 + k * np.cos(th))

        y = int(0 + k * np.sin(th))


        ptList.append((x, y))

    ptList = np.array(ptList)

    return ptList

def Rotate(period, day):

    deg = day / period * 360
    m = np.eye(3)  
    rad = deg * (np.pi * 2 / 360)
    c = np.cos(rad)
    s = np.sin(rad)
    m[0,0] = c
    m[0,1] = -s
    m[1,0] = s
    m[1,1] = c

    return m

def Translate(tx, ty):
    m = np.eye(3)
    m[0,2] = tx
    m[1,2] = ty
    
    return m

def transform(M, varr):

    ones = np.ones((varr.shape[0], 1))
    varr_homo = np.hstack((varr, ones)) # Nx3
    varr_homo = varr_homo.T # transpose, 3xN
    res = np.dot(M, varr_homo) # 3xN
    res = res.T # Nx3
    res = res[:,:2] # Nx2

    return res

#planet status
num = 8

period = [88, 224, 365, 687, 4329, 10768, 30660, 60225]

dist = [50, 70, 90, 110, 160, 210, 300, 450]

size = [4, 10, 10, 5, 27, 23, 20, 20]

color = [[106, 106, 106], [181, 190, 194], [130, 90, 78], [133, 195, 235], [179, 206, 242], [168, 198, 225], [120, 90, 65] , [130,90,85]]

day = 0

#set star position
rng = np.random.default_rng(2172000282)

starLoc = []

for i in range(30):

    starLoc.append((rng.integers(0, 1000), rng.integers(0, 1000)))

#Planets moves and rotate based on planet status set above

while cv2.waitKey(100) !=27: # = esc
    screen = np.zeros((1000, 1000, 3), np.uint8)
    #draw stars
    for i in range(30):

        star = getPlanetList(2,0)

        T0 = Translate(starLoc[i][0], starLoc[i][1])

        star = transform(T0, star)

        star = star.astype(int)

        drawImage(screen, star, (255, 255, 255))
    
    #draw sun 
    
    sun = getPlanetList(30, 0)

    M = Translate(500, 500) # sun

    result = transform(M, sun)

    result = result.astype(int)

    drawImage(screen, result, (0, 127, 255))

    #draw orbit of planet

    for i in range(num):

        circle = getCircleList(dist[i], stPoint)

        circle = transform(M, circle)

        circle = circle.astype(int)

        drawImage(screen, circle, (80,80,80))
    
    #draw planets
    
    for i in range(num):

        ptList = getPlanetList(size[i], 0)

        T0 = Translate(dist[i], 0)

        T1 = Rotate(period[i], day)

        TransRot = M @ T1 @ T0

        result = transform(TransRot, ptList)

        result = result.astype(int)

        drawImage(screen, result, color[i])

    day = day + 10

    cv2.imshow("solar_system",screen)


