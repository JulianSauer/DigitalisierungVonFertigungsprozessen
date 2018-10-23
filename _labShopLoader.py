"""Utility module for working with measurement system's generated files"""

import numpy as np


class LabShopLoader:
    """ Class to Load LabShop Pulse Data """
    def __init__(self):
        self.data = np.empty([1, 1])
        self.column = []
        self.content = []
        self.offset = 5
        self.skippable = 0
        self.xaxis_size = 0
        self.meta = {}
        self.filename = ""

    def load(self, fname):
        """ Load File and initialize data """
        with open(fname) as file:
            # remove excess whitespaces and replace , with .
            self.content = [' '.join(x.split()).replace(",", ".") for x in file.read().split("\n")]
            self.skippable = self.find("Header Size")
            self.xaxis_size = self.find("X-Axis size")
            self.data = np.zeros((self.xaxis_size, 5))
            startline = self.skippable + self.offset
            endline = startline + self.xaxis_size
			
			# Zeilen selektieren
            for value in self.content[startline:endline]:
                array=value.split(" ")
                array.append(0)
                self.data[int(array[0])-1]= array
			# Daten auswerten
            return self.data

    def find(self, searchstring, returntype=int):
        """ Find specific entry in file """
        return returntype([w for w in self.content if w.startswith(searchstring)][0].split(":")[1])
