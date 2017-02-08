#########################################################
####inspired by https://scratch.mit.edu/projects/1360458/
#########################################################

####################
###Features#########
####################

# Draw an Image to fractalize.
# fractalize the image with zoom in and zoom out support
# anti segments for dragon fractal support
# save fractals and screenshot zooms
# load data from the library
# fractal brush mode where you can place fractals you have made before in combo


from tkinter import *
import copy
from drawHelpers import *
from inputHelpers import *
from dataHelpers import *
from saveHelpers import *

###############################
###Initialization Of Data######
###############################
            
def init(data):
    initModes(data)
    initFormat(data)
    initNav(data)
    initShapes(data)
    initFiles(data)
###############################
###Input Handlers##############
###############################

def mousePressed(event, data):
    if data.mode == data.design and data.loadMode == False:
        addPoint(data,event.x,event.y)
        
def keyPressed(event, data):
    checkLoadModeInput(event,data)
    if data.loadMode == False:
        checkNumInput(event,data)
        checkBkey(event,data)
        checkSpaceKey(event,data)
        checkNavInput(event,data)
        checkFKey(event,data)  
        checkQKey(event,data)   
    
###############################
###View Functions##############
###############################

def redrawAll(canvas, data):
    drawLayout(canvas,data)

###############################
###########Timer Handling######
###############################            
def timerFired(data):
    pass

###############################
# use the run function as-is ##
###############################

def run(width=300, height=300):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='white', width=0)
        redrawAll(canvas, data)
        canvas.update()    

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 100 # milliseconds
    init(data)
    # create the root and the canvas
    root = Tk()
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")

run(900,600)
