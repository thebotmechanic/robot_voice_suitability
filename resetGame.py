#import modules
from psychopy import core, visual, gui, data, event, sound, logging
from psychopy.tools.filetools import fromFile, toFile
import numpy, random
import pandas as pd # needed for reading csv files
import random 
logging.console.setLevel(logging.WARNING)

class robotVoiceEval:
	# initialise test images
	# index images with sound
	# turn gui on/off
	# initialise psypy 
	def __init__(self, guiID=True, logging=True, display=False, shorten=True):
		# import test images
		try:  
		    self.expInfo = fromFile('lastParams.pickle')
		except:  
		    # create dictionary of robots that are needed
		    self.expInfo = {
		    "robot_1":"robot_imgs/stevie-rs.png",
		    "robot_2":"robot_imgs/pr2-rs.png",
		    "robot_3":"robot_imgs/pepper-rs.png",
		    "robot_4":"robot_imgs/sciprr-rs.png",
		    "robot_5":"robot_imgs/icub-rs.png",
		    "robot_6":"robot_imgs/flash-rs.png",
		    "robot_7":"robot_imgs/g5-rs.png",
		    "robot_8":"robot_imgs/poli-rs.png",
		    "button":"robot_imgs/button.png",
		    "robots": ["robot_1","robot_2","robot_3","robot_4","robot_5","robot_6","robot_7","robot_8"],
		    "testing_list": ["stevie","pr2","pepper","sciprr","icub","flash","g5","poli"]
		    }
		    self.expInfo['dateStr'] = data.getDateStr() 
		    toFile('lastParams.pickle', self.expInfo)

		# prompt for ID - needs to be before win opened
		if (guiID==True):    
			self.ID  = self.getID()
		else:
			self.ID = 'dummy'

		# setup window
		self.win = visual.Window(
			size=[1440/2, 900], 
			fullscr=display, 
			screen=0,
			units='pix')

		# setup clock and mouse events events
		self.clock = core.Clock()
		self.mouse = event.Mouse(visible=True,newPos=False,win=self.win)

	# opens a dialog box to get user ID
	def getID(self):
		p1 = gui.Dlg()
		p1.addField("Subject ID:")    
		p1.show()
		return p1.data[0]

	# load voices passes in voicefile arg 
	## todo repeating work here

	# create splash screen that requires buttonpress to advance
	def splash(self, txtstring, col_arg=0):
		if col_arg == 1:
			print('background is true')
			back = visual.Rect(self.win, width=1920, height=1080, fillColor='black')
			back.draw()

		item = visual.TextStim(self.win, 
		    pos=[0,0],
		    text=txtstring,
		    height=60, wrapWidth=1500, units='pix'
		    )
		advance = visual.TextStim(self.win, 
		    pos=[0,-400],
		    text="press any button to continue",
		    height=30, wrapWidth=1500, units='pix'
		    )

		item.draw()
		advance.draw()
		self.win.flip()
		event.waitKeys()




if __name__ == "__main__":    #event.waitKeys()
	# use a loop structure like this to repeat the experiment
	for i in range(0,3):
		ex1 = robotVoiceEval(guiID=True, display=False, shorten=False)
		ex1.splash('TEST SCREEN')

		# psychopy cannot have dialog box open at the same time as visual.Window() object
		# Make sure this is included or it will crash
		ex1.win.close()
		
