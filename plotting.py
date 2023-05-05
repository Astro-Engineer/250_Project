import matplotlib.pyplot as plt
import numpy as np

xpoints = np.array([0, 6])
ypoints = np.array([0, 250])

plt.plot(xpoints, ypoints)
plt.xlabel("X-Label")
plt.ylabel("Y-Label")
plt.title("Title")
plt.savefig("Sample")
plt.show()