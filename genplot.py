#!/usr/bin/env python2.7
""" simplest ploting tool for a paper! """
import sys
sys.dont_write_bytecode = True
import argparse
import matplotlib.pyplot as plt
import numpy as np
from os.path import basename
from base import *
from genline import Line
from gencdf import CDF
from genscat import Scat
from genbar import Bar

LIMITATION = "limitation: draws one graph PER run... :(\n" + \
        "Joseph suggests using a bash script to call this genplot " + \
        "in order to generate multiple graphs at once."

parser = argparse.ArgumentParser(description="Simplest plotting tool\n", 
        epilog=with_color(31, LIMITATION))
## mandatory arguments to plot the graph!!
parser.add_argument('datafiles', nargs='*', 
        help="data file to draw (ex. ./genplot.py -m cdf abc.dat)")
parser.add_argument('--mode', dest='mode', type=str, required=True,
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
parser.add_argument('-o', dest='outname', type=str,
        help="PDF file name (ex. abc.pdf or /tmp/abc)")
parser.add_argument('--debug', dest='debug', type=bool, default=False)
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
    if savename.endswith(suffix):
        savename = savename.replace(suffix, '')
    print '[INFO] saving to {}{}'.format(savename, suffix)

    plt.savefig(savename + suffix)
    from subprocess import call
    call(["pdfcrop", savename + suffix])
    call(["rm", "-f", savename + suffix])
    call(["mv", savename + "-crop.pdf", savename + suffix])



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

    print '=' * 32, 'INFOS', '=' * 33
    print '  datafiles:', filenames
    print '  plotmode:', plotmode 
    print '  limits: {}, {}'.format(xlim, ylim)
    print '  lables: x=\"{}\", y=\"{}\"'.format(args.xlabel, args.ylabel)
    print '  legends: {}'.format(legends)
    print '  adjust: %s' % (adjust)
    print '=' * 70

    if plotmode == 'line':
        obj = Line(debug, adjust)
    elif plotmode == 'cdf':
        obj = CDF(debug, adjust)
    elif plotmode == 'scat' or plotmode == 'scatter':
        obj = Scat(debug, adjust)
    elif plotmode == 'bar':
        obj = Bar(debug, adjust)
    
    if args.xlabel is not None:
        obj.xlabel = args.xlabel
    if args.ylabel is not None:
        obj.ylabel = args.ylabel

    fig = plt.figure(figsize=(10, 4.75))
    ax = fig.add_subplot(111)
    ax.grid(which='major', axis='y', linestyle='--', linewidth='0.2')

    print filenames
    obj.loadall(filenames)

    limits = (xlim, ylim)

    if limits[0][0] is None and limits[0][1] is None and \
        limits[1][0] is None and limits[1][1] is None:
            print 'Limits are none...'
            limits = None
    obj.drawall(ax=ax, limits=limits, legends=legends)

    if plotmode == 'cdf':
        obj.stat()



    # for idx, f in enumerate(filenames):
    #     xs, ys, opt = obj.load(f)

    #     if len(legends) > idx:
    #         label = legends[idx]
    #         if args.debug is True:
    #             print '[DEBUG] label for', idx, label
    #     else:
    #         label = basename(f)
    #         if args.debug is True:
    #             print '[DEBUG] using filename as label for', label

    #     if plotmode == 'bar':
    #         obj.draw(f, label=label, ax=ax)
    #         continue
    #     else:
    #         obj.draw(xs, ys, label=label, ax=ax)

    #     if args.xmin  == None and args.xmax == None:
    #         if xlim[0] == None and xlim[1] == None:
    #             xlim = (min(xs), max(xs))
    #         elif xlim[1] == None:
    #             xlim = (min(xlim[0], min(xs)), max(xs))
    #         elif xlim[0] == None:
    #             xlim = (min(xs), max(xlim[1], max(xs)))
    #         else:
    #             xlim = (min(xlim[0], min(xs)), max(xlim[1], max(xs)))

    #         if args.debug is True:
    #             print '[DEBUG]', xlim

    #     elif xlim[1] == None:
    #         xlim = (xlim[0], max(xs))
    #     elif xlim[0] == None:
    #         xlim = (min(xs), xlim[1])

    #     # if plotmode == 'cdf':
    #     #     print '[BONUS]', with_color(31, 'tails: ' + obj.tail())
    #     #     print '[BONUS]', with_color(31, 'tails: ' + obj.stats())

    # if plotmode == 'cdf':
    #     if ylim[0] is None and ylim[1] is None:
    #         ylim = (0, 1.0)
    #     elif ylim[0] is not None and ylim[1] is None:
    #         ylim = (ylim[0], 1.0)
    #     elif ylim[0] is None and ylim[1] is not None:
    #         ylim = (0.0, ylim[1])

    # print '[INFO] xlim', xlim
    # print '[INFO] ylim', ylim
    # plt.ylim(ylim[0], ylim[1])
    # plt.xlim(xlim[0], xlim[1])

    # # ticks
    # # if plotmode == 'scat':
    # #     plt.yticks(np.arange(ylim[0], ylim[1] + 0.05, 0.05))

    # ''' legends '''
    # if plotmode == 'bar':
    #     ypos = np.arange(len(obj.legends))
    #     legends = obj.legends
    #     print '[INFO] legends', legends
    #     plt.xticks(ypos, legends, rotation=45)
    #     plt.margins(0.05)
    #     plt.subplots_adjust(bottom=0.175)
    # if plotmode == 'cdf':
    #     plt.legend(loc='lower right')
    # elif plotmode == 'scat':
    #     plt.legend(loc='lower right')
    #     # plt.legend(loc='upper right')
    # else:
    #     plt.legend(loc='best')

    # plt.xlabel(obj.xlabel, fontsize=14)
    # plt.ylabel(obj.ylabel, fontsize=14)

    # if args.xtick is not None:
    #     xtick_interval = int(args.xtick)
    #     print '[INFO] gonna set xtick to', xtick_interval
    #     xticks = [x for x in range(0, int(xlim[1]) + xtick_interval, xtick_interval)]
    #     plt.xticks(xticks, fontsize=14)
    # else:
    #     xticks = plt.gca().get_xticks()
    #     plt.xticks(xticks, fontsize=14)
    # yticks = plt.gca().get_yticks()
    # plt.yticks(yticks, fontsize=14)

    # plt.legend(prop={'size':16})

    
    if args.outname:
        saveplot()
    plt.show()
