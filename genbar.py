''' generate multi-bar graph from data '''
import sys
sys.dont_write_bytecode = True
import numpy as np
import scipy.stats as ss
import matplotlib.pyplot as plt

class Bar:
    def __init__(self, debug=False):
        self.debug = debug
        self.legends = []
        self.xmin = float('inf')
        self.xmax = -1.0
        self.ymin = 0.0
        self.ymax = 1.0
        self.xlabel = 'Bar'
        self.ylabel = 'Latency (in msec)'
        self.confidence = 0.90
        self.ftups = {}

    def load(self, fname):
        tup = {}
        data = []
        with open(fname) as f:
            lines = f.readlines()
            for c in lines:
                c = c.strip()
                if '/*' in c or '#' in c:
                    if 'legend' in c.lower():
                        legend = c.split(':')[1]
                        if '*/' in legend:
                            legend = legend.replace('*/', '')
                        tup['legend'] = legend.strip()
                    continue
                c = float(c)
                # c *= 1000.0
                data.append(c)

        tup["data"] = data
        tup["dlen"] = len(data)
        tup["avg"] = np.mean(data)
        tup["std"] = np.std(data)
        tup["err"] = ss.t.ppf(self.confidence, tup["avg"]) * tup["std"]

        tup["low"] = tup["avg"] - tup["err"]
        tup["high"] = tup["avg"] + tup["err"]
        tup["dmin"] = min(tup["data"])
        tup["dmax"] = max(tup["data"])

        tup['idx'] = len(self.ftups)
        self.ftups[fname] = tup
        self.legends.append(tup['legend'])

        return tup["avg"], tup["err"]

    def draw(self, fname, label): 
        tup = self.ftups[fname]
        if 'legend' in tup:
            label = tup['legend']
        print label, tup['avg']
        plt.bar(tup['idx'], tup['avg'], align='center', alpha=0.5,)
        # plt.bar(tup['idx'], tup['avg'], yerr=tup['err'], align='center', alpha=0.5,)
        return

    def stat(self, fname):
        targets = ['dlen', 'low', 'high', 'dmin', 'dmax', 
                'avg', 'std', 'err']
        # print 'Sample size:', len(tup["data"])
        # print '[{:.3f} - {:.3f}]'.format(tup["low"], tup["high"])
        # print tup["dmin"], tup["dmax"]
        # print tup["avg"], tup["std"], tup["err"]
        return ''


