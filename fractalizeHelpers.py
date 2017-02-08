import math
# Gets the number of times left required to fractalize to get the highest res image.
def getNumTimes(data):
    currPoints = len(data.fractalPoints[-1]) 
    nTimes = int(math.log(data.maxPoints//(currPoints),len(data.points)))
    return nTimes


#finds the distance between two points
def dist(point1,point2):
    x1 = point1[0]
    x2 = point2[0]
    y1 = point1[1]
    y2 = point2[1]
    xsq = (x2 - x1)**2
    ysq = (y2 - y1)**2
    return (xsq + ysq) ** .5

#finds the angle between two points and the horizontal
def ang(point1,point2):
    x1 = point1[0]
    y1 = point1[1]
    x2 = point2[0]
    y2 = point2[1]
    dy = y2 - y1
    dx = x2 - x1
    theta = math.atan2(dy,dx)
    return theta

#finds the segment lengths of a whole set of points    
def getSegLens(points):
    segLens = []
    for index in range(0,len(points) - 1):
        point1 = points[index]
        point2 = points[index+1]
        distance = dist(point1,point2) 
        segLens.append(distance)
    return segLens

#finds the segment angles of a whole set of points
def getSegAngles(points):
    segAngles = []
    for index in range(0,len(points)-1):
        point1 = points[index]
        point2 = points[index+1]
        angle = ang(point1,point2)
        segAngles.append(angle)
    return segAngles

#scales an image down to a correct scale.
def scaleImage(points,scale):
    scaled = []
    for point in points:
        px = point[0]
        py = point[1]
        scaledx = px * scale
        scaledy = py * scale
        newPoint = (scaledx,scaledy)
        scaled.append(newPoint)
    return scaled

#translates an image to a position
def translateImage(points,position):
    translated = []
    refPoint = points[0]
    x1 = refPoint[0]
    y1 = refPoint[1]
    x2 = position[0]
    y2 = position[1]
    dx = x2 - x1
    dy = y2 - y1
    for point in points:
        px = point[0]
        py = point[1]
        translatedx = px + dx
        translatedy = py + dy
        newPoint = (translatedx,translatedy)
        translated.append(newPoint)
    return translated

#rotates an image a certain angle
def rotateImage(points,angle):
    offset = ang(points[0],points[-1])
    rotated = []
    refPoint = points[0]
    x1 = refPoint[0]
    y1 = refPoint[1] 
    for point in points:
        thetai = ang(refPoint,point)
        distance = dist(point,refPoint)
        rotatedx = x1 + distance * math.cos(thetai + angle - offset)
        rotatedy = y1 + distance * math.sin(thetai + angle - offset)
        newPoint = (rotatedx,rotatedy)
        rotated.append(newPoint)
    return rotated

###adds sides to the fractal depending on your side count.
def sideAdder(data):
    sides = data.sides
    angle = math.pi * 2 / data.sides
    for side in range(1,sides):
        position = data.fractalPoints[0][-1]
        currAngle = side * angle
        rotPoints = rotateImage(data.points,currAngle)
        transPoints = translateImage(rotPoints,position)
        data.fractalPoints[0].pop()
        data.fractalPoints[0].extend(transPoints)

