''' generate multi-bar graph from data '''
import sys
sys.dont_write_bytecode = True
import numpy as np
import scipy.stats as ss
import matplotlib.pyplot as plt
from base import Base as base

class Bar(base):
    def __init__(self, debug=False, adjust=None):
        super(Bar, self).__init__(debug, adjust)
        self.gentype = 'Bar'
        self.xlabel = 'Bar'
        self.ylabel = 'Latency (in msec)'
        self.xmin = float('inf')
        self.xmax = -1.0
        self.ymin = 0.0
        self.ymax = 1.0
        self.confidence = 0.90

    def load(self, fname):
        return super(Bar, self).load(fname)
    def loadall(self, fnames):
        return super(Bar, self).loadall(fnames)

    def draw(self, xs, ys, opt, label=None, ax=None):
        if ax is None:
            plt.bar(xs, ys, yerr=opt, align='center', alpha=0.5,)
        else:
            ax.bar(xs, ys, yerr=opt, align='center', alpha=0.5,)
        return

    def drawall(self, labels=None, ax=None, limits=None, legends=[]):
        labels = []
        for obj in self.objs:
            xs, ys, opt = obj.xs, obj.ys, obj.opt
            if len(legends) == 0:
                label = obj.label
            else:
                if len(legends) >= obj.idx:
                    label = legends[obj.idx]
                else:
                    label = obj.label

            labels.append(label)
            self.draw(xs, ys, opt, ax=ax)

        ypos = np.arange(len(self.objs))
        legends = labels
        print '[INFO] legends', legends
        plt.xticks(ypos, legends, rotation=45)
        plt.margins(0.05)
        plt.subplots_adjust(bottom=0.175)
        plt.legend(prop={'size':16})

        plt.xlabel(self.xlabel, fontsize=14)
        plt.ylabel(self.ylabel, fontsize=14)

    def stat(self, fname):
        targets = ['dlen', 'low', 'high', 'dmin', 'dmax', 
                'avg', 'std', 'err']
        # print 'Sample size:', len(tup["data"])
        # print '[{:.3f} - {:.3f}]'.format(tup["low"], tup["high"])
        # print tup["dmin"], tup["dmax"]
        # print tup["avg"], tup["std"], tup["err"]
        return ''


