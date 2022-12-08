import os
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import sys
if sys.version_info[0] < 3:
    import Tkinter as tkinter
    import ttk
else:
    import tkinter
    from tkinter import ttk
import numpy as np
import numpy.typing as npt
import matplotlib as mpl
if os.environ.get('DISPLAY','') == '':
    backend = 'TkAgg'
    print('No default display, setting ' + backend + '.\n')
    mpl.use(backend)
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Slider
from scipy.stats import norm

# General plot parameters
mpl.rcParams['font.size'] = 18
mpl.rcParams['axes.linewidth'] = 2
mpl.rcParams['axes.spines.top'] = False
mpl.rcParams['axes.spines.right'] = False
mpl.rcParams['xtick.major.size'] = 10
mpl.rcParams['xtick.major.width'] = 2
mpl.rcParams['ytick.major.size'] = 10
mpl.rcParams['ytick.major.width'] = 2


def gaussian(x: npt.NDArray[np.float64], mu: float, sigma: float, mag: float) -> npt.NDArray[np.float64]:
    return mag * norm.pdf(x,mu,sigma)

def newFig():

    def H1(curve):
        H1locs = np.where(x > crit)
        return np.sum(curve[H1locs])/np.sum(curve)


    def H0(curve):
        H0locs = np.where(x <= crit)
        return np.sum(curve[H0locs])/np.sum(curve)

    def format(num):
        return str(np.float_(round(num *100, 2)))

    crit = 10
    mu1 = -10 
    sigma1 = 20
    mag1 = 0.5
    mu2 = 30
    sigma2 = 25 
    mag2 = 1

    fig = plt.figure(figsize=(6, 4))

    ax1 = fig.add_subplot(221) #curves
    ax1.set_axis_off()

    x = np.linspace(-100, 100, 200)
    y1 = gaussian(x, mu1, sigma1, mag1)
    y2 = gaussian(x, mu2, sigma2, mag2)
    max = np.amax(np.concatenate((y1,y2), axis=None))
    xc = crit * np.array([1, 1])
    yc = [0, max]

    ax1.plot(x, y1)
    ax1.plot(x, y2)
    ax1.plot(xc, yc)

    H1y1 = H1(y1)
    H1y2 = H1(y2)
    H0y1 = H0(y1)
    H0y2 = H0(y2)
    
    ax2 = fig.add_subplot(222) #stats
    ax2.set_axis_off()
    ax2.axis('tight')
    ax2.axis('off')
    tab = ax2.table(cellText= [[format(H1y1), format(H1y2)],[format(H0y1), format(H0y2)]])
    tab.auto_set_column_width([1,1])
    tab.auto_set_font_size(False)
    
    ax3 = fig.add_subplot(223) #controller
    ax3.set_axis_off()
    sl1 = ax3.inset_axes([0, .9, 1, .1],)
    slide1 = Slider(ax=sl1, label='H1', valmin=-100, valmax=100, valinit=1, facecolor='#cc7000')

    sl2 = ax3.inset_axes([0, .4, 1, .1],)
    slide2 = Slider(ax=sl2, label='H2', valmin=-100, valmax=100, valinit=1, facecolor='#cc5000')

    ax4 = fig.add_subplot(224) #ROC
    ax4.set_axis_off()
    ax4.plot(np.cumsum(y2), np.cumsum(y1))



    return fig

# Animation function
def animate(i):
    x = np.linspace(0, 1, 100)
    y = fermi(x, 0.5, T[i])
    f_d.set_data(x, y)
    f_d.set_color(colors(i))
    temp.set_text(str(int(T[i])) + ' K')
    temp.set_color(colors(i))

# Update values
def update(val):
    s1 = slide1.val
    s2 = slide2.val
    f_d.set_data(x, fermi(x, Ef, T))
    fig.canvas.draw_idle()


class App(tkinter.Tk):
    def __init__(self):
        super().__init__()
        # Create figure and add axes
        fig = newFig()
        fig.show()
        # Create animation
#        FuncAnimation(fig=fig, func=animate, frames=range(len(T)), interval=500, repeat=True)
        return

if __name__ == '__main__':
    app = App()
    app.mainloop()