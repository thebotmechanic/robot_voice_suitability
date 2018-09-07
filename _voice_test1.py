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
		    "robot_1":"robot_imgs/stevie.png",
		    "robot_2":"robot_imgs/pr2.png",
		    "robot_3":"robot_imgs/pepper.png",
		    "robot_4":"robot_imgs/sciprr.png",
		    "robot_5":"robot_imgs/icub.png",
		    "robot_6":"robot_imgs/flash.png",
		    "robot_7":"robot_imgs/g5.png",
		    "robot_8":"robot_imgs/poli.png",
		    "button":"robot_imgs/button.png",
		    "robots": ["robot_1","robot_2","robot_3","robot_4","robot_5","robot_6","robot_7","robot_8"],
		    "testing_list": ["stevie","pr2","pepper","sciprr","icub","flash","g5","poli"]
		    }
		    self.expInfo['dateStr'] = data.getDateStr() 
		    toFile('lastParams.pickle', self.expInfo)
		self.expInfo['dateStr'] = data.getDateStr()  # add the current time

		# index voices with images
		self.soundLink = {
		 "stevie":[1], 		# CEREPROC GILES
		 "pr2":[2,4],		# DAVID
		 "pepper":[3],		# PEPPER DEFAULT
		 "sciprr":[4,2],	# DAVID
		 "icub":[5,7],		# ACAPELA ROD
		 "flash":[6],		# CEREPROC SCOTTISH
		 "g5":[7,5],		# ACAPELA ROD
		 "poli":[8]}		# AMAZON POLLY KIMBERLY

		# prompt for ID - needs to be before win opened
		if (guiID==True):    
			self.ID  = self.getID()
		else:
			self.ID = 'dummy'

		# Open log file
		if (logging==True):    
			self.openLogFile()

		# setup window
		self.win = visual.Window(
			size=[1440/2, 900], 
			fullscr=display, 
			screen=0,
			units='pix')

		# setup clock and mouse events events
		self.clock = core.Clock()
		self.mouse = event.Mouse(visible=True,newPos=False,win=self.win)

		# setting for debugging
		if shorten:
			self.shorten = shorten

	# opens a dialog box to get user ID
	def getID(self):
		p1 = gui.Dlg()
		p1.addField("Subject ID:")    
		p1.show()
		return p1.data[0]

	# initialise log file
	def openLogFile(self):
		fileName = self.expInfo['dateStr'] + self.expInfo['dateStr']
		self.dataFile = open('data/'+fileName+'.csv', 'w')  
		self.dataFile.write('ID, voice, choice1, t1, s1, choice2, t2, s2, choice3, t3, s3 \n') # todo ID, suitability

	# saves stored data to log file
	def saveData(self,data):
		self.dataFile.write(data) # todo ID, suitability

	# load voices passes in voicefile arg 
	def loadVoices(self, voicefile):
			voices = pd.read_csv(voicefile) # read csv
			robots = list(voices)

			# for full set of voices
			testing_list = []
			for i in range(0,len(robots)):
				testing_list.append(voices[robots[i]].tolist())

			# for degbugging (fewer voices)
			testing_list2 = []
			robots2 = robots
			if (self.shorten is True):
				del robots2[2:5] # delete voices 2-5 

			for i in range(0,len(robots2)):
				testing_list2.append(voices[robots2[i]].tolist())

			return [testing_list2, robots2]

	# randomises the order of voices in a list 
	def randomiseVoices(self, soundfiles, soundID):
		# create ranodm order
		shuffle = random.sample(range(0, len(soundID)), len(soundID))
		# sort files and fileIDs according to order
		soundfiles = [ soundfiles[i] for i in shuffle]
		soundID = [ soundID[i] for i in shuffle]

		# returns [randomised list, index to randomised list]
		return [soundfiles, soundID]

	# play voice passed in arg, and wait until voice completed before updating screen
	def speak(self,voice_clip, wait=True):
		voice = sound.Sound(voice_clip)
		waitTime = voice.getDuration()
		## todo - this part could be initialised in init function
		listenText = visual.TextStim(self.win,pos=[0,450],text="Listen to the sound",height=40,wrapWidth=1000,units='pix')
		fixation = visual.GratingStim(self.win, color=-1, colorSpace='rgb',
		                          tex=None, mask='cross', size=10)
		listenText.draw()
		fixation.draw()
		self.win.flip()
		voice.play()

		# wait until voice has finished playing before updating screen
		if wait:
			core.wait(waitTime)
	
	# called at the start of program to place robots on the screen
	def updateRobotList(self, test=1, img_width=768/2.5,img_height=950/2.5):
		# initialise robots that will be used for the study
		self.img_robo1 = visual.ImageStim(self.win, units='pix', size=(img_width,img_height), image=self.expInfo["robot_1"])    
		self.img_robo2 = visual.ImageStim(self.win, units='pix', size=(img_width,img_height), image=self.expInfo["robot_2"])    
		self.img_robo3 = visual.ImageStim(self.win, units='pix', size=(img_width,img_height), image=self.expInfo["robot_3"])    
		self.img_robo4 = visual.ImageStim(self.win, units='pix', size=(img_width,img_height), image=self.expInfo["robot_4"])    
		self.img_robo5 = visual.ImageStim(self.win, units='pix', size=(img_width,img_height), image=self.expInfo["robot_5"])    
		self.img_robo6 = visual.ImageStim(self.win, units='pix', size=(img_width,img_height), image=self.expInfo["robot_6"])    
		self.img_robo7 = visual.ImageStim(self.win, units='pix', size=(img_width,img_height), image=self.expInfo["robot_7"])    
		self.img_robo8 = visual.ImageStim(self.win, units='pix', size=(img_width,img_height), image=self.expInfo["robot_8"])    
		self.button = visual.ImageStim(self.win, units='pix', size=(727/3,432/3), image=self.expInfo["button"])    
		self.robot_list = [self.img_robo1,self.img_robo2,self.img_robo3,self.img_robo4,self.img_robo5,self.img_robo6,self.img_robo7,self.img_robo8, self.button]

		# for test 1
		if test==1:
			# define settings for how images are displayed
			top_spacing = 160
			bottom_spacing = 285
			buffer = 50
			offset = -200
			spacing = img_width + buffer

			# place robots on the screen
			self.img_robo1.pos=((buffer/2 + img_width/2) + offset, top_spacing)
			self.img_robo2.pos=((buffer/2 + img_width/2) + offset, -bottom_spacing)
			self.img_robo3.pos=((buffer/2 + img_width/2) + spacing+offset, top_spacing)
			self.img_robo4.pos=((buffer/2 + img_width/2) + spacing+offset, -bottom_spacing)
			self.img_robo5.pos=(-(buffer/2 + img_width/2) + offset, top_spacing)
			self.img_robo6.pos=(-(buffer/2 + img_width/2) + offset, -bottom_spacing)
			self.img_robo7.pos=(-(buffer/2 + img_width/2) - spacing+offset, top_spacing)
			self.img_robo8.pos=(-(buffer/2 + img_width/2) - spacing+offset, -bottom_spacing)
			self.button.pos=(700, 0)

		## todo - update for tests 2 and 3
		elif test ==2:
			#set way 
			print("test 2")
		elif test==3:
			#set way
			print("test 2")

	# returns robot selected for given stimuluus
	# choice refers to selection number
	# list refers to avalable robots
	# index refers to 
	# filter refers to not showing all robots
	def selectRobot(self, choice, list, index = "dummy", ignore=None, filter=False):   

		# if we only want to show a selection of robots
		if filter is True:
			new_list = []
			temp_list = list[0:len(list)-1] # copy all except button
			# identify robot associated with voice
			print(index)
			val = self.soundLink[index]
			val[:] = [x - 1 for x in val]
			print(len(temp_list))
			for i in range(0,len(val)):
				if (i==0):
					robot_pic = temp_list[ val[i] ]
				temp_list.pop(val[i])
			
			print(len(temp_list))
			random_pics = random.sample(temp_list,3)
			random_pics.append(robot_pic)

			for item in random_pics:
				'''pos = [0,-1000]
				increment = [0,500]
				item.pos = pos
				pos = [pos[0]+increment[0],pos[1]+increment[1]]'''
				item.draw()

		# show all available robots
		else:
			for item in list:
				item.draw()

		# notify users to what the choice is
		if choice == 0:
			choice = '1st'
		elif choice == 1:
			choice = '2nd'
		elif choice == 2:
			choice = '3rd'

		message1 = visual.TextStim(self.win, 
		pos=[0,450],
		text="What robot best suits the voice: %s choice?" % choice,
		height=40, wrapWidth=1000, units='pix'
		)
		message1.draw()

	# check to see if robot was selected
	def checkRobot(self):
		while not event.getKeys(keyList=['e']):
			# returns [robot string, robot object, robot index, time taken for choice]
			if sum(self.mouse.getPressed()) and self.img_robo1.contains(self.mouse):
				return ["robot_1", self.img_robo1, 0, self.clock.getTime()]
			elif sum(self.mouse.getPressed()) and self.img_robo2.contains(self.mouse):
				return ["robot_2", self.img_robo2, 1, self.clock.getTime()]
			elif sum(self.mouse.getPressed()) and self.img_robo3.contains(self.mouse):
				return ["robot_3", self.img_robo3, 2, self.clock.getTime()]
			elif sum(self.mouse.getPressed()) and self.img_robo4.contains(self.mouse):
				return ["robot_4", self.img_robo4, 3, self.clock.getTime()]
			elif sum(self.mouse.getPressed()) and self.img_robo5.contains(self.mouse):
				return ["robot_5", self.img_robo5, 4, self.clock.getTime()]
			elif sum(self.mouse.getPressed()) and self.img_robo6.contains(self.mouse):
				return ["robot_6", self.img_robo6, 5, self.clock.getTime()]
			elif sum(self.mouse.getPressed()) and self.img_robo7.contains(self.mouse):
				return ["robot_7", self.img_robo7, 6, self.clock.getTime()]
			elif sum(self.mouse.getPressed()) and self.img_robo8.contains(self.mouse):
				return ["robot_8", self.img_robo8, 7, self.clock.getTime()]
			elif sum(self.mouse.getPressed()) and self.button.contains(self.mouse):
				return ["button", self.button, 8, self.clock.getTime()]

	# prompts user with likert scale evaluation
	def getRating(self, robot_img=0, img_width=768/2.5,img_height=950/2.5):
		scales = '1=Extremely Suitable, 9=Extremely Unsuitable'
		label = ['1','2','3','4','5']
		item = visual.TextStim(self.win, 
		    pos=[300,450],
		    text="How suitable do you think the voice is for the robot?",
		    height=40, wrapWidth=1000, units='pix'
		    )
		img_robot = visual.ImageStim(self.win,ori=0, size=(img_width,img_height), units='pix',
		    image=robot_img,    
		    pos=(-400, 0)
		    )
		ratingScale = visual.RatingScale(self.win, low=1, high=5, pos=(300,0), size=1, textSize = 0.7, showAccept=True, acceptPreText="click point on scale", acceptSize=1.25, labels = label)
		# prompt for user to input rating
		while ratingScale.noResponse:
			item.draw()
			img_robot.draw()
			ratingScale.draw()
			self.win.flip()
		print('rating was %i' % ratingScale.getRating() )
		return ratingScale.getRating()

	# function to orchestrate playing of voices
	# testID refers to what test is being run 
	# num_iter refers to how many clips to be played
	def playVoices(self, soundfiles, soundID, testID = 1, num_iter = 3):			
		voiceOrder = []
		for i in range(0,num_iter):
			# for random sampling 
			if testID ==1:
				## todo modify so doesnt choose same voice twice
				voice = random.choice(soundfiles)
				voiceOrder.append(voice)
				self.speak(voice)
				core.wait(0.5)

			# for staged scenario
			elif testID ==2:
				print('fuck')
				voice = soundfiles[i]
				voiceOrder.append(voice)
				self.speak(voice)
				# switch to different splash screen
				if i == 0:
					self.splashScreen("Oh, hi there")
				elif i == 1: 
					self.splashScreen("Ok, thanks for letting me know.")
				elif i == 2:
					self.splashScreen("Sure thing. Take your time.")

		# return the order voices were played - needed for replaying 
		return voiceOrder

	# create splash screen that requires buttonpress to advance
	def splashScreen(self, txtstring):
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

	# redraws robots with opacity changed and selection number shown
	# index refers to robot that was selected
	# iter refers to order robot was selected
	def updateScreen(self, index, iter):
		self.robot_list[index].opacity = 0.5
		pos = self.robot_list[index].pos
		item = visual.TextStim(self.win, pos=pos, text=iter+1, height=60, wrapWidth=1500, units='pix')
		return item

	'''def test1a(self, voicefile):
		# play voices
		[voicelist, voiceNames] = self.loadVoices(voicefile)
		[voicelist, voiceNames] = self.randomiseVoices(voicelist, voiceNames )
		tempResponse = []
		for voice in range(0,len(voiceNames)):
			robot_list = self.updateRobotList()
			voiceOrder = self.playVoices(voicelist[voice], voiceNames[voice])

			# show images
			num_pick = 0
			tempResponse = [self.ID, voiceNames[voice]] 
			while  num_pick < 3: 
				self.selectRobot(num_pick,self.robot_list)
				self.win.flip()
				self.clock.reset()
				[name, clicked, index, timer] = self.checkRobot()
				print("time taken was %f seconds" % timer)

				# todo save details of choice
				if name != "button":
					#rating = self.getRating(self.expInfo[name])
					rating = 10
					self.robot_list.remove(clicked)
					num_pick +=1
				else:
					rating = 0
					for i in range (0,len(voiceOrder)):
						print(voiceOrder[i])
						self.speak(voiceOrder[i])
						core.wait(0.5) 
				tempResponse.append(name)
				tempResponse.append(str(timer))
				tempResponse.append(str(rating))
				core.wait(0.2)
			tempResponse = ','.join(tempResponse)
			self.saveData(tempResponse+'\n')
			print(tempResponse)'''

	def test1b(self, voicefile):
		# import and randomise order of voices
		[voicelist, voiceNames] = self.loadVoices(voicefile)
		[voicelist, voiceNames] = self.randomiseVoices(voicelist, voiceNames )
		tempResponse = [] # initialise data to be logged

		# loop to iterate through each voice profile
		for voice in range(0,len(voiceNames)):
			repeat = True
			while repeat is True:
				# refresh list of robots
				robot_list = self.updateRobotList()
				# play voice files corresponding to voice profile
				voiceOrder = self.playVoices(voicelist[voice], voiceNames[voice])

				counter = 0 # initialise loop for selecting top three robots
				num_picks = 3
				tempResponse = [self.ID, voiceNames[voice]]  # update log
				pick = [] # initialise list for storing robots chosen
				while  counter < num_picks: 
					# show images of robots
					self.selectRobot(counter,self.robot_list)
					# refresh screen and timer 
					self.win.flip()
					self.clock.reset()
					# get robot choice
					[name, clicked, index, timer]  = self.checkRobot()
					print("time taken was %f seconds" % timer)

					# todo save details of choice
					if name != "button":
						# get rating on Likert scale
						#rating = self.getRating(self.expInfo[name])
						rating = 10
						# remove selected robot from list
						# self.robot_list.remove(clicked)
						# update screen with to reflect selection
						pick.append(self.updateScreen(index,counter))
						for item in pick:
							item.draw()
						counter +=1
					else:
						# go back to start of voice
						print("breakTrigger called")
						break

						'''rating = 0
						for i in range (0,len(voiceOrder)):
							print(voiceOrder[i])
							self.speak(voiceOrder[i])
							core.wait(0.5) '''
					tempResponse.append(name)
					tempResponse.append(str(timer))
					tempResponse.append(str(rating))
					core.wait(0.2)

					if counter == num_picks:
						self.selectRobot(counter,self.robot_list)
						# refresh screen and timer 
						self.win.flip()
						repeat = False
						## todo write function to get Likert for each category
						while not event.getKeys(keyList=['e']):
							i = 5

				# print data to file
				tempResponse = ','.join(tempResponse)
				self.saveData(tempResponse+'\n')
				print(tempResponse)

