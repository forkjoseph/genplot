import sys, os
sys.dont_write_bytecode = True
import numpy as np
import matplotlib.pyplot as plt
from base import Base as base

class Line(base):
    def __init__(self, debug=False, adjust=None, usemp=False):
        super(Line, self).__init__(debug, adjust)
        self.gentype = 'Line'
        self.xlabel = 'Frame Number'
        self.ylabel = 'Latency (in msec)'
        self.xmin = 0.0
        self.xmax = float('inf')
        self.ymin = 0.0
        self.ymax = float('inf')

    def load(self, fname, myidx=0):
        return super(Line, self).load(fname, myidx)

    def loadall(self, fnames):
        return super(Line, self).loadall(fnames)

    def draw(self, xs, ys, label, ax=None):
        if ax is None:
            plt.plot(xs, ys, label=label)
        else:
            ax.plot(xs, ys, label=label, linewidth='2')

    def drawall(self, labels=None, ax=None, limits=None, legends=[]):
        if self.debug:
            print '[DEBUG] labels:', labels
        for obj in self.objs:
            xs, ys = obj.xs, obj.ys

            if self.debug:
                print '[DEBUG] obj.label:', obj.label

            if labels is None and obj.label is None:
                label = obj.fname
            # elif labels is not None:
            else:
                label = obj.label

            # if len(legends) >= obj.idx:
            #     label = legends[obj.idx]
            self.draw(xs, ys, label=label, ax=ax)

        xlim, ylim = limits[0], limits[1]

        if limits[0] == None or limits[0][0] == None:
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
            print '[DEBUG] Y-axis limit %s' % (str(ylim))
#         else:
#             xlim = limits[0]
#             ylim = limits[1]
#             if ylim[0] is None and ylim[1] is None:
#                 # reset
#                 ylim = (0.0, 1.0)
#             if xlim[0] is None:
#                 xlim = (0.0, xlim[1])


        # print '[DEBUG] Y-axis limit %s' % (str(ylim))
        if ax is not None:
            ax.set_ylim(ylim[0], ylim[1])
            ax.set_xlim(xlim[0], xlim[1])
        else:
            plt.ylim(ylim[0], ylim[1])
            plt.xlim(xlim[0], xlim[1])

        plt.legend(loc='best', prop={'size':16})
        plt.xlabel(self.xlabel, fontsize=14)
        plt.ylabel(self.ylabel, fontsize=14)

        ### TODO: why are ticks not updated after limit changes?
        ## x ticks -> 8 items
        ## y ticks -> 6 items
        xticks = plt.gca().get_xticks()
        plt.xticks(xticks, fontsize=14)
        print xticks
        yticks = plt.gca().get_yticks()
        plt.yticks(yticks, fontsize=14)
        print yticks

