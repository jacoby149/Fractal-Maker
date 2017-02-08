import copy
from fractalizeHelpers import *
###dataHelpers

##################################################
#############General Initialization of Data#######
##################################################

###For making a general 2D list
def make2DList(rows,cols):
    answer = []
    empty = [0]
    for row in range(rows):
        answer.append(copy.copy(empty)*cols)
    return answer

###Initializes modes for the software
def initModes(data):
    data.mode = 0
    data.design = 0
    data.build = 1
    data.freeze = False
    data.screenShot = False

###Initializes general formatting of the windows
def initFormat(data):
    data.cellColor = "navy"
    data.gridSep = 4
    data.sqSize = 25
    data.margin = data.sqSize
    data.optionPaneHeight = data.sqSize * 3
    data.rows = (data.height-data.optionPaneHeight - data.margin)//data.sqSize
    data.cols = (data.width - 2 * data.margin)//data.sqSize
    data.grid = make2DList(data.rows,data.cols)    

###Initializes general navigational variables    
def initNav(data):
    data.reticle = (0,0)
    data.center = (data.width/2,data.height/2)
    data.zoom = 1
    data.speed = 50 
    data.zoomSpeed = 1.1
    data.goBack = False

###Initializes variables to make fractal shapes    
def initShapes(data):
    data.maxPoints = 128
    data.minTopPoints = 5
    data.sides = 1
    data.points = []
    data.fractalPoints = []
    data.freezePoints = []
    data.initColor = "#f11"
    nums = list(map(lambda x:str(x),list(range(10))))
    lets = list(map(lambda x : chr(ord("a") + x),list(range(6))))
    data.posColorChars = nums + lets
    data.colorFunc = lambda x : (x + 1) % 16

###Initializes data to save
def initFiles(data):
    data.selectedSave = "outfile"
    data.loadMode = False

######################################################
###########Main functions to manipulate fractal data##
######################################################

###fractalizes the user image
def fractalize(data):
    points = data.points
    fractalPoints = data.fractalPoints
    keepRunning = True
    while keepRunning:
        if getNumTimes(data) == 0:
            return False        
        makeFractalPointLv(data)

###makes one extra layer of fractal to the current fractal
def makeFractalPointLv(data):
    points = data.points
    fractalPoints = data.fractalPoints
    currFracPoints = fractalPoints[-1]
    imageLen = dist(points[0],points[-1])
    segLens = getSegLens(currFracPoints)
    segAngles = getSegAngles(currFracPoints)
    newFractalPoints = []
    lastPoint = (0,0)
    for i in range(0,len(fractalPoints[-1])- 1):
        scale = segLens[i]/imageLen
        angle = segAngles[i]
        position = currFracPoints[i]
        piece = copy.copy(points)
        piece = scaleImage(points,scale)
        piece = rotateImage(piece,angle)
        piece = translateImage(piece,position)
        newFractalPoints += piece
        lastPoint = newFractalPoints.pop()
    #for the last last point
    newFractalPoints.append(lastPoint)
    fractalPoints.append(newFractalPoints)
    purgePoints(data)
    freezePopulate(data)

###Fills up the freezePoints so freeze mode is possible    
def freezePopulate(data):
    for level in range(len(data.fractalPoints)):
        currPoints = data.fractalPoints[level]
        if level >= len(data.freezePoints):
            data.freezePoints.append(currPoints)

###Refreshes the fractal for every time a nav key is pressed
def fractalizeRefresh(data):
    if data.freeze == True:
        return
    if canRefresh(data):
        data.goBack = False
        data.fractalPoints = [copy.copy(data.points)]
        sideAdder(data)
        fractalize(data)
    else:
        data.fractalPoints = [copy.copy(data.points)]
        sideAdder(data)
        data.goBack = True

###determines if a fractal should refresh 
###or tell you to go back to prevent crashes
def canRefresh(data):
    currPoints = data.fractalPoints[0]
    for i in range(len(currPoints) - 1):
        p1 = currPoints[i]
        p2 = currPoints[i+1]
        if inBoard(data,p1,p2):
            return True
    return False

