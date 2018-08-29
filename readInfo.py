#import modules
from psychopy import core, visual, gui, data, event, sound
from psychopy.tools.filetools import fromFile, toFile
import numpy, random
import pandas as pd # needed for reading csv files
import random 

a = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16]
del a[-1]
print(a[0:len(a)-1])