#import modules
from psychopy import core, visual, gui, data, event, sound
from psychopy.tools.filetools import fromFile, toFile
import numpy, random
import pandas as pd # needed for reading csv files
import random 

# STEP 1: LOAD PARAMS
#########
try:  
    expInfo = fromFile('lastParams.pickle')
except:  
    # create dictionary of robots that are needed
    expInfo = {
    "robot_1":"robot_imgs/stevie.png",
    "robot_2":"robot_imgs/pr2.png",
    "robot_3":"robot_imgs/pepper.png",
    "robot_4":"robot_imgs/sciprr.png",
    "robot_5":"robot_imgs/icub.png",
    "robot_6":"robot_imgs/flash.png",
    "robot_7":"robot_imgs/g5.png",
    "robot_8":"robot_imgs/poli.png",
    "robots": ["robot_1","robot_2","robot_3","robot_4","robot_5","robot_6","robot_7","robot_8"],
    #"testing_list": ["stevie","pr2","pepper","sciprr","icub","flash","g5","poli"]
    "testing_list": ["stevie","pr2"]
    }
    expInfo['dateStr'] = data.getDateStr() 
    toFile('lastParams.pickle', expInfo)
expInfo['dateStr'] = data.getDateStr()  # add the current time


# STEP 2: DEFINE FUNCTIONS
#########
def playSound(voice_clip):
    voice = sound.Sound(voice_clip)
    waitTime = voice.getDuration()
    listenText = visual.TextStim(win,pos=[0,450],text="Listen to the sound",height=40,wrapWidth=1000,units='pix')
    fixation = visual.GratingStim(win, color=-1, colorSpace='rgb',
                              tex=None, mask='cross', size=10)
    listenText.draw()
    fixation.draw()
    win.flip()
    voice.play()
    core.wait(waitTime)

def selectRobot(choice, list, ignore=None):   
    if ignore:
        print('ignored')
    else:
        for item in list:
            item.draw()
    
    # STEP 05: ADD TEXT TO THE SCREEN
    if choice == 0:
        choice = '1st'
    elif choice == 1:
        choice = '2nd'
    elif choice == 2:
        choice = '3rd'

    message1 = visual.TextStim(win, 
    pos=[0,450],
    text="What robot best suits the voice: %s choice?" % choice,
    height=40, wrapWidth=1000, units='pix'
    )
    message1.draw()

def updateRobotList():
    return([img_robo1,img_robo2,img_robo3,img_robo4,img_robo5,img_robo6,img_robo7,img_robo8])

def checkRobot():
    while not event.getKeys(keyList=['e']):
        if sum(mouse.getPressed()) and img_robo1.contains(mouse):
            return ["robot_1", img_robo1, clock.getTime()]
        elif sum(mouse.getPressed()) and img_robo2.contains(mouse):
            return ["robot_2", img_robo2, clock.getTime()]
        elif sum(mouse.getPressed()) and img_robo3.contains(mouse):
            return ["robot_3", img_robo3, clock.getTime()]
        elif sum(mouse.getPressed()) and img_robo4.contains(mouse):
            return ["robot_4", img_robo4, clock.getTime()]
        elif sum(mouse.getPressed()) and img_robo5.contains(mouse):
            return ["robot_5", img_robo5, clock.getTime()]
        elif sum(mouse.getPressed()) and img_robo6.contains(mouse):
            return ["robot_6", img_robo6, clock.getTime()]
        elif sum(mouse.getPressed()) and img_robo7.contains(mouse):
            return ["robot_7", img_robo7, clock.getTime()]
        elif sum(mouse.getPressed()) and img_robo8.contains(mouse):
            return ["robot_8", img_robo8, clock.getTime()]

def getRating(robot_img=0):
    scales = '1=Extremely Suitable, 9=Extremely Unsuitable'
    label = ['1','2','3','4','5']
    item = visual.TextStim(win, 
        pos=[300,450],
        text="How suitable do you think the voice is for the robot?",
        height=40, wrapWidth=1000, units='pix'
        )

    img_robot = visual.ImageStim(win,ori=0, size=(img_width,img_height), units='pix',
        image=robot_img,    
        pos=(-400, 0)
        )
    ratingScale = visual.RatingScale(win, low=1, high=5, pos=(300,0), size=1, textSize = 0.7, showAccept=True, acceptPreText="click point on scale", acceptSize=1.25, labels = label)
    while ratingScale.noResponse:
        item.draw()
        img_robot.draw()
        ratingScale.draw()
        win.flip()
    print('rating was %i' % ratingScale.getRating() )
    return ratingScale.getRating()

def saveData(csvfile,data):
    csvfile.write(data) # todo ID, suitability

def shuffleFiles(soundfiles, soundID):
    random.sample(range(0, len(soundID)), len(soundID))