###purges points that are out of the screen so the program doesn't freeze up
def purgePoints(data):
    while True:
        fractalPtLvl = data.fractalPoints[-1]
        endpt1 = fractalPtLvl[-1] 
        endpt2 = fractalPtLvl[-2]
        purgeEnd = not inBoard(data,endpt1,endpt2)
        stpt1 = fractalPtLvl[0]
        stpt2 = fractalPtLvl[1]
        purgeSt = not inBoard(data,stpt1,stpt2)
        if len(fractalPtLvl) < data.minTopPoints:
            return
        if purgeSt:
            fractalPtLvl.pop(0)
        if purgeEnd:
            fractalPtLvl.pop()
        if not purgeSt and not purgeEnd:
            return

def resetFractal(data):
    data.fractalPoints = [copy.copy(data.points)]
    sideAdder(data)
    data.lvZoomVals = []
    data.purgedPoints = []
    data.purgedZooms = []

#######################################
##########Navigation Data##############
#######################################        

#finds the coordinate of a point after navigation
def navPoint(data,point):
    transPoint = translate(data.reticle,point)
    nPoint = zoom(data.center,transPoint,data.zoom)
    return nPoint

#translates a point according to your reticle
def translate(reticle,point):
    px = point[0]
    py = point[1]
    rx = reticle[0]
    ry = reticle[1]
    return (px + rx,py + ry)

#zooms into a a point that is the center
def zoom(center,transPoint,zoom):
    cx = center[0]
    cy = center[1]
    px = transPoint[0]
    py = transPoint[1]
    dx = px - cx
    dy = py - cy
    zoomx = dx * zoom + cx
    zoomy = dy * zoom + cy
    return (zoomx,zoomy)

#######################################
###In Board Checking Functions#########
#######################################        

#checks if a point is still in board after translation and zoom.
def inBoard(data,point1,point2 = None):
    if point2 == None:
        return onePointInBoard(data,point1)
    p1 = navPoint(data,point1)
    p2 = navPoint(data,point2)
    p1x = p1[0]
    p1y = p1[1]
    p2x = p2[0]
    p2y = p2[1]
    xOk = getXOk(p1x,p2x,data)    
    yOk = getYOk(p1y,p2y,data)    
    if not(xOk and yOk):
        return False
    return True

###to determine if one point is in the board
def onePointInBoard(data,point):
    p = navPoint(data,point)
    px = p[0]
    py = p[1]
    xInRange = data.margin < px < data.width - data.margin
    yInRange = data.optionPaneHeight < py < data.height - data.margin
    if not(xInRange and yInRange):
        return False
    return True

###determines if the y coordinates go across the board
def getYOk(p1y,p2y,data):
    y1UnderRange = p1y < data.optionPaneHeight
    y2UnderRange = p2y < data.optionPaneHeight
    y1OverRange = p1y > data.height - data.margin
    y2OverRange = p2y > data.height - data.margin
    y1inRange = data.optionPaneHeight <= p1y <= data.height - data.margin
    y2inRange = data.optionPaneHeight <= p2y <= data.height - data.margin
    yOk = False
    if y1inRange or y2inRange:
        yOk = True
    elif y1UnderRange and y2OverRange:
        yOk = True
    elif y2UnderRange and y1OverRange:
        yOk = True
    return yOk

###determines if the x coordinates cross the board
def getXOk(p1x,p2x,data):
    x1UnderRange = p1x < data.margin
    x2UnderRange = p2x < data.margin
    x1OverRange = p1x > data.width - data.margin
    x2OverRange = p2x > data.width - data.margin
    x1inRange = data.margin <= p1x <= data.width - data.margin
    x2inRange = data.margin <= p2x <= data.width - data.margin
    xOk = False
    if x1inRange or x2inRange:
        xOk = True
    elif x1UnderRange and x2OverRange:
        xOk = True
    elif x2UnderRange and x1OverRange:
        xOk = True
    return xOk

