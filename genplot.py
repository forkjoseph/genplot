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

from src.util import *
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
parser.add_argument('-l', '--legends', dest='legends', type=str, nargs='+')
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

if __name__ == '__main__':
    plotmode = args.mode.lower()
    xlim = (args.xmin, args.xmax)
    ylim = (args.ymin, args.ymax)
    debug, usemp = args.debug, args.mp
    xlabel, ylabel = args.xlabel, args.ylabel
    outname = args.outname

    filenames = get_filenames(args)
    legends, adjust = get_others(args, filenames=filenames)

    print '=' * 32, 'INFOS', '=' * 33
    print '   plotmode:', plotmode 
    print '  datafiles:', filenames
    print '     limits: {}, {}'.format(xlim, ylim)
    print '     lables: x=\"{}\", y=\"{}\"'.format(xlabel, ylabel)
    print '    legends: {}'.format(legends)
    print '     adjust: %s' % (adjust)
    print '   out name: %s' % (outname)
    print '      debug: %s' % (debug)
    print '=' * 72

    if plotmode == 'line':
        obj = Line(debug, adjust, usemp)
    elif plotmode == 'cdf':
        obj = CDF(debug, adjust, usemp)
    elif plotmode == 'scat' or plotmode == 'scatter':
        obj = Scat(debug, adjust, usemp)
    elif plotmode == 'bar':
        is_parsed = args.parsed
        print PINFO + 'data is already parsed?', is_parsed
        obj = Bar(debug, adjust=adjust, usemp=usemp, parsed=is_parsed)
    
    if xlabel is not None:
        obj.xlabel = xlabel
    if ylabel is not None:
        obj.ylabel = ylabel

    fig = plt.figure(figsize=(10, 4.75))
    ax = fig.add_subplot(111)
    ax.grid(which='major', axis='y', linestyle='--', linewidth=0.2)

    # print '[INFO] file nemas:', filenames
    obj.loadall(filenames)

    # limits = (xlim, ylim)
    # if limits[0][0] is None and limits[0][1] is None and \
    #     limits[1][0] is None and limits[1][1] is None:
    #         limits = None
    #         if debug is True:
    #             print '[DEBUG] Limits are none...'

    obj.drawall(ax=ax, limits=(xlim, ylim), legends=legends)
    if plotmode == 'cdf':
        obj.stat()
    
    if args.outname:
        saveplot(plt, args)
    print PINFO + 'showing the graph ¯\\_(ツ)_/¯'
    try:
        plt.show()
    except Exception:
        print PERR + 'no display detected! Make sure to use --noshow option!'

