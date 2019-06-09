import sys
sys.dont_write_bytecode = True
import os
from model import *
from util import with_color
import multiprocessing as mp
from threading import Thread

class Base(object):
    def __init__(self, debug=False, adjust=None, usemp=False):
        self.debug = debug
        self.adjust = adjust
        self.usemp = usemp
        self.labels = []
        self.fnames = []
        self.objs = []

    def load(self, fname, myidx, argv=None):
        gentype = self.gentype
        if self.usemp is False:
            idx = len(self.objs)
        else:
            idx = myidx

        # if self.debug is True:
        #     print '[DEBUG] %d. gentype %s' % (idx, gentype)
            # print self.__dict__

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
            obj = DataBar(idx, self.debug, self.adjust, argv)
            obj.skip_parsing = self.skip_parsing
        else:
            raise Exception('Unsupported gentype')

        if self.debug is True:
            print '[DEBUG] gentype %s loaded for %s' % \
                (gentype, fname)

        if self.usemp is False:
            self.fnames.append(fname)
        else:
            self.fnames[idx] = fname

        if argv is not None:
            xs, ys, opt = obj.load(fname, argv=argv)
        else:
            xs, ys, opt = obj.load(fname)

        if self.usemp is False:
            self.objs.append(obj)
        else:
            self.objs[idx] = obj
        if self.usemp is False:
            self.labels.append(obj.label)
        else:
            self.labels[idx] = obj.label
        return xs, ys, opt

    def loadall(self, fnames):
        if self.usemp is False:
            for idx, fname in enumerate(fnames):
                self.load(fname)
                if self.debug is True:
                    print ('[DEBUG] %s is loaded' % (fname))
        else:
            dlen = len(fnames)
            self.fnames = [None for x in range(dlen)]
            self.objs = [None for x in range(dlen)]
            self.labels = [None for x in range(dlen)]
            if self.debug is True:
                print '[DEBUG] fnames: %s' % (self.fnames)
                print '[DEBUG] objs: %s' % (self.objs)
                print '[DEBUG] labels: %s' % (self.labels)

            threads = []
            for idx, fname in enumerate(fnames):
                t = Thread(target=self.load, args=(fname, idx,))
                threads.append(t)
                t.start()

            if self.debug is True:
                print '[DEBUG] waiting for parsers to be done...'
            for t in threads:
                t.join()
        return


