import sys, os
sys.dont_write_bytecode = True
import numpy as np
import matplotlib.pyplot as plt
from .base import Base as base

class Scat(base):
    def __init__(self, debug=False, adjust=None):
        super(Scat, self).__init__(debug, adjust)
        self.gentype = 'Scatter'
        self.xlabel = 'Frame Number'
        self.ylabel = 'Latency (in msec)'
        self.xmin = float('inf')
        self.xmax = -1.0
        self.ymin = float('inf')
        self.ymax = -1.0

    def load(self, fname):
        return super(Scat, self).load(fname)

    def loadall(self, fnames):
        return super(Scat, self).loadall(fnames)

    def draw(self, xs, ys, label, ax=None):
        if ax is None:
            plt.scatter(xs, ys, label=label)
        else:
            ax.scatter(xs, ys, label=label)
        return

    def drawall(self, labels=None, ax=None, limits=None, legends=[]):
        for obj in self.objs:
            xs, ys = obj.xs, obj.ys
            label = obj.label
            if len(legends) >= obj.idx:
                label = legends[obj.idx]
            self.draw(xs, ys, label=label, ax=ax)

        if limits is None:
            ''' x-axis --> len of data '''
            ''' y-axis --> min/max of data '''
            ylim = (float('inf'), float('-inf'))
            
            ''' update only xlim for CDF '''
            for obj in self.objs:
                ys = obj.ys
                ymin = min(ys)
                ymax = max(ys)
                if ymin < ylim[0]: 
                    ylim = (ymin, ylim[1])
                if ymax > ylim[1]: 
                    ylim = (ylim[0], ymax)
            ''' well... let's just set xlim=(0, own) '''
            # ylim = (0.0, ylim[1])
            print('[DEBUG] Y-axis limit %s' % (str(ylim)))
#         else:
#             xlim = limits[0]
#             ylim = limits[1]
#             if ylim[0] is None and ylim[1] is None:
#                 # reset
#                 ylim = (0.0, 1.0)
#             if xlim[0] is None:
#                 xlim = (0.0, xlim[1])

        # plt.xlim(xlim[0], xlim[1])
        print('[DEBUG] Y-axis limit %s' % (str(ylim)))
        if ax is not None:
            ax.set_ylim(ylim[0], ylim[1])
        else:
            plt.ylim(ylim[0], ylim[1])

        plt.legend(loc='best', prop={'size':16})
        plt.xlabel(self.xlabel, fontsize=14)
        plt.ylabel(self.ylabel, fontsize=14)

        ### TODO: why are ticks not updated after limit changes?
        ## x ticks -> 8 items
        ## y ticks -> 6 items
        xticks = plt.gca().get_xticks()
        plt.xticks(xticks, fontsize=14)
        print(xticks)
        yticks = plt.gca().get_yticks()
        plt.yticks(yticks, fontsize=14)
        print(yticks)



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


