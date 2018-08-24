#import modules
from psychopy import core, visual, gui, data, event, sound
from psychopy.tools.filetools import fromFile, toFile
import numpy, random
import pandas as pd # needed for reading csv files

# STEP 02: SAVE A BUNCH OF PARAMS
#########
try:  
    expInfo = fromFile('lastParams.pickle')
except:  
    # create dictionary of terms that are needed
    expInfo = {
    "robot_1":"robot_imgs/stevie.png",
    "robot_2":"robot_imgs/pr2.png",
    "robot_3":"robot_imgs/pepper.png",
    "robots": ["robot_1","robot_2","robot_3"]
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
    size=[1440/2, 900], 
    fullscr=False, 
    screen=0,
    units='pix'
    )

clock = core.Clock()
mouse = event.Mouse(visible=True,newPos=False,win=win)

# STEP 04: PLAY SOUND 
## READ IN SOUNDS FROM SPREADSHEET AND LINK WITH ID AND FILE PATH
voices = pd.read_csv('sounds.csv')
pepper = voices.task_1 #you can also use df['column_name']
print(pepper)




def playSound(voice_clip):
    voice = sound.Sound(voice_clip)
    waitTime = voice.getDuration()
    listenText = visual.TextStim(win,pos=[0,450],text="Listen to the sound",height=40,wrapWidth=1000,units='pix')
    listenText.draw()
    win.flip()
    voice.play()
    core.wait(waitTime)
#playSound('sounds/pepper_sydney/sentence_02.wav')

# for each sound in sound list
for voice in pepper:
    playSound(voice)
# STEP 04: PLOT IMAGES ON SCREEN
#########
img_robo1 = visual.ImageStim(win,
    image=expInfo["robot_1"],
    ori=0, 
    pos=(0, 150), 
    size=(768/2.5,950/2.5),
    units='pix'
    )
img_robo2 = visual.ImageStim(win,
    image=expInfo["robot_2"],
    ori=0, 
    pos=(0, -300), 
    size=(768/2.5,950/2.5),
    units='pix'
    )

robotInfo = {
"robot_1":"img_robo1",
"robot_2":"img_robo2",
}
robot_list = [img_robo1,img_robo2]

def selectRobot(choice, ignore=None):
   
    if ignore:
        print('ignored')
    else:
        for item in robot_list:
            item.draw()
    
    # STEP 05: ADD TEXT TO THE SCREEN
    message1 = visual.TextStim(win, 
    pos=[0,450],
    text="What robot best suits the voice: %s choice?" % choice,
    height=40,
    wrapWidth=1000,
    units='pix'
    )
    message1.draw()

selectRobot('1st')


win.flip()

# STEP 06: CAPTURE WHICH IMAGE WAS CLICKED
# option 1: use keys
#keys = event.waitKeys(keyList=["1","2","3","4","5","6","7","8"],timeStamped=clock) 
#print(keys)

while not event.getKeys():
    if sum(mouse.getPressed()) and img_robo1.contains(mouse):
        robot_list.remove(img_robo2)
        selectRobot('2nd')
        win.flip()
        print('mouse pressed')
        core.wait(0.2)
#if sum(mouse.getPressed()) and myShape.contains(mouse):
#    print("My shape was pressed")
##############

#win.flip()
event.waitKeys()  # wait for participant to respond

win.close()
core.quit()