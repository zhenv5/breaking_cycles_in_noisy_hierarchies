# -*- coding: utf-8 -*-
"""
Script to plot recall-precision values with f-measure equi-potential lines.
Created on Dec 16, 2009
@author: Jörn Hees
modified by: Jiankai Sun 
Date: 2017.03.22
"""

import scipy as sc
import pylab as pl
import itertools as it

def fmeasure(p, r):
    """Calculates the fmeasure for precision p and recall r."""
    return 2*p*r / (p+r)


def _fmeasureCurve(f, p):
    """For a given f1 value and precision get the recall value.

    The f1 measure is defined as: f(p,r) = 2*p*r / (p + r).

    If you want to plot "equipotential-lines" into a precision/recall diagramm
    (recall (y) over precision (x)), for a given fixed f value we get this
    function by solving for r:
    """
    return f * p / (2 * p - f)


def _plotFMeasures(fstepsize=.1,  stepsize=0.0005, start = 0.0, end = 1.0):
    """Plots 10 fmeasure Curves into the current canvas."""
    p = sc.arange(start, end, stepsize)[1:]
    for f in sc.arange(0., 1., fstepsize)[1:]:
        points = [(x, _fmeasureCurve(f, x)) for x in p
                  if 0 < _fmeasureCurve(f, x) <= 1.5]
        try:
            xs, ys = zip(*points)
            curve, = pl.plot(xs, ys, "--", color="gray", linewidth=0.8)  # , label=r"$f=%.1f$"%f) # exclude labels, for legend
            # bad hack:
            # gets the 10th last datapoint, from that goes a bit to the left, and a bit down
            datapoint_x_loc = int(len(xs)/2)
            datapoint_y_loc = int(len(ys)/2)
            # x_left = 0.05
            # y_left = 0.035
            x_left = 0.035
            y_left = -0.02
            pl.annotate(r"$f=%.1f$" % f, xy=(xs[datapoint_x_loc], ys[datapoint_y_loc]), xytext=(xs[datapoint_x_loc] - x_left, ys[datapoint_y_loc] - y_left), size="small", color="gray")
        except Exception as e:
            print e 

#colors = "gcmbbbrrryk"
#colors = "yyybbbrrrckgm"  # 7 is a prime, so we'll loop over all combinations of colors and markers, when zipping their cycles
colors = "ycyybbbbrrrr"
#markers = "so^>v<dph8"  # +x taken out, as no color.
markers = "^*>vsod*sod*ph8<"

# # if you don't believe the prime loop:
# icons = set()
# for i,j in it.izip(it.cycle(colors),it.cycle(markers)):
#    if (i,j) in icons: break
#    icons.add((i,j))
# print len(icons), len(colors)*len(markers)


def plotPrecisionRecallDiagram(title="title", points=None, labels=None, loc="best",xy_ranges = [0.6, 1.0, 0.6, 1.0], save_file = None):
    """Plot (precision,recall) values with 10 f-Measure equipotential lines.

    Plots into the current canvas.
    Points is a list of (precision,recall) pairs.
    Optionally you can also provide labels (list of strings), which will be
    used to create a legend, which is located at loc.
    """
    if labels:
        ax = pl.axes([0.1, 0.1, 0.7, 0.8])  # llc_x, llc_y, width, height
    else:
        ax = pl.gca()
    pl.title(title)
    pl.xlabel("Precision")
    pl.ylabel("Recall")
    _plotFMeasures(start = min(xy_ranges[0],xy_ranges[2]), end = max(xy_ranges[1],xy_ranges[3]))

    if points:
        getColor = it.cycle(colors).next
        getMarker = it.cycle(markers).next

        scps = []  # scatter points
        for i, (x, y) in enumerate(points):
            label = None
            if labels:
                label = labels[i]
            print i, x, y, label
            scp = ax.scatter(x, y, label=label, s=50, linewidths=0.75,
                             facecolor=getColor(), alpha=0.75, marker=getMarker())
            scps.append(scp)
            # pl.plot(x,y, label=label, marker=getMarker(), markeredgewidth=0.75, markerfacecolor=getColor())
            # if labels: pl.text(x, y, label, fontsize="x-small")
        if labels:
            # pl.legend(scps, labels, loc=loc, scatterpoints=1, numpoints=1, fancybox=True) # passing scps & labels explicitly to work around a bug with legend seeming to miss out the 2nd scatterplot
            #pl.legend(scps, labels, loc=(1.01, 0), scatterpoints=1, numpoints=1, fancybox=True)  # passing scps & labels explicitly to work around a bug with legend seeming to miss out the 2nd scatterplot
            pl.legend(scps, labels, loc= loc, scatterpoints=1, numpoints=1, fancybox=True,fontsize = 10)  # passing scps & labels explicitly to work around a bug with legend seeming to miss out the 2nd scatterplot
    pl.axis(xy_ranges)  # xmin, xmax, ymin, ymax
    if save_file:
        pl.savefig(save_file)
    
    pl.show()
    pl.close()

def load_points(file_name):
    f = open(file_name,"r")
    points = {}
    for l in f.readlines():
        s = l.split()[0]
        p = float(l.split()[1])
        r = float(l.split()[2])
        points[s] = (p,r)
    f.close()
    return points 

def draw_recall_precision(data_file,title = "Precision_Recall"):
    data_dict = load_points(data_file)
    sorted_pairs = sorted(data_dict.iteritems(), key = lambda x: x[0])
    values = [v for _,v in sorted_pairs]
    keys = [k for k,_ in sorted_pairs]
    plotPrecisionRecallDiagram(title = title,points = values,labels = keys, loc = "lower right" ,xy_ranges = [0.2,1,0.2,1], save_file = data_file[:len(data_file)-4] + "_" + title+".pdf")

import argparse
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-i","--input",default= " ", help = "input performance file: method_name precision recall f1_score...")
    parser.add_argument("--title",default = "Precision Recall Performance", help = "title to show figures")
    args = parser.parse_args()    
    draw_recall_precision(args.input,title = args.title)
