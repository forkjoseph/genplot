# Stupid Graph Generator ¯\_(ツ)_/¯

### Limitation
It draws one graph PER run... :( So, Joseph suggests using a bash script to call
``genplot.py`` in order to generate multiple graphs at once. To be provided in
samples directory...

### Examples
```bash
## basic
./genplot.py --mode cdf samples/data1.dat samples/data2.dat

## to provide 'basic' working directory 
./genplot.py --mode cdf --basedir samples/ data1.dat data2.dat

## to iterate formatted files
./genplot.py --mode cdf --baseiter samples/data{}.dat 1 2

## to generate PDF version
./genplot.py --mode cdf samples/data1.dat -o /tmp/abc  ## w/ or w/o .pdf 
```

### Legends
To set legends, you have two methods: pre-defined or passing as arguments.
- pre-defined: put ``# legend: ABCDEFGH`` in **EACH** datafile.
- arguments: pass ``--legends ABCD EFGH`` as a list of legends
It's your choice to select :)

### Advanced Examples
```bash
TBD
```


### INSTALL
```bash
$ pip install --user matplotlib numpy scipy

## for mac
$ brew install pdfcrop 

## for Debian
$ sudo apt-get install texlive-extra-utils  
```

#### TODO
- [ ] 
