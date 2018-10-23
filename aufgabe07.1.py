#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os.path
import _labShopLoader
import matplotlib.pyplot as plt
import numpy as np
import scipy.optimize as sy
from matplotlib.widgets import Button
import os
import scipy.optimize as opt

def to_local():
    ''' change to local workspace for runtime stuff '''
    os.chdir(os.path.dirname(os.path.realpath(__file__)))

# pylint: disable = C0103
if __name__ == '__main__':
    to_local()

    fig = plt.figure()
    ax = fig.add_subplot(111)



    OSCILLATORS = []
    START = 450
    STOP = 1280
    BUTTONINDEX = 0

    selectedarea = ax.axvspan(START, STOP, alpha=0.1, color='gray', label="Optimization Area")

    def on_click(event):
        ''' react to click and select oscillator or range of optimization '''
        global BUTTONINDEX, START, STOP
        if event.button == 3:
            BUTTONINDEX = 3
            _ndarray = selectedarea.get_xy()
            _thex = int(event.xdata)
            _ndarray[:, 0] = [_thex] * 5
            selectedarea.set_xy(_ndarray)
            # Frequenzbereichanfang berechnen

        plt.draw()

    def on_motion(event):
        global BUTTONINDEX, STOP
        if BUTTONINDEX != 3:
            return
        else:
            _ndarray = selectedarea.get_xy()
            _thex = int(event.xdata)
            _ndarray[2:4, 0] = [_thex] * 2
            selectedarea.set_xy(_ndarray)
            # Frequenzbereichende berechnen
            plt.draw()

    def on_release(_):
        global BUTTONINDEX
        if BUTTONINDEX == 3:
            BUTTONINDEX = 0

    # axbtn = plt.axes([0.85, 0.85, 0.1, 0.075])
    # optbtn = Button(axbtn, 'Optimize')

    fig.canvas.mpl_connect('button_press_event', on_click)
    fig.canvas.mpl_connect('motion_notify_event', on_motion)
    fig.canvas.mpl_connect('button_release_event', on_release)

    #plt.show()

    def errorFunction(args):
        omegaH=[]
        integratedValues = doubleIntegral(partition)
        for val in partition[:,1]:
            omegaH.append(hOmega(val,args[0],args[1],args[2])*10**6)
        return np.linalg.norm(omegaH-integratedValues*10**6)**2

    FILE = "Versuchsdaten_Example.txt"
    
    if not os.path.isfile(FILE):
        print("File \"%s\" not found" % FILE)
        quit()
    LSL = _labShopLoader.LabShopLoader()
    partition=LSL.load(FILE)

    popt = opt.minimize(errorFunction,[900,0.1,0.1],method="L-BFGS-B",bounds=((0.1,np.inf),(0.1,np.inf),(0.1,np.inf)),tol=0.1)
    print("popt Werte:", poptx.x)
    omegaH=[]
    for val in partition[:,1]:
        omegaH.append(hOmega(val,popt3.x[0],popt3.x[1],popt3.x[2])*10**6)

    axarr[0].plot(partition[:,1],omegaH, label = "OmegaH")
    plt.legend()
    plt.show()

    def hOmega(omega, omega0, gamma, m):
        return 1 / (m * np.sqrt( (omega0**2 - omega**2)**2  + 4*gamma**2*omega**2 ))

    def doubleIntegral(partition):
        integratedValues=[0,0]
        for entry in partition:
            if entry[0] > 2:
                val=entry[2]+entry[3]*1j
                x=val/(1j*(entry[1]*2*np.pi))
                integratedValues.append(x/(1j*entry[1]*2*np.pi))
        return np.array(integratedValues)

