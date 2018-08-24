import pandas as pd
df = pd.read_csv('sounds.csv')
saved_column = df.task_1 #you can also use df['column_name']
print(saved_column)