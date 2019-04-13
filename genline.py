''' generate line plot from data '''
import sys
sys.dont_write_bytecode = True
import numpy as np
import matplotlib.pyplot as plt

class Line:
    def __init__(self, debug=False):
        self.debug = debug
        self.legend = None
        self.xlabel = 'Frame Number'
        self.ylabel = 'Latency (in msec)'

    def load(self, fname):
        data = []
        with open(fname) as f:
            lines = f.readlines()
            for c in lines:
                c = c.strip()
                # if '/*' in c or '#' in c:
                if '/*' in c:
                    continue
                if '#' in c:
                    if 'legend' in c:
                        legend = c.split(':')[1]
                        self.legend = legend.strip()
                    continue
                c = float(c)
                data.append(c)
        tss = [x for x in range(len(data))]
        """ filtering for -1 """
        data = [x if x >= 0 else float('inf') for x in data]
        return tss, data

    def draw(self, xs, ys, label, ax=None):
        if self.legend:
            label = self.legend
        if ax is None:
            plt.plot(xs, ys, label=label)
        else:
            ax.plot(xs, ys, label=label, linewidth='2')

if __name__ == '__main__':
    ymin, ymax = 0, int(max([x if x != float('inf') else 0 for x in data]))
    # figname = None
    # if len(sys.argv) > 2:
    #     if len(sys.argv) == 3:
    #         figname = sys.argv[2]
    #         try:
    #             isint = int(figname)
    #             help()
    #         except ValueError:
    #             pass
    #     elif len(sys.argv) == 4:
    #         xmin = int(sys.argv[2])
    #         xmax = int(sys.argv[3])
    #     elif len(sys.argv) == 5:
    #         xmin = int(sys.argv[2])
    #         xmax = int(sys.argv[3])
    #         figname = sys.argv[4]
    #         try:
    #             isint = int(figname)
    #             help()
    #         except ValueError:
    #             pass
    #     else:
    #         help()

    print 'Y-min:', ymin
    print 'Y-max:', ymax
    plt.xlabel("Time")
    plt.ylabel("Value")
        
    plt.plot(xs, data)
    # plt.xlim(xmin, xmax)
    plt.ylim(ymin, ymax)

    plt.show()

# print 'min:', xmin
# print 'max:', xmax
# if figname:
#     import os
#     savename = os.getcwd() + '/' + figname
#     print 'saving to', savename + '.pdf'

# plt.scatter(xs, data)
# plt.xlabel("Time")
# plt.ylabel("Value")
# if figname:
#     plt.savefig(savename + '.pdf')
#     from subprocess import call
#     call(["pdfcrop", savename + '.pdf'])
#     call(["rm", "-f", savename + '.pdf'])
#     call(["mv", savename + "-crop.pdf", savename + ".pdf"])
# plt.show()

# for x, y in zip(xs, data):
#     if y <= 300:
#         print x,y
