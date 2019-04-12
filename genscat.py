import sys
sys.dont_write_bytecode = True
import numpy as np
import matplotlib.pyplot as plt

class Scat:
    def __init__(self):
        self.legend = None
        self.fnames = []
        self.xmin = float('inf')
        self.xmax = -1.0
        self.ymin = float('inf')
        self.ymax = -1.0
        self.xlabel = 'Frame Number'
        self.ylabel = 'Latency (in msec)'

    def load(self, fname):
        data = []
        with open(fname) as f:
            lines = f.readlines()
            for c in lines:
                c = c.strip()
                if '/*' in c or '#' in c:
                    if 'legend' in c:
                        legend = c.split(':')[1]
                        if '*/' in legend:
                            legend = legend.replace('*/', '')
                        self.legend = legend.strip()
                    continue
                c = float(c)
                # c *= 1000.0
                data.append(c)

        self.data = data
        self.tss = [x for x in range(len(data))]
        return self.tss, self.data

    def draw(self, xs, ys, label, ax=None):
        if self.legend:
            label = self.legend
        if ax is None:
            plt.scatter(self.tss, self.data, label=label)
        else:
            plt.scatter(self.tss, self.data, label=label)

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


