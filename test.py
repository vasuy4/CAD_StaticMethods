# Implementation of matplotlib function
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import TextBox


fig, ax = plt.subplots()#   w  w w .   d e  m    o 2 s    . c  o  m
plt.subplots_adjust(bottom = 0.2)
t = np.arange(-2.0, 2.0, 0.001)
s = np.sin(t)+np.cos(2 * t)
initial_text = "sin(t) + cos(2t)"
l, = plt.plot(t, s, lw = 2)

def submit(text):

    ydata = eval(text)
    l.set_ydata(ydata)
    ax.set_ylim(np.min(ydata), np.max(ydata))
    plt.draw()

axbox = plt.axes([0.4, 0.05, 0.3, 0.075])
text_box = TextBox(axbox, 'Formula Used : ',
                   initial = initial_text)

text_box.on_submit(submit)

fig.suptitle('matplotlib.pyplot.subplots_adjust() Example')
plt.show()