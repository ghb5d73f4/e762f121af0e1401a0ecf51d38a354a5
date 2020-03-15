#!/usr/env python
# -*- coding: utf-8 -*-
# -*- format: python -*-
# -*- author: G. Henning -*-
# -*- created: Tue Feb 19 09:24:44 CET 2019 -*-
# -*- copyright: GH/IPHC 2019 -*-
# -*- file: loadhisto.py -*-
# -*- purpose: -*-
 
'''
Load an histogram from a file (.asc), 
   with additional info from the log: 
    - duration
    - hits and pileup
'''

import codecs

from math import sqrt, exp

import matplotlib.pyplot as plt


from pyhisto import Histogram as histo

def plotfit(original,
            background,
            bgsubstracted,
            gaussian,
            residuals,
            figsize=(20,8),
            *w, **kw):
    plt.figure(figsize=(20,8))
    plt.grid(True)
    plt.step(*original.xy())
    plt.step(*background.xy())
    plt.step(*bgsubstracted.xy())
    plt.step(*gaussian.xy())
    plt.step(*residuals.xy())
    plt.show()


class tnthisto(object):
    def __init__(self,
                 directory,
                 card=106, voie=1,
                 calibration=lambda x:x,
                 normalizetoduration=False,):
        #first, identify the file:
        self.filepath = "{0}/Card{1:04d}_histo_V{2}.asc".format(directory,
                                                                card, voie)
        self.logpath =  "{0}/Card{1:04d}_log.txt".format(directory, card)

        # processing the log first
        self.duration = float([_ for _ in codecs.open(self.logpath,
                                                encoding='iso-8859-1',
                                                mode='r').readlines() if "Duration" in _][0].split('=')[-1].split()[0])
        self.hits = tuple(map(float,[_ for _ in codecs.open(self.logpath,
                                                encoding='iso-8859-1',
                                                mode='r').readlines()
                     if "Histogram" in _][voie-1].split(':')[-1].split('/')))
        # now, reading the histogram
        nbins=32769
        norm = 1.0
        if normalizetoduration:
            norm = 1./self.duration
        self.h = histo(nbins) ## TODAO: calibration ?
        for i,v in enumerate(map(int, codecs.open(self.filepath,
                                                  encoding='iso-8859-1',
                                               mode='r').readlines()
                               )):
            #print(i,v)
            self.h.bins[i].count = v*norm
        self.calibration(calibration)

    def calibration(self, function):
        #Apply calibration functiont o bin limits
        # and reorder the bins if necessary (see histogram own clean)
        for b in self.h:
            b.lowedge = function(b.lowedge)
            b.upedge = function(b.upedge)
        pass

    def peakfit(self,
                xmin, xmax):
        hs = self.h.slice(xmin, xmax)
        #getting an estimate of BG
        bg = hs.empty_copy()
        bg_l = hs[0].count
        bg_r = hs[-1].count
        for i,b in enumerate(bg):
            b.count = bg_l + i/len(bg)*(bg_r-bg_l)
        #making bg substracted histogram
        hsbgsub = hs.copy()
        hsbgsub -= bg
        for b in hsbgsub:
            if b.count<0:
                b.count = 0
        # Now, counting the sum
        S = sum(hsbgsub)*hsbgsub[0].width()
        # Mean value
        M = sum( (b.center()*b.count for b in hsbgsub) )/sum(hsbgsub)
        # Stddev
        Stdev = sum( (b.center()**2.*b.count for b in hsbgsub) )/sum(hsbgsub)
        Stdev -= M*M
        Stdev = sqrt(Stdev)
        # making the gaussian, and residual
        G = hsbgsub.empty_copy()
        R = G.copy()
        for i,b in enumerate(G):
            b.count = S/sqrt(2.*3.141592654*Stdev*Stdev)*exp(-(b.center()-M)**2./2./Stdev/Stdev)
            R[i].count = hsbgsub[i] - b.count  
        return {'original':hs,
                'background':bg,
                'bgsubstracted':hsbgsub,
                'gaussian':G,
                'residuals':R,
                'integral':S,
                'mean': M,
                'stdev': Stdev,
                }
            

    def plot(self,
             xmin=0, xmax=None,
             target='screen',
             figsize=(20,10)):
        plt.figure(figsize=figsize)
        plt.grid(True)
        plt.step(*self.h.slice(xmin,xmax).xy(),
                 color='black')
        if target=='screen':
            plt.show()
        else:
            plt.savefig(target)
