from utils import *
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter, find_peaks


start = 1649486900
# start = 0

chart_data = read_chart_data()
only_total = {int(t):v[0] for t,v in chart_data.items() if int(t) >= start}

xs = np.array(list(only_total.keys()))
ys = np.array(list(only_total.values()))

peaks, _ = find_peaks(ys, distance=6)
# xs = xs[peaks]
# ys = ys[peaks]

new = savgol_filter(ys[peaks], min(11, len(peaks)), 7)

plt.plot(xs, ys)
# plt.plot(xs[peaks], ys[peaks])
plt.plot(xs[peaks], new)
plt.show()