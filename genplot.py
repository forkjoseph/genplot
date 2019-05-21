#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
""" simplest ploting tool for a paper! """
import sys
sys.dont_write_bytecode = True
import argparse
import matplotlib
# matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from os.path import basename
from src.base import *
from src.genline import Line
from src.gencdf import CDF
from src.genscat import Scat
from src.genbar import Bar

LIMITATION = "limitation: draws one graph PER run... :(\n" + \
        "Joseph suggests using a bash script to call this genplot " + \
        "in order to generate multiple graphs at once."

parser = argparse.ArgumentParser(description="Simplest plotting tool\n", 
        epilog=with_color(31, LIMITATION))
## mandatory arguments to plot the graph!!
parser.add_argument('datafiles', nargs='*', 
        help="data file to draw (ex. ./genplot.py -m cdf abc.dat)")
parser.add_argument('-m', '--mode', dest='mode', type=str, required=True,
        choices=['scat', 'bar', 'histo', 'line', 'cdf'],
        help="which plot mode to use")
## EITHER or !!!! 
parser.add_argument('--basedir', dest='basedir', type=str,
        help="base directory to iterate for data file")
parser.add_argument('--baseiter', dest='baseiter', type=str,
        help="base **iterator** mode (useful when feeding data w/ a format)")
## optional arguements 
parser.add_argument('--adjust', dest='adjust', type=str, default=None)
parser.add_argument('--xmin', dest='xmin', type=float, default=None)
parser.add_argument('--xmax', dest='xmax', type=float, default=None)
parser.add_argument('--ymin', dest='ymin', type=float, default=None)
parser.add_argument('--ymax', dest='ymax', type=float, default=None)
parser.add_argument('--xtick', dest='xtick', type=float,
        help="????????????????? TBD ~_~ ")
parser.add_argument('--xticks', dest='xticks', type=list)
parser.add_argument('--xlabel', dest='xlabel', type=str)
parser.add_argument('--ylabel', dest='ylabel', type=str)
parser.add_argument('--legends', dest='legends', type=str, nargs='+')
parser.add_argument('-o', '--output', dest='outname', type=str,
        help="PDF file name (ex. abc.pdf or /tmp/abc). Default is PDF format. " + 
        "For PNG output, make sure to pass FILENAME.png as arguement")
parser.add_argument('-M', '--mp', action='store_true',
        help="[EXP] Use multithreads to load data (helpful for big datasets)")
parser.add_argument('-P', '--parsed', action='store_true',
        help="[EXP] For bar graph, use parsed data")
parser.add_argument('-D', '--debug', action='store_true')
parser.add_argument('-V', '--verbose', action='store_true')
args = parser.parse_args()

def saveplot():
    figname = args.outname
    if args.basedir is None:
        savename = args.outname
    else:
        if lastslash is True:
            savename = basedir + args.outname
        else:
            savename = basedir + '/' + args.outname
    suffix = '.pdf'
    realsuffix = '.pdf'
    if savename.endswith('.png'):
        realsuffix = '.png'
        savename = savename.replace(realsuffix, '')
    elif savename.endswith(suffix):
        savename = savename.replace(realsuffix, '')
    
    import os
    dname = os.path.dirname(os.path.realpath(savename))
    bname = os.path.basename(savename)
    __tmp = dname + '/.tmp-' + bname + suffix
    __tmp2 = dname + '/.tmp2-' + bname + suffix
    print '[INFO] saving to {}{}'.format(savename, suffix)

    plt.savefig(__tmp)
    from subprocess import call
    call(["pdfcrop", __tmp, __tmp2])
    call(["rm", "-f", __tmp])
    if realsuffix == '.pdf':
        call(["cp", __tmp2, savename + suffix])

    if realsuffix == '.png':
        print '[INFO] converting to {}{}'.format(savename, realsuffix)
        call(["convert", "-density", "400", __tmp2, savename + realsuffix])
    call(["rm", "-f", __tmp2])
    print '[INFO] saved to {}{}'.format(savename, realsuffix)
    return

if __name__ == '__main__':
    plotmode = args.mode.lower()
    xlim = (args.xmin, args.xmax)
    ylim = (args.ymin, args.ymax)
    debug = args.debug

    if args.basedir and args.baseiter:
        print '[ERROR] both args cannot be supported! (choose either)'
        # parser.print_help()
        sys.exit(-1)

    filenames = []
    if not args.basedir and not args.baseiter:
        filenames = args.datafiles
        lastslash = False
    elif not args.basedir and args.baseiter:
        baseiter = args.baseiter
        for f in args.datafiles:
            filenames.append(baseiter.format(f))
    elif args.basedir and not args.baseiter:
        basedir = args.basedir
        if basedir[len(basedir) - 1] == '/':
            lastslash = True
        else:
            lastslash = False
        for f in args.datafiles:
            if lastslash is True:
                filenames.append(basedir + f)
            else:
                filenames.append(basedir + '/' + f)
    if len(filenames) < 1:
        print '[ERROR] you must provide data files to draw mannnnn!'
        sys.exit(-1)

    if args.legends is not None:
        legends = args.legends
    else:
        legends = []

    if args.adjust is not None:
        adjust = args.adjust
    else:
        adjust = None
    usemp = args.mp

    print '=' * 32, 'INFOS', '=' * 33
    print '  datafiles:', filenames
    print '  plotmode:', plotmode 
    print '  limits: {}, {}'.format(xlim, ylim)
    print '  lables: x=\"{}\", y=\"{}\"'.format(args.xlabel, args.ylabel)
    print '  legends: {}'.format(legends)
    print '  adjust: %s' % (adjust)
    print '=' * 70

    if plotmode == 'line':
        obj = Line(debug, adjust, usemp)
    elif plotmode == 'cdf':
        obj = CDF(debug, adjust, usemp)
    elif plotmode == 'scat' or plotmode == 'scatter':
        obj = Scat(debug, adjust, usemp)
    elif plotmode == 'bar':
        is_parsed = args.parsed
        print '[INFO] data is already parsed?', is_parsed
        obj = Bar(debug, adjust=adjust, usemp=usemp, parsed=is_parsed)
    
    if args.xlabel is not None:
        obj.xlabel = args.xlabel
    if args.ylabel is not None:
        obj.ylabel = args.ylabel

    fig = plt.figure(figsize=(10, 4.75))
    ax = fig.add_subplot(111)
    ax.grid(which='major', axis='y', linestyle='--', linewidth=0.2)

    print '[INFO] file nemas:', filenames
    obj.loadall(filenames)

    limits = (xlim, ylim)

    if limits[0][0] is None and limits[0][1] is None and \
        limits[1][0] is None and limits[1][1] is None:
            limits = None
            if debug is True:
                print '[DEBUG] Limits are none...'

    obj.drawall(ax=ax, limits=limits, legends=legends)

    if plotmode == 'cdf':
        obj.stat()
    
    if args.outname:
        saveplot()
    print '[INFO] showing the graph ¯\\_(ツ)_/¯'

    plt.show()
