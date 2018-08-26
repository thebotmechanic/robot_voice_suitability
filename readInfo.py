import pandas as pd
import random
voices = pd.read_csv('sounds_t3.csv')
voices2  = [voices.pepper, voices.pr2]
robots = list(voices)
voices['pr2'].tolist()
testing_list = []

order = random.sample(range(0, len(robots)), len(robots))


x = [1,2,3,4,5]
y = [11,22,33,44,55]
print(random.shuffle(x,y))
 