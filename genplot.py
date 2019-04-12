#!/usr/bin/env python2.7
""" simple multiple ploting tool with one script """
import sys, os
sys.dont_write_bytecode = True
import argparse
import matplotlib.pyplot as plt
import numpy as np
from genline import Line
from gencdf import CDF
from genscat import Scat
from genbar import Bar

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('datafiles', nargs='*')
parser.add_argument('--basedir', dest='basedir', type=str)
parser.add_argument('--baseiter', dest='baseiter', type=str)
parser.add_argument('--mode', dest='mode', type=str, required=True, \
        choices=['scat', 'bar', 'histo', 'line', 'cdf'])
parser.add_argument('--xmin', dest='xmin', type=float, default=None)
parser.add_argument('--xmax', dest='xmax', type=float)
parser.add_argument('--ymin', dest='ymin', type=float)
parser.add_argument('--ymax', dest='ymax', type=float)
parser.add_argument('--xtick', dest='xtick', type=float)
parser.add_argument('--xticks', dest='xticks', type=list)
parser.add_argument('--xlabel', dest='xlabel', type=str)
parser.add_argument('--ylabel', dest='ylabel', type=str)
parser.add_argument('-o', dest='outname', type=str)
parser.add_argument('--legends', dest='legends', type=str, nargs='+')
args = parser.parse_args()

def with_color(c, s):
    return "\x1b[%dm%s\x1b[0m" % (c, s)

if __name__ == '__main__':
    plotmode = args.mode.lower()
    xlim = (args.xmin, args.xmax)
    ylim = (args.ymin, args.ymax)

    if args.basedir and args.baseiter:
        print '[error] both args cannot be supported! (choose either)'
        sys.exit(-1)

    filenames = []
    if not args.basedir and not args.baseiter:
        filenames = args.datafiles
        lastslash = False
    elif not args.basedir and args.baseiter:
        # print 'baseiter', args.baseiter
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

    if args.legends is not None:
        legends = args.legends
        # legends = args.legends.split(',')
        # legends = [x.strip() for x in legends]
    else:
        legends = []

    print '== INFOS =='
    print '  datafiles:', filenames
    print '  plotmode:', plotmode 
    print '  limits: {}, {}'.format(xlim, ylim)
    print '  lables: x=\"{}\", y=\"{}\"'.format(args.xlabel, args.ylabel)
    print '  legends: {}'.format(legends)

    if plotmode == 'line':
        obj = Line()
    elif plotmode == 'cdf':
        obj = CDF()
    elif plotmode == 'scat' or plotmode == 'scatter':
        obj = Scat()
    elif plotmode == 'bar':
        obj = Bar()
    
    if args.xlabel is not None:
        obj.xlabel = args.xlabel
    if args.ylabel is not None:
        obj.ylabel = args.ylabel

    fig = plt.figure(figsize=(10, 4.75))
    ax = fig.add_subplot(111)
    ax.grid(which='major', axis='y', linestyle='--', linewidth='0.2')

    for idx, f in enumerate(filenames):
        xs, ys = obj.load(f)
        from os.path import basename
        bname = basename(f)
        label = bname

        # print f, len(xs), len(ys)
        if plotmode == 'bar':
            obj.draw(f, label=bname, ax=ax)
            continue
        else:
            if len(legends) > idx:
                label = legends[idx]
            obj.draw(xs, ys, label=label, ax=ax)

        if args.xmin  == None and args.xmax == None:
            if xlim[0] == None and xlim[1] == None:
                xlim = (min(xs), max(xs))
            elif xlim[1] == None:
                xlim = (min(xlim[0], min(xs)), max(xs))
            elif xlim[0] == None:
                xlim = (min(xs), max(xlim[1], max(xs)))
            else:
                xlim = (min(xlim[0], min(xs)), max(xlim[1], max(xs)))
            print xlim
        elif xlim[1] == None:
            xlim = (xlim[0], max(xs))
        elif xlim[0] == None:
            xlim = (min(xs), xlim[1])

        if plotmode == 'cdf':
            print with_color(31, 'tails: ' + obj.tail())
            print with_color(31, 'tails: ' + obj.stats())

    if plotmode == 'cdf':
        if ylim[0] is None and ylim[1] is None:
            ylim = (0, 1.0)
        elif ylim[0] is not None and ylim[1] is None:
            ylim = (ylim[0], 1.0)
        elif ylim[0] is None and ylim[1] is not None:
            ylim = (0.0, ylim[1])

    # if plotmode == 'cdf': # xlim[0] == None:
    #     xlim = (0.0, xlim[1])
    print 'xlim', xlim
    print 'ylim', ylim
    plt.ylim(ylim[0], ylim[1])
    plt.xlim(xlim[0], xlim[1])

    # ticks
    # if plotmode == 'scat':
    #     plt.yticks(np.arange(ylim[0], ylim[1] + 0.05, 0.05))
    if plotmode == 'bar':
        ypos = np.arange(len(obj.legends))
        legends = obj.legends
        print legends
        plt.xticks(ypos, legends, rotation=45)
        plt.margins(0.05)
        plt.subplots_adjust(bottom=0.175)
    if plotmode == 'cdf':
        plt.legend(loc='lower right')
    elif plotmode == 'scat':
        plt.legend(loc='lower right')
        # plt.legend(loc='upper right')
    else:
        plt.legend(loc='best')

    plt.xlabel(obj.xlabel, fontsize=14)
    plt.ylabel(obj.ylabel, fontsize=14)

    if args.xtick is not None:
        xtick_interval = int(args.xtick)
        print 'gonna set xtick to', xtick_interval
        xticks = [x for x in range(0, int(xlim[1]) + xtick_interval, xtick_interval)]
        plt.xticks(xticks, fontsize=14)
    else:
        xticks = plt.gca().get_xticks()
        plt.xticks(xticks, fontsize=14)
    yticks = plt.gca().get_yticks()
    plt.yticks(yticks, fontsize=14)

    plt.legend(prop={'size':16})

    if args.outname:
        figname = args.outname
        if args.basedir is None:
            savename = args.outname
        else:
            if lastslash is True:
                savename = basedir + args.outname
            else:
                savename = basedir + '/' + args.outname

        suffix = '.pdf'
        if savename.endswith(suffix):
            savename = savename.replace(suffix, '')
        print '[INFO] saving to {}{}'.format(savename, suffix)

        plt.savefig(savename + suffix)
        from subprocess import call
        call(["pdfcrop", savename + suffix])
        call(["rm", "-f", savename + suffix])
        call(["mv", savename + "-crop.pdf", savename + suffix])
    plt.show()
