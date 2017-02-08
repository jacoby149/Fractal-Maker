import copy
from dataHelpers import *
from saveHelpers import *
###inputHelpers

#######################################
##########Number Input#################
#######################################

def checkNumInput(event,data):
    numpress = event.keysym in list(map(lambda x:str(x),list(range(1,10))))
    if numpress and data.mode == data.design:
        data.sides = int(event.keysym)
        data.fractalPoints = [copy.copy(data.points)]
        sideAdder(data)

#######################################
##########Load Mode Input##############
#######################################

def checkLoadModeInput(event,data):
    on = data.loadMode
    if event.keysym == "Up" and on:
        downSelected(data)
    elif event.keysym == "Down" and on:
        upSelected(data)
    elif event.keysym == "Escape":
        data.loadMode = not on
    elif event.keysym == "Return" and on:
        saves = getAllSaves(data)
        if len(saves) < 9:
            save(data)
    elif event.keysym == "Tab" and on:
        load(data)
    elif event.keysym == "Delete" and on:
        saves = getAllSaves(data)
        if len(saves) > 1:
            delete(data)
            saves = getAllSaves(data)
            data.selectedSave = saves[0]
    elif event.keysym.isalpha() and len(event.keysym) == 1 and on:
        data.selectedSave = data.selectedSave + event.keysym
    elif event.keysym == "BackSpace" and on:
        if len(data.selectedSave)>=1:
            data.selectedSave = data.selectedSave[:-1]

#######################################
##########mousePressed Input###########
#######################################

#when mouse clicked add point
def addPoint(data,x,y):
    sqSize = data.sqSize
    gridY = round(y / data.sqSize) * data.sqSize
    gridX = round(x /data.sqSize) * data.sqSize
    pointTuple = (gridX,gridY)
    if inBoard(data, pointTuple):
        data.points.append(pointTuple)
        data.fractalPoints = [copy.copy(data.points)]
        sideAdder(data)

#######################################
##########High Level keyPressed Input##
#######################################

#SpaceBar
#pops a point
def checkSpaceKey(event,data):
    spaceBarBools = len(data.points) != 0 and data.mode == data.design
    if event.keysym == "space" and spaceBarBools:
        popPoint(data)

def popPoint(data):
    data.points.pop()
    data.fractalPoints = [copy.copy(data.points)]
    sideAdder(data)

#B Button
#for Toggling mode between build and design mode
#resets nav when going from build to design
def checkBkey(event,data):
    buildBools = len(data.points) > 2 and data.points[0] != data.points[-1]
    if event.keysym == "b" and buildBools:
        data.freezePoints = []
        data.freeze = False
        fractalize(data)
        modeToggle(data)

def modeToggle(data):
    if data.mode == data.design:
        data.mode = data.build
    else:
        resetNav(data)
        resetFractal(data)
        data.mode = data.design

#F key
def checkFKey(event,data):
    inBuild = data.mode == data.build
    if event.keysym == "f" and inBuild:
        if data.freeze == True:
            data.freezePoints = []
        data.freeze = not data.freeze
        fractalizeRefresh(data)

#Q key
def checkQKey(event,data):
    if event.keysym == "q":
        data.screenShot = True

#######################################
##########Navigation Input#############
#######################################

#General Navigation Input
def checkNavInput(event,data):
    if event.keysym == "i" and data.mode == data.build:
        zoomIn(data)
        fractalizeRefresh(data)    
    elif event.keysym == "o" and data.mode == data.build:
        zoomOut(data)
        fractalizeRefresh(data)
    elif event.keysym in ["w","a","s","d"] and data.mode == data.build:
        shiftReticle(data,event.keysym)
        fractalizeRefresh(data)
    elif event.keysym == "r":
        resetNav(data)
        fractalizeRefresh(data)
#WASD Keys
#moves the reticle with the zoom accounted for
def shiftReticle(data,key):
    x1 = data.reticle[0]
    y1 = data.reticle[1]
    dx = 0
    dy = 0
    if key == "w":
        dy = data.speed/data.zoom
    elif key == "a":
        dx = data.speed/data.zoom
    elif key == "s":
        dy = -data.speed/data.zoom
    else:
        dx = -data.speed/data.zoom
    data.reticle = (x1+dx,y1+dy)
    
#R Key
#resets the navigation point
def resetNav(data):
    data.zoom = 1
    data.reticle = (0,0)

#I key
#zooms in
def zoomIn(data):
    data.zoom *= data.zoomSpeed

#O key    
#zooms out    
def zoomOut(data):
    data.zoom /= data.zoomSpeed