'''
	def test2(self, voicefile):
		# import and randomise order of voices
		[voicelist, voiceNames] = self.loadVoices(voicefile)
		#[voicelist, voiceNames] = self.randomiseVoices(voicelist, voiceNames )

		# loop to iterate through each voice profile
		for voice in range(0,len(voiceNames)):
			# refresh list of robots
			robot_list = self.updateRobotList()
			# play voice files corresponding to voice profile
			voiceOrder = self.playVoices(voicelist[voice], voiceNames[voice], testID=2)
			
			
			tempResponse = [self.ID, voiceNames[voice]] # initialise data to be logged
			num_pick = 0 # initialise loop for selecting top three robots
			while  num_pick < 3:  
				# call function to select robot
				self.selectRobot(num_pick, self.robot_list, index = voiceNames[voice], filter=True)
				# log data 
				self.win.flip()
				self.clock.reset()
				[name, clicked, timer] = self.checkRobot()
				print("time taken was %f seconds" % timer)
				num_pick += 1
			# todo. add new screen where user confirms choice by pressing enter
'''

if __name__ == "__main__":    #event.waitKeys()

	# test #1
	ex1 = robotVoiceEval(guiID=False, display=True, shorten=True)
	ex1.test1b('sounds_t3.csv')

	#ex1.test2('sounds_t4.csv')

	# test #2
