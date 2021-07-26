import pandas as pd
import numpy as np
import math

df = pd.read_csv('./csv/final.csv')

N = len(df)
x = np.array(df['parallax'])
m = np.mean(x)
s = np.std(x)

e = 2 * s / math.sqrt(N)
print(m, s, e)