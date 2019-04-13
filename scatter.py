#!/usr/bin/env python
# -*- coding -*-
import sys, time
import pandas as pd
import matplotlib
matplotlib.rcParams['text.usetex'] = True
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

from matplotlib import rc
rc('font',**{'family':'sans-serif','sans-serif':['Helvetica']})


def yeah(fname):
    print '='*70
    print fname
# Set ipython's max row display
    # pd.set_option('display.max_row', 1000)
    fig = plt.figure(figsize=(10, 4.75))
    ax = fig.add_subplot(111)

    df = pd.read_csv(fname)
    arr_idx = df.index.tolist()
    vz = df['bz_vz'].tolist()
    sp = df['bz_sp'].tolist()

    ax.scatter(arr_idx, vz, label='Verizon', marker='^', color='orange',
            s=24,
            linewidth='1',
            )
    ax.scatter(arr_idx, sp, label='Sprint', marker='+', color='blue',
            s=24,
            linewidth='1',
            )

    print 'avg, min, max, median'
    print np.mean(vz), np.min(vz), np.max(vz), np.median(vz)
    print np.mean(sp), np.min(sp), np.max(sp), np.median(sp)

    cols = df.columns.tolist()
    if 'bz_w1' in cols:
        wifi = df['bz_w1'].tolist()
        wifi = [x for x in wifi if not np.isnan(x)]
        print np.mean(wifi), np.min(wifi), np.max(wifi), np.median(wifi)
        uponly = [x for x in wifi if x > .0]
        print np.mean(uponly), np.min(uponly), np.max(uponly), np.median(uponly)
        realwifi = [x for x in wifi if x > .0 and x < 1000.0]
        print np.mean(realwifi), np.min(realwifi), np.max(realwifi), np.median(realwifi)
        print 'uptime: ', len(uponly), len(wifi)
        print 'avg wifi', np.mean(realwifi)
        wifi = [x if x > .0 else float('inf') for x in wifi]
        ax.scatter(arr_idx, wifi, label='XFinityWiFi',
                marker='x', color='green', 
                s=24,
                linewidth='1',
                )

    plt.rc('axes', labelsize=14)


    plt.legend( bbox_to_anchor=(0,1.02,1,0.2), loc="lower left", 
            mode="expand",
            borderaxespad=0, fancybox=False,
            ncol=3, 
            edgecolor='black',
            scatterpoints = 3,
            prop={'size': 16},
        )

    ax = plt.gca()

    plt.xlim(0, len(arr_idx))
    print len(arr_idx)
    plt.ylim(0, 200)
    ax.get_yaxis().set_tick_params(direction='in')
    ax.get_xaxis().set_tick_params(direction='in')
    plt.yticks( [0, 50, 100, 150, 200], fontsize=14)
    plt.xticks(np.arange(0, len(arr_idx), 500.0), fontsize=14)
    plt.xlabel('Time (in sec)', fontsize=14)
    plt.ylabel('Latency (RTT in msec)', fontsize=14)



    savename = fname.split('/')[1]
    savename = savename.split('.')[0]
    print savename
    savename = 'figs/camera/scatter_' + savename + '.pdf'
    plt.savefig(savename)
    # plt.show()
    return savename

for fname in sys.argv[1:]:
    savename = yeah(fname)
    import subprocess
    cmd = 'pdfcrop ' + savename
    process = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()

    cmd = 'rm ' + savename
    process = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()

    cmd = 'mv ' + savename.split('.')[0] + '-crop.pdf ' + savename
    process = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
