#import modules
from psychopy import core, visual, gui, data, event, sound
from psychopy.tools.filetools import fromFile, toFile
import numpy, random
import pandas as pd # needed for reading csv files
import random 

class Person:
  def __init__(self, name, age):
    self.name = name
    self.age = age

  def myfunc(self):
    print("Hello my name is " + self.name)

p1 = Person("John", 36)
p1.myfunc() 


te = gui.Dlg()

te.addField("Subject ID:")
te.addField("Condition Num:")

te.show()


print (te.data)