def test_1(soundfiles, soundID, ID=0):

    if (ID == 1):        
        gui.show()
        subj_id = gui.data[0]
    else:
        subj_id = 'dummy'

    # make a text file to save data
    fileName = expInfo['dateStr'] + expInfo['dateStr']
    dataFile = open('data/'+fileName+'.csv', 'w')  
    dataFile.write('ID, voice, choice1, t1, s1, choice2, t2, s2, choice3, t3, s3 \n') # todo ID, suitability

    order = random.sample(range(0, len(robots)), len(robots))
    soundfiles = [ soundfiles[i] for i in order]
    soundID = [ soundID[i] for i in order]

    counter = 0
    for voices in soundfiles:
        tempResponse = [subj_id, soundID[counter]]  
        counter+=1
        robot_list = updateRobotList()
        # first turn 
        # a) play 3 sound clips at random
        for i in range(0,3):
            playSound(random.choice(voices))
            core.wait(0.5)        

        # b) splash screen with options     
   
        for i in range(0,3):
            selectRobot(i,robot_list)
            win.flip()
            clock.reset()
            [name, clicked, timer] = checkRobot()
            print("time taken was %f seconds" % timer)
            rating = getRating(expInfo[name])

            # todo save details of choice
            robot_list.remove(clicked)
            tempResponse.append(name)
            tempResponse.append(str(timer))
            tempResponse.append(str(rating))
            core.wait(0.2)
        tempResponse = ','.join(tempResponse)
        saveData(dataFile, tempResponse+'\n')
        print(tempResponse)
        
if __name__ == "__main__":    #event.waitKeys()
    # STEP 03: CREATE A WINDOW AND CLOCK
    #########
    # setup GUI - this may or may not be called upon
    gui = gui.Dlg()
    gui.addField("Subject ID:")


    win = visual.Window(
        size=[1440/2, 900], 
        fullscr=True, 
        screen=0,
        units='pix'
        )

    clock = core.Clock()
    mouse = event.Mouse(visible=True,newPos=False,win=win)

    #print(pepper)
    ## READ IN ROBOTS FROM SPREADSHEET AND LINK WITH ID AND FILE PATH
    # TODO
    img_width = 768/2.5
    img_height = 950/2.5
    buffer = 50
    spacing = img_width + buffer

    img_robo1 = visual.ImageStim(win,ori=0, size=(img_width,img_height), units='pix',
        image=expInfo["robot_1"],    
        pos=((buffer/2 + img_width/2), 150)
        )
    img_robo2 = visual.ImageStim(win,ori=0, size=(img_width,img_height), units='pix',
        image=expInfo["robot_2"],    
        pos=((buffer/2 + img_width/2), -275)
        )
    img_robo3 = visual.ImageStim(win,ori=0, size=(img_width,img_height), units='pix',
        image=expInfo["robot_3"],    
        pos=((buffer/2 + img_width/2) + spacing, 150)
        )
    img_robo4 = visual.ImageStim(win,ori=0, size=(img_width,img_height), units='pix',
        image=expInfo["robot_4"],    
        pos=((buffer/2 + img_width/2) + spacing, -275)
        )
    img_robo5 = visual.ImageStim(win,ori=0, size=(img_width,img_height), units='pix',
        image=expInfo["robot_5"],    
        pos=(-(buffer/2 + img_width/2), 150)
        )
    img_robo6 = visual.ImageStim(win,ori=0, size=(img_width,img_height), units='pix',
        image=expInfo["robot_6"],    
        pos=(-(buffer/2 + img_width/2), -275)
        )
    img_robo7 = visual.ImageStim(win,ori=0, size=(img_width,img_height), units='pix',
        image=expInfo["robot_7"],    
        pos=(-(buffer/2 + img_width/2) - spacing, 150)
        )
    img_robo8 = visual.ImageStim(win,ori=0, size=(img_width,img_height), units='pix',
        image=expInfo["robot_8"],    
        pos=(-(buffer/2 + img_width/2) - spacing, -275)
        )
    

    # part 0: splash screen for instructions, info capture and informed consent
    ## todo 

    # part 1: test with robot voices and images top three selection
    # get confidence for each choice

        # STEP 04: LOAD SOUND AND IMAGES OF ROBOT
    ## READ IN SOUNDS FROM SPREADSHEET AND LINK WITH ID AND FILE PATH
    voices = pd.read_csv('sounds_t3.csv')
    #voices2  = [voices.poli, voices.pr2]
    robots = list(voices)
    voices['pr2'].tolist()
    testing_list = []
    #for i in list(voices):        
    #    
    for i in range(0,len(list(voices))):
        testing_list.append(voices[robots[i]].tolist())
    #    
    #    print (testing_list[robots])
    #print( testing_list )
    #voices2  = [testing_list[0],testing_list[1]]

    print(testing_list)
    test_1(testing_list,list(voices))

    ################################
    #selectRobot(0)
    #win.flip()
    #event.waitKeys() 
# part 2: interactive demo with user in context scenario


# part 3: same as part 1, but with fewer choices

'''
# for each sound in sound list

# STEP 04: PLOT IMAGES ON SCREEN
#########


robotInfo = {
"robot_1":"img_robo1",
"robot_2":"img_robo2",
}





win.flip()

# STEP 06: CAPTURE WHICH IMAGE WAS CLICKED
# option 1: use keys
#keys = event.waitKeys(keyList=["1","2","3","4","5","6","7","8"],timeStamped=clock) 
#print(keys)

while not event.getKeys(keyList=[e]):
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
 # wait for participant to respond
'''

win.close()
core.quit()