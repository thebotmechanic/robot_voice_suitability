import pandas as pd
import random
voices = pd.read_csv('sounds_t3.csv')
voices2  = [voices.pepper, voices.pr2]
robots = list(voices)
print(robots)

del robots[2:5]
print(robots)


 