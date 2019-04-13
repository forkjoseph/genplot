#!/usr/bin/env python
''' generate histogram from data '''
import matplotlib.pyplot as plt
import numpy as np
import sys

xlabel = "Latency in msec"
def help():
    print 'usage: genhisto.py FILENAME [xmin] [xmax] [figname]'
    sys.ext(-1)

def load(fname):
    data = []
    with open(fname) as f:
	lines = f.readlines()
	for c in lines:
	    c = c.strip()
            if '/*' in c or '#' in c:
                continue
	    c = float(c)
	    data.append(c)
    return data

fname = sys.argv[1]
data = load(fname)

xmin, xmax = 0, int(max(data))
figname = None
if len(sys.argv) > 2:
    if len(sys.argv) == 3:
        figname = sys.argv[2]
        try:
            isint = int(figname)
            help()
        except ValueError:
            pass
    elif len(sys.argv) == 4:
        xmin = int(sys.argv[2])
        xmax = int(sys.argv[3])
    elif len(sys.argv) == 5:
        xmin = int(sys.argv[2])
        xmax = int(sys.argv[3])
        figname = sys.argv[4]
    else:
        help()

print 'min:', xmin
print 'max:', xmax
if figname:
    import os
    savename = os.getcwd() + '/' + figname
    print 'saving to', savename + '.pdf'

plt.hist(data, bins=range(xmin, xmax, 50))
plt.xlabel(xlabel)
plt.ylabel("Frequency")
if figname:
    plt.savefig(savename + '.pdf')
    from subprocess import call
    call(["pdfcrop", savename + '.pdf'])
    call(["rm", "-f", savename + '.pdf'])
    call(["mv", savename + "-crop.pdf", savename + ".pdf"])

plt.show()
