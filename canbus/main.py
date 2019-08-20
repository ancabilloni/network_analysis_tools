#! /usr/bin/env python3

from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg

import sys
import collections
import random
import time
import math
import numpy as np
import can
import logging

class CanSignalPlotter():
    def __init__(self, x_range=100, rate=100, wanted_frame_id=None, size=(600,350)):
        # Data stuff
        self.WANTED_ID = wanted_frame_id
        self._bufsize = int(x_range)
        self.databuffer = collections.deque([0.0]*self._bufsize, self._bufsize)
        self.x = np.linspace(0, x_range, self._bufsize)
        self.y = np.zeros(self._bufsize, dtype=np.float)

        # PyQtGraph stuff

        self.app = QtGui.QApplication(sys.argv)
        self.app.aboutToQuit.connect(self.exitHandler)
        self.plt = pg.plot(title='CAN Bus Signal Plot')
        self.plt.resize(*size)
        self.plt.showGrid(x=True, y=True)
        self.plt.setLabel('left', 'Time', 's')
        self.plt.setLabel('bottom', 'Signals', '')
        self.plt.setYRange((1.0/rate)*0.9, (1.0/rate)*1.1, padding=0) # Set fixed range for y (allow +/- 10 %)
        self.curve = self.plt.plot(self.x, self.y, pen=(0,255,255))
        
        # Set up socketcan and QTimer
        bustype = 'socketcan'
        channel = 'can0'
        canbus_available = True
        try:
            self.bus = can.interface.Bus(channel=channel, bustype=bustype)
        except IOError:
             canbus_available = False

        if canbus_available:
            self.timer = QtCore.QTimer()
            self.timer.timeout.connect(self.spin)
            self.timer.start(1)
            self._t0 = time.time()
        else:
            logging.warning('NO CANBUS AVAILABLE. CHECK CONNECTION')

    def spin(self):
        """ QTimer spin through this to check on can message """
        can_msg = self.bus.recv()
        now = time.time()

        if can_msg is not None and self.check_frame(can_msg.arbitration_id):
            self.databuffer.append(round(now-self._t0, 4))
            # self.y[:-1] = self.y[1:] 
            # self.y[-1] = round(now-self._t0, 4)
            self._t0 = now
            self.y[:] = self.databuffer
            self.curve.setData(self.x, self.y)
            self.app.processEvents()

    def check_frame(self, can_id):
        """ Check for desired can id"""
        if self.WANTED_ID is None:
            return True
        elif can_id == self.WANTED_ID:
            return True
        return False

    def exitHandler(self):
        """ Clean up when app closes"""
        print("App close")

    def run(self):
        sys.exit(self.app.exec_())

if __name__ == '__main__':
    if len(sys.argv) > 2:
        _wanted_frame_id = int(sys.argv[1],0)
        _rate = float(sys.argv[2])
    elif len(sys.argv) > 1:
        _wanted_frame_id = int(sys.argv[1],0)
        _rate = 100
    else:
        _wanted_frame_id = None
        _rate = 100
        
    # Plot x range 500
    m = CanSignalPlotter(x_range=500, rate=_rate, wanted_frame_id = _wanted_frame_id)
    m.run()