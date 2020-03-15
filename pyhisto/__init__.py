#!/usr/env python
'''
This module provides Histogram solutions in python

It is optimized for python 3.5 and above

It includes:
- Histogram: a 1D histogram
- LazyHistogram: a simpler 1D histogram optimized for speed when filling
- GhostHistogram: same interface as a 1D histogram when filling, but does nothing
- Histogram2D: for heat maps.

'''

from .histogram import Histogram
from .lazy_histogram import LazyHistogram
from .ghost_histogram import GhostHistogram
from .histogram2D import Histogram2D

