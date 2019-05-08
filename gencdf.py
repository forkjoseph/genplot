import sys, os
sys.dont_write_bytecode = True
import numpy as np
import matplotlib.pyplot as plt
from base import Base as base
from base import *

class CDF(base):
    def __init__(self, debug=False, adjust=None):
        super(CDF, self).__init__(debug, adjust)
        self.gentype = 'CDF'
        self.xlabel = 'Latency (in msec)'
        self.ylabel = 'CDF'
        self.xmin = float('inf')
        self.xmax = -1.0
        self.ymin = 0.0
        self.ymax = 1.0

    def load(self, fname):
        return super(CDF, self).load(fname)

    def loadall(self, fnames):
        return super(CDF, self).loadall(fnames)

    def draw(self, xs, ys, label=None, ax=None):
        if ax is None:
            plt.plot(xs, ys, label=label)
        else:
            ax.plot(xs, ys, label=label, linewidth=2.0)
        return

    def drawall(self, labels=None, ax=None, limits=None, legends=[]):
        for obj in self.objs:
            xs, ys = obj.xs, obj.ys
            label = obj.label
            if len(legends) > 0 and len(legends) >= obj.idx:
                label = legends[obj.idx]
            self.draw(xs, ys, label=label, ax=ax)

        if limits is None:
            xlim = (float('inf'), float('-inf'))
            ylim = (self.ymin, self.ymax)
            ''' update only xlim for CDF '''
            for obj in self.objs:
                xs = obj.xs
                xmin = min(xs)
                xmax = max(xs)
                if xmin < xlim[0]: 
                    xlim = (xmin, xlim[1])
                if xmax > xlim[1]: 
                    xlim = (xlim[0], xmax)
            ''' well... let's just set xlim=(0, own) '''
            xlim = (0.0, xlim[1])
            print xlim
        else:
            xlim = limits[0]
            ylim = limits[1]
            if ylim[0] is None and ylim[1] is None:
                # reset
                ylim = (0.0, 1.0)
            if xlim[0] is None:
                xlim = (0.0, xlim[1])

        plt.ylim(ylim[0], ylim[1])
        plt.xlim(xlim[0], xlim[1])
        plt.legend(loc='lower right')
        plt.legend(prop={'size':16})

        plt.xlabel(self.xlabel, fontsize=14)
        plt.ylabel(self.ylabel, fontsize=14)
        xticks = plt.gca().get_xticks()
        plt.xticks(xticks, fontsize=14)
        yticks = plt.gca().get_yticks()
        plt.yticks(yticks, fontsize=14)


    def stat(self):
        for obj in self.objs:
            print '[BONUS]', with_color(31, 'tails: ' + self.tail(obj))
            print '[BONUS]', with_color(31, 'tails: ' + self.stats(obj))
            
        
    ''' returns 95, 99, 99.9 by default '''
    def tail(self, obj):
        lastx = None
        th999 = False
        th99  = False
        th95  = False
        ys = reversed(obj.yvals)
        xs = list(reversed(obj.sorted_data))
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

    def stats(self, obj):
        xmin, xmax = np.nanmin(obj.data), np.nanmax(obj.data)
        median = np.nanmedian(obj.data)
        # mean = np.nanmean(self.data)
        # return str({'min': xmin, 'max': xmax,
        #         'median': median, 'mean': mean})
        return str({'min': xmin, 'max': xmax,
                'median': median, })
