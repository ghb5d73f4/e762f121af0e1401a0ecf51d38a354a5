#!/usr/env python
# -*- coding: utf-8 -*-
# -*- format: python -*-
# -*- author: G. Henning -*-
# -*- created: Fri Oct 26 12:32:27 CEST 2018 -*-
# -*- copyright: GH/IPHC 2018 -*-
# -*- file: test.py -*-
# -*- purpose: -*-
 
'''
Module docstring
'''

import pyhisto
from pyhisto import Histogram as histo

if __name__=="__main__":
    print("# Starting test")
    h1 = histo(10)
    i=0
    for b in h1:
        b+=i
        i+=1
    print(h1.slice(2,8))
    print("#... done")
