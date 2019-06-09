import sys
sys.dont_write_bytecode = True
import os

PINFO = '[INFO] '
PWARN = '[WARN] '
PERR = '[ERROR] '
def with_color(c, s):
    return "\x1b[%dm%s\x1b[0m" % (c, s)

def saveplot(plt, args):
    figname = args.outname
    basedir = args.basedir
    if basedir is None:
        savename = outname
    else:
        if lastslash is True:
            savename = basedir + outname
        else:
            savename = basedir + '/' + outname
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
    print PINFO + 'saving to {}{}'.format(savename, suffix)

    plt.savefig(__tmp)
    from subprocess import call
    call(["pdfcrop", __tmp, __tmp2])
    call(["rm", "-f", __tmp])
    if realsuffix == '.pdf':
        call(["cp", __tmp2, savename + suffix])

    if realsuffix == '.png':
        print PINFO + 'converting to {}{}'.format(savename, realsuffix)
        call(["convert", "-density", "400", __tmp2, savename + realsuffix])
    call(["rm", "-f", __tmp2])
    print PINFO + 'saved to {}{}'.format(savename, realsuffix)
    return plt

def get_filenames(args): 
    if args.basedir and args.baseiter:
        errmsg = 'both args cannot be supported! (choose either)'
        print with_color(31, PERR + errmsg)
        # parser.print_help()
        raise Exception(errmsg)

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
        errmsg = 'You must provide data files to draw mannnnn!'
        print with_color(31, PERR + errmsg)
        raise Exception(errmsg)
        sys.exit(-1)
    return filenames

def get_others(args, filenames=[]):
    legends = []
    if args.legends is not None:
        legends = args.legends
    adjust = args.adjust
    if len(legends) != 0:
        if len(legends) < len(filenames):
            msg = "Number of legends is SMALLER than number of files."
            print with_color(31, PERR + msg)
            raise Exception(msg)
        elif len(legends) != len(filenames):
            msg = '\n[WARN] # of legends mismatch w/ # of files. Are you sure about this?'
            print with_color(33, msg)
    return legends, adjust

