
import cv2
import numpy as np

screen = np.zeros((1000, 1000, 3))
ptList = []
def drawImage(screen, ptList, color):

    n = len(ptList)-1

    for i in range(0, n):

        cv2.line(screen, ptList[i], ptList[i+1], color)


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

def Translate(tx, ty):

    m = np.eye(3)

    m[0,2] = tx

    m[1,2] = ty

    return m

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
def transform(M, varr):
    varr = np.ones(varr,1)
    
    varr_homo = np.hstack((varr)) 

    varr_homo = varr_homo.T 

    res = np.dot(M, varr_homo) 

    res = res.T # Nx3

    res = res[:,:2] # Nx2

 
    return res


#planet status

num = 6

period = [88, 224, 365, 687, 4329, 10768]

dist = [50, 70, 90, 110, 160, 210]

size = [4, 10, 10, 5, 27, 23]

color = [[106, 106, 106], [181, 190, 194], [130, 90, 78], [133, 195, 235], [179, 206, 242], [168, 198, 225]]

day = 0


while cv2.waitKey(100) !=27: # = esc
    screen = np.zeros((1000, 1000, 3), np.uint8)

    sun = getPlanetList(30, 0)

    M = Translate(500, 500) # sun

    drawImage(screen, M, (0, 127, 255))

    #draw planets
    
    for i in range(num):

        ptList = getPlanetList(size[i], 0)

        T0 = Translate(dist[i], 0)

        TransRot = M @ T0


        drawImage(screen, TransRot, color[i])

    day = day + 10

    cv2.imshow("solar_system",screen)    