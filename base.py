import sys
sys.dont_write_bytecode = True
import os
from model import *
import multiprocessing as mp
from multiprocessing import cpu_count, Pool
from multiprocessing import Process
from multiprocessing import Manager

class Base(object):
    def __init__(self, debug=False, adjust=None, usemp=False):
        self.debug = debug
        self.adjust = adjust
        self.usemp = usemp
        self.labels = []
        self.fnames = []
        self.objs = []

    def load(self, fname):
        gentype = self.gentype
        idx = len(self.objs)
        if self.debug is True:
            print '[DEBUG] %d. gentype %s' % (idx, gentype)

        if 'CDF' == gentype:
            obj = DataCDF(idx, self.debug, self.adjust)
        elif 'Line' == gentype:
            obj = DataLine(idx, self.debug, self.adjust)
        elif 'Scatter' == gentype:
            obj = DataScat(idx, self.debug, self.adjust)
        elif 'Histogram' == gentype:
            opt = 50 # bins 
            obj = DataHisto(idx, self.debug, self.adjust, opt)
        elif 'Bar' == gentype:
            opt = 0.90 # confidence
            obj = DataBar(idx, self.debug, self.adjust, opt)
        else:
            raise Exception('Unsupported gentype')

        if self.debug is True:
            print '[DEBUG] gentype %s loaded for %s' % \
                (gentype, fname)

        self.fnames.append(fname)
        xs, ys, opt = obj.load(fname)
        self.objs.append(obj)
        self.labels.append(obj.label)
        return xs, ys, opt

    def loadall(self, fnames):
        if self.usemp is False:
            for idx, fname in enumerate(fnames):
                self.load(fname)
                if self.debug is True:
                    print ('[DEBUG] %s is loaded' % (fname))
        else:
            print ('multi-thread is not supported yet...!')
        return

def with_color(c, s):
    return "\x1b[%dm%s\x1b[0m" % (c, s)
