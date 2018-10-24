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


    # plt.show()

    def double_integral(data):
        integrated_values = []
        print(len(data))
        for entry in data:
            val = entry[2] + entry[3] * 1j
            x = val / (1j * (entry[1] * 2 * np.pi))
            integrated_values.append(x / (1j * entry[1] * 2 * np.pi))
        return np.array(integrated_values)


    def h_omega(omega, omega0, gamma, m):
        return 1 / (m * np.sqrt((omega0 ** 2 - omega ** 2) ** 2 + 4 * gamma ** 2 * omega ** 2))


    def error_function(x0, *args):
        omega_h = []
        data = args[0]
        integrated_values = double_integral(data)
        for val in data[:, 1]:
            omega_h.append(h_omega(val, x0[0], x0[1], x0[2]))
        return np.linalg.norm(omega_h - integrated_values) ** 2


    FILE = "Versuchsdaten_Example.txt"

    if not os.path.isfile(FILE):
        print("File \"%s\" not found" % FILE)
        quit()
    LSL = _labShopLoader.LabShopLoader()
    partition = LSL.load(FILE)

    popt = opt.minimize(error_function, x0=[900, 0.1, 0.1], args=(partition[100:1255, :]), method="L-BFGS-B",
                        bounds=((0.1, np.inf), (0.1, np.inf), (0.1, np.inf)), tol=0.1)
    print("popt Werte:", popt.x)
    omegaH = []
    for val in partition[:, 1]:
        omegaH.append(h_omega(val, popt.x[0], popt.x[1], popt.x[2]))

    _, axarr = plt.subplots(2, sharex=True)
    axarr[0].plot(partition[10:, 1], np.abs(double_integral(partition[10:, :])), label="2x integriertes Zeug")
    axarr[1].plot(partition[:, 1], omegaH, label="OmegaH")
    plt.legend()
    plt.show()
