import time
import random
import pandas as pd

s = []
i = time.time()
while i < time.time() + 100:
    i += 1
    s.append([i, random.randint(0, 10), random.random()])
# print(s)
s.insert(0, [1649087655, 0, 0.0])
df = pd.DataFrame(s , columns = ["dt", "val1", "val2"])

df.dt = df.dt.astype("datetime64[s]")

print(df.head(10))

df = df.set_index("dt")