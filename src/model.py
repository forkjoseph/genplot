import sys
sys.dont_write_bytecode = True
import os
import numpy as np
import scipy.stats as ss

class DataModel(object):
    def __init__(self, idx, debug=False, adjust=False):
        self.idx = idx
        self.data = []
        self.label = None
        self.legend = None
        self.fname = None
        self.adjust = adjust
        self.debug = debug
        # print ('IS DEBUG? ', self.debug)

    def parse(self, fname):
        self.fname = os.path.basename(fname)
        with open(fname) as f:
            idx = 0
            for c in f.readlines():
                c = c.strip()
                if '/*' in c or '#' in c:
                    # if self.debug is True:
                    #     print ('[DEBUG] # detected for', fname, c)
                    if 'legend' in c.lower():
                        if self.debug is True:
                            print ('[DEBUG] legend detected!')
                        legend = c.split(':')[1]
                        if '*/' in legend:
                            legend = legend.replace('*/', '')
                        self.label = legend.strip()
                        self.legend = legend.strip()
                        if self.debug is True:
                            print ('[DEBUG] setting legend in parse \"%s\"' % self.label)
                    else:
                        legend = c.split('#')[1]
                        self.label = legend.strip()
                        self.legend = legend.strip()

                        if self.debug is True:
                            print ('[DEBUG] setting legend in parse \"%s\"' % self.label)
                    continue

                try:
                    c = float(c)
                except ValueError as e:
                    if ':' in c:
                        ## assuming the data point is right handed
                        tmp = c.split(':')
                        if len(tmp) == 2:
                            lidx = tmp[0]
                            c = float(tmp[1])
                    else:
                        tmp = c.split(' ')
                        if len(tmp) == 2:
                            lidx = tmp[0]
                            c = float(tmp[1])
                        # else:
                        #     print '\x1b[33m[ERROR] can\'t parse %s\x1b[0m' % (c)
                        #     raise e
                        else:
                            tmp = c.split('\t')
                            if len(tmp) == 2:
                                lidx = tmp[0]
                                c = float(tmp[1])
                            else:
                                print ('\x1b[33m[WARNING] skipping string \"%s\" at line %d \x1b[0m' % (c, idx))
                                continue

                if self.adjust is not None:
                    tmp = self.adjust
                    tmp = str(c) + tmp
                    adjusted = eval(tmp)
                    c = float(adjusted)
                self.data.append(c)
		idx += 1
        return

class DataCDF(DataModel):
    def __init__(self, idx, debug=False, adjust=None):
        super(DataCDF, self).__init__(idx, debug, adjust)
        self.sorted_data = []
        self.yvals = []

    def load(self, fname, myidx=0):
        super(DataCDF, self).parse(fname)
        self.sorted_data = np.sort(self.data)
        self.yvals = np.arange(len(self.sorted_data))/float(len(self.sorted_data)-1)
        self.xs = self.sorted_data
        self.ys = self.yvals
        return self.xs, self.ys, None

        # xs = self.sorted_data
        # ys = self.yvals
        # label = self.label
        # ax.plot(xs, ys, label=label, linewidth='2')

class DataLine(DataModel):
    def __init__(self, idx, debug=False, adjust=None):
        super(DataLine, self).__init__(idx, debug, adjust)
        self.tss = []

    def load(self, fname, myidx=0):
        super(DataLine, self).parse(fname)
        self.tss = [x for x in range(len(self.data))]
        """ filtering for -1 """
        self.data = [x if x >= 0 else float('inf') for x in self.data]
        self.xs = self.tss
        self.ys = self.data
        return self.xs, self.ys, None

        # label = self.label
        # ax.plot(xs, ys, label=label, linewidth='2')

class DataScat(DataModel):
    def __init__(self, idx, debug=False, adjust=None):
        super(DataScat, self).__init__(idx, debug, adjust)
        self.tss = []

    def load(self, fname, myidx=0):
        super(DataScat, self).parse(fname)
        self.tss = [x for x in range(len(self.data))]
        self.xs = self.tss
        self.ys = self.data
        return self.xs, self.ys, None

        # label = self.label
        # plt.scatter(xs, ys, label=label)

class DataHisto(DataModel):
    def __init__(self, idx, debug=False, adjust=None, bins=50):
        super(DataHisto, self).__init__(idx, debug, adjust)
        self.bin = bins
        self.xmin = 0
        self.xmax = float('inf')
        self.bins = []

    def load(self, fname, myidx=0):
        super(DataHisto, self).parse(fname)
        self.xmin, self.xmax = min(self.data), max(self.data)
        self.bins = range(self.xmin, self.xmax, self.bin)
        self.xs = self.data
        self.ys = self.bins
        return self.xs, self.ys, None

class DataBar(DataModel):
    ### for bar, you must pass index
    def __init__(self, idx, debug=False, adjust=None, confidence=0.90):
        super(DataBar, self).__init__(idx, debug, adjust)
        self.confidence = confidence
        self.idx = idx
        self.avg = .0
        self.std = .0
        self.err = .0
        self.low = .0
        self.high = .0
        self.opt = .0

    def load(self, fname, myidx=0, argv=None):
        if self.skip_parsing is True:
            self.data = [fname] 
            if argv is not None:
                self.label = argv
                self.legend = argv
        else:
            super(DataBar, self).parse(fname)
        self.dlen = len(self.data)
        self.avg = np.mean(self.data)
        self.std = np.std(self.data)
        self.err = ss.t.ppf(self.confidence, self.avg) * self.std
        self.low = self.avg - self.err
        self.high = self.avg + self.err
        self.dmin, self.dmax = min(self.data), max(self.data)
        
        self.xs = self.idx
        self.ys = self.avg
        self.opt= self.err # [optional]
        return self.xs, self.ys, self.opt

        # plt.bar(xs, ys, yerr=yerr align='center', alpha=0.5,)
        ## label must be done **after** all data plot


if __name__ == '__main__':
    print 'test...'
    # obj = DataBar(0)
    obj = DataCDF()
    obj.load('samples/data1.dat')
    for k, v in obj.__dict__.iteritems():
        if k != 'data':
            print k,v 

