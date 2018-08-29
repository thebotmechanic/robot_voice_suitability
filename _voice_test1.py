#import modules
from psychopy import core, visual, gui, data, event, sound, logging
from psychopy.tools.filetools import fromFile, toFile
import numpy, random
import pandas as pd # needed for reading csv files
import random 
logging.console.setLevel(logging.WARNING)

class robotVoiceEval:
	def __init__(self, guiID=False, logging=True, display=False, shorten=True):
		# import parameters from previous studies
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

		self.soundLink = {
		 "stevie":[1],
		 "pr2":[2,4],
		 "pepper":[3],
		 "sciprr":[4,2],
		 "icub":[5,7],
		 "flash":[6],
		 "g5":[7,5],
		 "poli":[8]}

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

		self.shorten = shorten

		# setup clock and mouse events events
		self.clock = core.Clock()
		self.mouse = event.Mouse(visible=True,newPos=False,win=self.win)

	def getID(self):
		p1 = gui.Dlg()
		p1.addField("Subject ID:")    
		p1.show()
		return p1.data[0]

	def openLogFile(self):
		fileName = self.expInfo['dateStr'] + self.expInfo['dateStr']
		self.dataFile = open('data/'+fileName+'.csv', 'w')  
		self.dataFile.write('ID, voice, choice1, t1, s1, choice2, t2, s2, choice3, t3, s3 \n') # todo ID, suitability


	def saveData(self,data):
		self.dataFile.write(data) # todo ID, suitability

	def loadVoices(self, voicefile):
			voices = pd.read_csv(voicefile) #
			robots = list(voices)
			# for actual 
			testing_list = []
			for i in range(0,len(robots)):
				testing_list.append(voices[robots[i]].tolist())

			testing_list2 = []
			robots2 = robots
			if (self.shorten is True):
				del robots2[2:5]

			for i in range(0,len(robots2)):
				testing_list2.append(voices[robots2[i]].tolist())

			return [testing_list2, robots2]

	def randomiseVoices(self, soundfiles, soundID):
		# create ranodm order
		shuffle = random.sample(range(0, len(soundID)), len(soundID))
		# sort files and fileIDs according to order
		soundfiles = [ soundfiles[i] for i in shuffle]
		soundID = [ soundID[i] for i in shuffle]
		return [soundfiles, soundID]

	def speak(self,voice_clip):
		voice = sound.Sound(voice_clip)
		waitTime = voice.getDuration()
		listenText = visual.TextStim(self.win,pos=[0,450],text="Listen to the sound",height=40,wrapWidth=1000,units='pix')
		fixation = visual.GratingStim(self.win, color=-1, colorSpace='rgb',
		                          tex=None, mask='cross', size=10)
		listenText.draw()
		fixation.draw()
		self.win.flip()
		voice.play()
		core.wait(waitTime)
		
	def updateRobotList(self, test=1, img_width=768/2.5,img_height=950/2.5):
		# import robots that will be used for the study
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

		if test==1:
			top_spacing = 160
			bottom_spacing = 285
			buffer = 50
			offset = -200
			spacing = img_width + buffer
			#set way
			self.img_robo1.pos=((buffer/2 + img_width/2) + offset, top_spacing)
			self.img_robo2.pos=((buffer/2 + img_width/2) + offset, -bottom_spacing)
			self.img_robo3.pos=((buffer/2 + img_width/2) + spacing+offset, top_spacing)
			self.img_robo4.pos=((buffer/2 + img_width/2) + spacing+offset, -bottom_spacing)
			self.img_robo5.pos=(-(buffer/2 + img_width/2) + offset, top_spacing)
			self.img_robo6.pos=(-(buffer/2 + img_width/2) + offset, -bottom_spacing)
			self.img_robo7.pos=(-(buffer/2 + img_width/2) - spacing+offset, top_spacing)
			self.img_robo8.pos=(-(buffer/2 + img_width/2) - spacing+offset, -bottom_spacing)
			self.button.pos=(700, 0)

		elif test ==2:
			#set way 
			print("test 2")
		elif test==3:
			#set way
			print("test 2")

	def selectRobot(self, choice, list, index = "dummy", ignore=None, filter=False):   

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
				item.draw()
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

		message1 = visual.TextStim(self.win, 
		pos=[0,450],
		text="What robot best suits the voice: %s choice?" % choice,
		height=40, wrapWidth=1000, units='pix'
		)
		message1.draw()

	def checkRobot(self):
		while not event.getKeys(keyList=['e']):
			if sum(self.mouse.getPressed()) and self.img_robo1.contains(self.mouse):
				return ["robot_1", self.img_robo1, self.clock.getTime()]
			elif sum(self.mouse.getPressed()) and self.img_robo2.contains(self.mouse):
				return ["robot_2", self.img_robo2, self.clock.getTime()]
			elif sum(self.mouse.getPressed()) and self.img_robo3.contains(self.mouse):
				return ["robot_3", self.img_robo3, self.clock.getTime()]
			elif sum(self.mouse.getPressed()) and self.img_robo4.contains(self.mouse):
				return ["robot_4", self.img_robo4, self.clock.getTime()]
			elif sum(self.mouse.getPressed()) and self.img_robo5.contains(self.mouse):
				return ["robot_5", self.img_robo5, self.clock.getTime()]
			elif sum(self.mouse.getPressed()) and self.img_robo6.contains(self.mouse):
				return ["robot_6", self.img_robo6, self.clock.getTime()]
			elif sum(self.mouse.getPressed()) and self.img_robo7.contains(self.mouse):
				return ["robot_7", self.img_robo7, self.clock.getTime()]
			elif sum(self.mouse.getPressed()) and self.img_robo8.contains(self.mouse):
				return ["robot_8", self.img_robo8, self.clock.getTime()]
			elif sum(self.mouse.getPressed()) and self.button.contains(self.mouse):
				return ["button", self.button, self.clock.getTime()]

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
		while ratingScale.noResponse:
			item.draw()
			img_robot.draw()
			ratingScale.draw()
			self.win.flip()
		print('rating was %i' % ratingScale.getRating() )
		return ratingScale.getRating()

	def playVoices(self, soundfiles, soundID, testID = 1, num_iter = 3):			
		# first turn 
		# a) play 3 sound clips at random
		voiceOrder = []
		for i in range(0,num_iter):
			if testID ==1:
				voice = random.choice(soundfiles)
				voiceOrder.append(voice)
				self.speak(voice)
				core.wait(0.5)
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
		return voiceOrder

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


	def test1(self, voicefile):
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
				[name, clicked, timer] = self.checkRobot()
				print("time taken was %f seconds" % timer)

				# todo save details of choice
				if name != "button":
					rating = self.getRating(self.expInfo[name])
					#rating = 10
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
			print(tempResponse)

	def test2(self, voicefile):
		# play voices
		[voicelist, voiceNames] = self.loadVoices(voicefile)
		#[voicelist, voiceNames] = self.randomiseVoices(voicelist, voiceNames )

		for voice in range(0,len(voiceNames)):
			robot_list = self.updateRobotList()
			#voiceOrder = self.playVoices(voicelist[voice], voiceNames[voice], testID=2)
			
			# show images
			num_pick = 0
			tempResponse = [self.ID, voiceNames[voice]] 
			while  num_pick < 3: 
				self.selectRobot(num_pick, self.robot_list, index = voiceNames[voice], filter=True)
				self.win.flip()
				self.clock.reset()
				[name, clicked, timer] = self.checkRobot()
				print("time taken was %f seconds" % timer)
				num_pick += 1

if __name__ == "__main__":    #event.waitKeys()

	# test #1
	ex1 = robotVoiceEval(guiID=False, display=True, shorten=True)
	#ex1.test1('sounds_t3.csv')

	ex1.test2('sounds_t4.csv')

	# test #2

























































































