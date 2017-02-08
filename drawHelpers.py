###drawHelpers
import copy
from dataHelpers import navPoint
from fractalizeHelpers import *
from saveHelpers import *
##########################################
###Main Screen Drawing####################
##########################################

#draws the UI
def drawLayout(canvas,data):
    drawWallPaperBack(canvas,data)
    drawShapes(canvas,data)
    if data.screenShot == True:
        filePath = "wallpapers/"+ data.selectedSave +".ps"
        canvas.postscript(file = filePath, colormode='color')
        data.screenShot = False
    drawGrid(canvas,data)
    drawShapes(canvas,data)
    drawOptionPane(canvas,data)
    drawText(canvas,data)
    drawSaveScreen(canvas,data)

#############HELPERS BELOW###########################

##########################################
###Save Screen Draw Functions#############
##########################################

###Draws Save Mode
def drawSaveScreen(canvas,data):
    if data.loadMode:
        drawSaveBack(canvas,data)
        drawSaveData(canvas,data)

###Draws the current save data on the save box
def drawSaveData(canvas,data):
    x1 = data.width/4 - data.margin
    x2 = data.width*3/4 + data.margin
    x = data.width/2
    y = data.height/4 + data.margin
    text = data.selectedSave
    y+= data.margin
    canvas.create_text(x,y,text = text)
    for filename in getAllSaves(data):
        index = getAllSaves(data).index(filename)+2+1/2
        if filename == data.selectedSave:
            fill = "yellow"
            y1 = data.height/4 + index*(data.margin)
            y2 = y1 + data.margin
            canvas.create_rectangle(x1,y1,x2,y2,fill=fill)
        y = data.height/4  + (index+1/2)*(data.margin)
        text = filename
        canvas.create_text(x,y,text=text)

###Draws the save Background
def drawSaveBack(canvas,data):
    linespace = data.margin*3/2
    x1 = data.width/4 - data.margin
    x2 = data.width*3/4 + data.margin
    y1 = data.height/4
    y2 = data.height*3/4
    fill = "white"
    canvas.create_rectangle(x1,y1,x2,y2,fill = fill)
    fill = "orange"
    y1 += 3/2*data.margin
    y2 = y1 + data.margin
    canvas.create_rectangle(x1,y1,x2,y2,fill = fill)
    text ="Enter-Save,Tab-Load,BckSpc-Delete,Arrows-Navigate,or type a name"
    x = data.width/2
    y = data.height/4 + data.margin
    canvas.create_text(x,y,text = text)

def drawWallPaperBack(canvas,data):
    x2 = data.width + 2*data.margin
    y2 = data.height
    canvas.create_rectangle(0,0,x2,y2,fill = "#113")

##########################################
###Background Drawing#####################
##########################################

#Draws the navy coordinate box.
def drawOptionPane(canvas,data):
    x1 = 0
    y1 = 0
    x2 = data.margin
    y2 = data.height
    fill = "navy"
    outline = "navy"
    canvas.create_rectangle(0,y1,x2,y2,fill=fill,outline=outline)
    x1 = data.width - data.margin
    y1 = 0
    x2 = data.width
    y2 = data.height
    canvas.create_rectangle(x1,y1,x2,y2,fill=fill,outline=outline)
    x1 = 0
    y1 = 0
    x2 = data.width
    y2 = data.optionPaneHeight
    canvas.create_rectangle(x1,y1,x2,y2,fill=fill,outline=outline)
    x1 = 0
    y1 = data.height - data.margin
    x2 = data.width
    y2 = data.height
    canvas.create_rectangle(x1,y1,x2,y2,fill=fill,outline=outline)
    
    

#draws the Grid for the coordinate box
def drawGrid(canvas,data):
    for row in range(data.rows):
        for col in range(data.cols):
            if row % data.gridSep == 0 or col % data.gridSep == 0:
                data.cellColor = "grey"
            else:
                data.cellColor = "navy"
            drawCell(canvas,data,row,col)

#draws the cells one by one for drawGrid
def drawCell(canvas,data,row,col):
    x1 = data.margin + col * data.sqSize
    y1 = data.optionPaneHeight + row * data.sqSize
    x2 = x1 + data.sqSize
    y2 = y1 + data.sqSize
    fill = "black"
    outline = data.cellColor
    width = 1
    canvas.create_rectangle(x1,y1,x2,y2,fill=fill,outline=outline,width = width)

#############################################
############User image drawing###############
#############################################

