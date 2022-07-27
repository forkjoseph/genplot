''' generate multi-bar graph from data '''
import sys
sys.dont_write_bytecode = True
import numpy as np
import scipy.stats as ss
import matplotlib.pyplot as plt
from .base import Base as base

class Bar(base):
    def __init__(self, debug=False, adjust=None, usemp=False, parsed=False):
        super(Bar, self).__init__(debug, adjust)
        self.gentype = 'Bar'
        self.xlabel = 'Bar'
        self.ylabel = 'Latency (in msec)'
        self.xmin = float('inf')
        self.xmax = -1.0
        self.ymin = 0.0
        self.ymax = 1.0
        self.confidence = 0.90
        self.skip_parsing = parsed
        self.data = []

    def load(self, fname, myidx=0):
        return super(Bar, self).load(fname, myidx)

    def loadall(self, fnames):
        if self.skip_parsing is False:
            return super(Bar, self).loadall(fnames)
        else:
            if self.debug is False:
                raise Exception ('NOT supported yet... :(')
            if len(fnames) > 1:
                raise Exception ('[ERROR] parsed datafile for bar graph must be in single file!')

            fname = fnames[0]
            f = open(fname)
            dcnt = 0
            for c in f.readlines():
                c = c.strip()
                ''' Note that legend in parsed data file for bar graph is
                    **x-axis's label** 
                '''
                if '/*' in c or '#' in c:
                    # if self.debug is True:
                    #     print ('[DEBUG] # detected for', fname, c)
                    if 'legend' in c.lower():
                        if self.debug is True:
                            print ('[DEBUG] legend detected!')
                        legend = c.split(':')[1]
                        if '*/' in legend:
                            legend = legend.replace('*/', '')
                        self.xlabel = legend
                        if self.debug is True:
                            print(('[DEBUG] setting legend in parse \"%s\"' %
                                    self.xlabel))
                    else:
                        legend = c.split('#')[1]
                        self.xlabel = legend
                        if self.debug is True:
                            print(('[DEBUG] setting legend in parse \"%s\"' %
                                    self.xlabel))
                    continue

                xlabel = None
                try:
                    c = float(c)
                except ValueError as e:
                    if len(c.split(' ')) == 2:
                        tmp = c.split(' ')
                        xlabel = tmp[0]
                        c = float(tmp[1])
                    elif len(c.split(',')) == 2:
                        tmp = c.split(',')
                        xlabel = tmp[0]
                        c = float(tmp[1])
                    else:
                        print(('\x1b[33m[WARNING] skipping string \"%s\"\x1b[0m' % (c)))
                        continue

                if self.adjust is not None:
                    tmp = self.adjust
                    tmp = str(c) + tmp
                    adjusted = eval(tmp)
                    c = float(adjusted)
                dcnt += 1
                if self.debug is True:
                    print(('[DEBUG] %d: %f' % (dcnt, c)))
                    super(Bar, self).load([c], dcnt, argv=xlabel)
            return 
            

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
        print('[INFO] legends', legends)
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


