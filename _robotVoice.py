#import modules
from psychopy import core, visual, gui, data, event, sound
from psychopy.tools.filetools import fromFile, toFile
import numpy, random

# STEP 02: SAVE A BUNCH OF PARAMS
#########
try:  
    expInfo = fromFile('lastParams.pickle')
except:  
    # create dictionary of terms that are needed
    expInfo = {
    "robot_1":"robot_imgs/stevie.png",
    "robot_2":"robot_imgs/pr2.png",
    "robot_3":"robot_imgs/pepper.png"
    }
    toFile('lastParams.pickle', expInfo)
expInfo['dateStr'] = data.getDateStr()  # add the current time

# optional: open a dialog box to get input or change params - see t2.py
'''
gui = gui.Dlg()
gui.addField("Subject ID:")
gui.addField("Condition Number:")
gui.show()
print(gui.data)
subj_id = gui.data[0]
cond_num = int(gui.data[1])
'''

# STEP 03: CREATE A WINDOW AND CLOCK
#########
win = visual.Window(
    size=[1440, 810], 
    fullscr=True, 
    screen=0,
    units='pix'
    )

clock = core.Clock()
mouse = event.Mouse(visible=True,newPos=False,win=win)

# STEP 04: PLAY SOUND 
def playSound(voice_clip):
    voice = sound.Sound(voice_clip)
    waitTime = voice.getDuration()
    listenText = visual.TextStim(win,pos=[0,450],text="Listen to the sound",height=40,wrapWidth=1000,units='pix')
    listenText.draw()
    win.flip()
    voice.play()
    core.wait(waitTime)
playSound('sounds/pepper_sydney/sentence_02.wav')

# STEP 04: PLOT IMAGES ON SCREEN
#########
def selectRobot(choice, ignore=None):
       
    selectRobot.img_robo1 = visual.ImageStim(win=win,
        image=expInfo["robot_1"],
        ori=0, 
        pos=(0, 150), 
        size=(768/2.5,950/2.5),
        units='pix'
        )
    selectRobot.img_robo2 = visual.ImageStim(win=win,
        image=expInfo["robot_2"],
        ori=0, 
        pos=(0, -300), 
        size=(768/2.5,950/2.5),
        units='pix'
        )

    # for loop to draw robot 
    # check ignore and remove accordingly
    selectRobot.img_robo1.draw()
    selectRobot.img_robo2.draw()
        
    # STEP 05: ADD TEXT TO THE SCREEN
    message1 = visual.TextStim(win, 
    pos=[0,450],
    text="What robot best suits the voice: {choice} choice?",
    height=40,
    wrapWidth=1000,
    units='pix'
    )
    message1.draw()
    win.flip()

selectRobot('1st')

    # STEP 06: CAPTURE WHICH IMAGE WAS CLICKED
    # option 1: use keys
    #keys = event.waitKeys(keyList=["1","2","3","4","5","6","7","8"],timeStamped=clock) 
    #print(keys)
while not event.getKeys(keyList=["e"]):
        #mouse= event.Mouse()
    # option 2: mouse press
    print(selectRobot.img_robo1.contains(mouse))
    if sum(mouse.getPressed()) and selectRobot.img_robo1.contains(mouse):
        box4 = visual.Rect(win=win,lineColor="black",fillColor="LightBlue",size=[100,50],pos=[-200,-90])
        box4.draw()
        win.flip()
        print("I love fat titties")

#if sum(mouse.getPressed()) and myShape.contains(mouse):
#    print("My shape was pressed")
##############

event.waitKeys()  # wait for participant to respond

win.close()
core.quit()