def drawImage(canvas,data,drawPoints,color):
    points = copy.deepcopy(drawPoints)
    def picture(canvas,points,color):
        r = 2
        fill = color
        if len(points) == 0:
            return
        if len(points) == 1:
            c = navPoint(data,points[0])
            cx = c[0]
            cy = c[1]
            canvas.create_oval(cx-r,cy-r,cx+r,cy+r,fill = fill)
            return
        else:
            p1 = navPoint(data,points[0])
            p2 = navPoint(data,points[1])
            c = p1
            cx = c[0]
            cy = c[1]
            canvas.create_line(p1[0],p1[1],p2[0],p2[1],fill=fill, width = 3)
            canvas.create_oval(cx-r,cy-r,cx+r,cy+r,fill = fill)
            points.pop(0)
            picture(canvas,points,color)
    return picture(canvas,points,color)

#draws the user made images
def drawShapes(canvas,data):
    drawPointsList = data.fractalPoints
    if data.freeze == True:
        drawPointsList = data.freezePoints
    color = data.initColor
    for drawPoints in drawPointsList:
        drawImage(canvas,data,drawPoints,color)
        color = changeColor(data,color)

#changes the color
def changeColor(data,color):
    colComps = data.posColorChars
    compr = colComps.index(color[1])
    compg = colComps.index(color[2])
    compb = colComps.index(color[3])
    colorVar1 = colComps[compr] 
    colorVar2 = colComps[data.colorFunc(compg)]
    colorVar3 = colComps[data.colorFunc(data.colorFunc(compb))]
    newColor = "#"+colorVar1+colorVar2+colorVar3
    return newColor


###############################################
########TEXT Drawing###########################
###############################################

#Draws all of the screen text
def drawText(canvas,data):
    drawTitleAndMore(canvas,data)
    if data.mode == data.design:
        drawDesignHelp(canvas,data)
    else:
        drawBuildHelp(canvas,data)
    if data.goBack == True:
        drawGoBack(canvas,data)

###############################################
########TEXT HELPERS(SIMPLE)###################
###############################################
def drawDesignHelp(canvas,data):
    x = data.margin
    y = data.margin + data.margin
    font = ("Purisa", 7)
    fill = "orange"
    anchor = "w"
    text = "### Use Num Keys to increase number of sides. Ex. hit 3 for 3 sides"
    canvas.create_text(x,y,text=text, font = font,fill = fill,anchor = anchor)
    text = "###Click to draw an image to fractalize."
    y += data.margin//2
    canvas.create_text(x,y,text=text, font = font,fill = fill,anchor = anchor)
    text = "###When you are ready, press B to build your fractal"
    x = data.width //2
    y = data.height - data.margin//2
    font = ("Purisa", 9)
    anchor = "center"
    canvas.create_text(x,y,text=text, font = font,fill = fill,anchor = anchor)

def drawBuildHelp(canvas,data):
    x = data.margin
    y = data.margin + data.margin
    font = ("Purisa", 7)
    fill = "orange"
    anchor = "w"
    text = """### Use I and O keys to zoom in and out.\
            ### Use F key to toggle freezing the current fractal image."""
    canvas.create_text(x,y,text=text, font = font,fill = fill,anchor = anchor)
    text = "###Use WASD keys to navigate your fractal."
    y += data.margin//2
    canvas.create_text(x,y,text=text, font = font,fill = fill,anchor = anchor)
    text = "###To reset Navigation, press R  ###Press Q to save image as .ps"
    x = data.width //2
    y = data.height - data.margin//2
    font = ("Purisa", 9)
    anchor = "center"
    canvas.create_text(x,y,text=text, font = font,fill = fill,anchor = anchor)

def drawGoBack(canvas,data):
    x = data.width//2
    y = data.height//2
    font = ("Purisa", 18)
    fill = "orange"
    text = "Go Back!!"
    canvas.create_text(x,y,text=text, font = font,fill = fill)

def drawTitleAndMore(canvas,data):
    x = data.width/2
    y = data.margin
    font = ("Purisa", 14,"bold underline")
    fill = "red"
    text = "Fractal Maker Suite"
    canvas.create_text(x,y,text=text, font = font,fill = fill )
    fill = "orange"
    text = "Freeze : "
    fStatus = False
    if data.freeze:
        fStatus = not fStatus
    text += str(fStatus) 
    font = ("Purisa",12)
    anchor = "w"
    x = data.width * 3/4
    canvas.create_text(x,y,text=text, font = font,fill = fill,anchor = anchor)
    y += data.margin
    text = "Mode : "
    mode = "DESIGN"
    if data.mode == data.build:
        mode = "BUILD"
    text += mode 
    canvas.create_text(x,y,text=text, font = font,fill = fill,anchor = anchor)
    x = data.margin
    y = data.margin
    anchor = "w"
    font = ("Purisa",9)
    text = "###Press escape to bring up save screen"
    canvas.create_text(x,y,text=text, font = font,fill = fill,anchor = anchor)
    
