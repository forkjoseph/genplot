import sys
sys.dont_write_bytecode = True
import os
import numpy as np
import matplotlib.pyplot as plt

class CDF:
    def __init__(self, debug=False):
        self.debug = debug
        self.legend = None
        self.fnames = []
        self.fname = None
        self.xmin = float('inf')
        self.xmax = -1.0
        self.ymin = 0.0
        self.ymax = 1.0
        self.xlabel = 'Latency (in msec)'
        self.ylabel = 'CDF'

    def load(self, fname):
        data = []
        withxaxis = False
        self.fname = os.path.basename(fname)
        with open(fname) as f:
            lines = f.readlines()
            for c in lines:
                c = c.strip()
                if '/*' in c or '#' in c:
                    if 'legend' in c.lower():
                        legend = c.split(':')[1]
                        if '*/' in legend:
                            legend = legend.replace('*/', '')
                        self.legend = legend.strip()
                        if self.debug is True:
                            print '[DEBUG] setting legend in parse', self.legend
                    continue
                try:
                    c = float(c)
                except ValueError as e:
                    tmp = c.split(' ')
                    if len(tmp) == 2:
                        idx = tmp[0]
                        c = float(tmp[1])
                        # c /= 1000.0
                    else:
                        raise e
                    # print e, c
                # c *= 1000.0
                data.append(c)

        self.data = data
        self.sorted_data = np.sort(self.data)
        self.yvals = np.arange(len(self.sorted_data))/float(len(self.sorted_data)-1)
        return self.sorted_data, self.yvals 

    def draw(self, xs, ys, label=None, ax=None):
        if label == self.fname:
            if self.legend is not None:
                label = self.legend
            else:
                label = self.fname
        else:
            label = label

        if self.debug is True:
            print '[DEBUG]', label, self.fname
        if ax is None:
            plt.plot(xs, ys, label=label)
        else:
            ax.plot(xs, ys, label=label, linewidth='2')
        return

        
    ''' returns 95, 99, 99.9 by default '''
    def tail(self):
        lastx = None
        th999 = False
        th99  = False
        th95  = False
        ys = reversed(self.yvals)
        xs = list(reversed(self.sorted_data))
        tails = {}
        for idx, y in enumerate(ys):
            if th999 is False:
                if y < 0.999:
                    tails['99.9'] = lastx
                    th999 = True
            elif th99 is False:
                if y < 0.99:
                    tails['99.0'] = lastx
                    th99 = True
            elif th95 is False:
                if y < 0.95:
                    tails['95.0'] = lastx
                    th95 = True
                    break
            lastx = xs[idx]
        return str(tails)

    def stats(self):
        xmin, xmax = np.nanmin(self.data), np.nanmax(self.data)
        median = np.nanmedian(self.data)
        # mean = np.nanmean(self.data)
        # return str({'min': xmin, 'max': xmax,
        #         'median': median, 'mean': mean})
        return str({'min': xmin, 'max': xmax,
                'median': median, })
