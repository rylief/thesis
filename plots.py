import numpy as np
from mpl_toolkits.axes_grid1 import make_axes_locatable
from matplotlib import pyplot as plt

plt.rcParams.update({'font.size': 18})

fig, axs = plt.subplots(1, 3, sharex=True, sharey=True)

plt.xlim(-1.1,1.1)
plt.ylim(-1.1,1.1)

axs[0].scatter(0, -1, s=128)
axs[0].set_title('rock position vs. velocity')
axs[0].set(xlabel='x', ylabel='v')
axs[0].grid()
axs[0].set_aspect('equal')

axs[1].scatter(-1, 0, s=128)
axs[1].set_title('rock position vs. velocity')
axs[1].set(xlabel='x', ylabel='v')
axs[1].grid()
axs[1].set_aspect('equal')

axs[2].scatter(0.5, -0.5, s=128)
axs[2].set_title('rock position vs. velocity')
axs[2].set(xlabel='x', ylabel='v')
axs[2].grid()
axs[2].set_aspect('equal')

plt.show()
