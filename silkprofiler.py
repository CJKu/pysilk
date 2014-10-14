import sys
import os
import re
import numpy as np
import matplotlib.pyplot as plt
import decimal
import pylab
import ConfigParser
from numpy import ma
from matplotlib import scale as mscale
from matplotlib import transforms as mtransforms
from matplotlib.ticker import Formatter, FixedLocator
import matplotlib.patches as patches

class Histogram(object):
  """
  Histogram enum.
  """
  Line = 1
  Bar = 2
  All = 10

class SilkParser(object):
  """
  1. Parse pattern file.
  2. Parse log file
  """
  def __init__(self):
    self.mPattern = None    # match pattern
    self.mXLabel = ""       # x-axis label
    self.mYLabel = ""       # y-axis label
    self.mTitle = ""        # diagram title
    self.mTable = []        # Store sample data

  def Parse(self, log, pattern):
    """
      Parse patterFile to fetch pattern strings to match logFile.
      Depend on pattern strings aquired from patternFile, fetch matched line log
      from logFile.
    """
    # Clear context before parsing.
    self.mPattern = None    # match pattern
    self.mXLabel = ""       # x-axis label
    self.mYLabel = ""       # y-axis label
    self.mTitle = ""        # diagram title
    self.mTable = []        # Store sample data

    # Parsing
    if False == self._ParsePattern(pattern):
      return False
    if False == self._ParseLog(log):
      return False

    return True

  def _ParsePattern(self, pattern):
    """
    1. Read pattern string
    2. Read x-axis label string
    2. Read y-axis label string
    """
    cp = ConfigParser.ConfigParser()
    cp.read(pattern)

    # [Mandatory] Read pattern string and create pattern object accordingly
    try:
      patternOption = cp.get('pattern', 'pattern')
      self.mPattern = re.compile(patternOption)
    except (ConfigParser.NoOptionError, ConfigParser.NoSectionError) as e:
      return False

    # [Option] Read xlabel and ylabel
    try:
      self.mXLabel = cp.get('diagram', 'xlabel')
    except (ConfigParser.NoOptionError, ConfigParser.NoSectionError) as e:
      pass

    try:
      self.mYLabel = cp.get('diagram', 'ylabel')
    except (ConfigParser.NoOptionError, ConfigParser.NoSectionError) as e:
      pass

    try:
      self.mTitle = cp.get('diagram', 'title')
    except (ConfigParser.NoOptionError, ConfigParser.NoSectionError) as e:
      pass

    return (self.mPattern != None)

  def _ParseLog(self, log):
    self.mMatches = 0
    self.mMismatches = 0

    with open(log, 'r') as logFile:
      for line in logFile:
        matched = re.match(self.mPattern, line)
        if matched:
          try:
            self.mMatches += 1
            x = matched.group('x')
            y = matched.group('y')
            entry = (x, y)
            self.mTable.append(entry)
          except IndexError as e:
            print "Parse Error : " + line
        else:
          self.mMismatches += 1

    return True
'''
class MeanScale(mscale.ScaleBase):
  name = 'meanscale'

  def __init__(self, axis, **kwargs):
    mscale.ScaleBase.__init__(self)

    self.mean = kwargs.pop("mean")
    self.maxv = kwargs.pop("maxv")
    self.minv = kwargs.pop("minv")

  def get_transform(self):
    #return mtransforms.IdentityTransform(self)
    #return self.LantitudeTransform((self.mean, self.maxv, self.minv))
    affine = mtransforms.Affine2D()
    affinenslate(0, 1)
    return affine
  
  def set_default_locators_and_formatters(self, axis):
    lowserStride = (self.mean - self.minv) / 5
    upperStride = (self.maxv - self.mean) / 5

    # Define ycks
    axis.set_major_locator(
      FixedLocator(
        np.arange(self.minv, self.mean, lowserStride).tolist() +
        np.arange(self.mean, self.maxv + upperStride, upperStride).tolist()
      )
    )
    # I don't really care about formatter, at last, for now

  #def limit_range_for_scale(self, vmin, vmax, minpos):
  #    return self.minv, self.maxv

  class LantitudeTransform(mtransforms.Affine2D):
    input_dims = 1
    output_dims = 1
    is_separable = True

    def __init__(self, statistic):
      mtransforms.Transform.__init__(self)
      self.statistic = statistic

    def transform_affine(self, a):
        print a
        return a
    #def transform_non_affine(self, a):
    #  print a
    #  return a
      #return np.log(np.abs(np.tan(a) + 1.0 / np.cos(a)))

    def inverted(self):
      return MeanScale.InvertedLatitudeTransform(self.statistic)

  class InvertedLantitudeTransform(mtransforms.Affine2D):
    input_dims = 1
    output_dims = 1
    is_separable = True

    def __init__(self, statistic):
      mtransforms.Transform.__init__(self)
      self.statistic = statistic

    def transform_affine(self, a):
      #return np.arctan(np.sinh(a))
      return a

    def inverted(self):
      return MeanScale.LatitudeTransform(self.statistic)
'''

class SilkDrawer(object):
  """
  Histogram drawer
  """
  def Line(self, yPlots, decorations, statistic):
    """
      Draw line histogram.
    """
    # Determin figure size according the the number of plots
    self._DetermineFigureSize(len(yPlots))

    ax = plt.subplot(111)

    # Draw mean and stddev decoration
    total, mean, stdev, maxv, minv = statistic
    upperBound = min(mean + stdev, maxv)
    lowerBound = max(mean - stdev, minv)
    ax.axhline(y = mean, linewidth= 2, color='red', ls = '--')
    ax.axhline(y = upperBound, linewidth= 2, color='green', ls = '--')
    ax.axhline(y = lowerBound, linewidth= 2, color='green', ls = '--')

    hotZoneTrans = mtransforms.blended_transform_factory(ax.transAxes, ax.transData)
    hotZone = patches.Rectangle((0, lowerBound), width = 1,
            height = upperBound - lowerBound,
            transform = hotZoneTrans, alpha = 0.5, color = 'yellow')
    ax.add_patch(hotZone)
    ax.set_ylim(lowerBound, upperBound)

    # Set yaxis locator
    '''
    plt.gca().set_yscale('meanscale', mean=mean, maxv=maxv, minv=minv)
    lowserStride = (mean - minv) / 5
    upperStride = (maxv - mean) / 5
    ax.yaxis.set_major_locator(
      FixedLocator(
        np.arange(minv, mean, lowserStride).tolist() +
        np.arange(mean, maxv + upperStride, upperStride).tolist()
      )
    )
    '''
    #ax.yaxis.set_transform(affine)
    # Draw plots
    affine = mtransforms.Affine2D().translate(0, 0) + ax.transData
    ax.plot(yPlots, color='blue', linestyle='solid', linewidth=2, marker='o',
        markerfacecolor='red', markeredgecolor='blue', markeredgewidth=1,
        markersize=4, transform = affine)

    # Draw decorations.
    ax.grid(True)
    plt.title(decorations[0])
    plt.xlabel(decorations[1])
    plt.ylabel(decorations[2])
    plt.show()

  def Bar(self, yPlots, diagram):
    """
      Draw bar histogram
    """
    self._DetermineFigureSize(10)
    minPlot = np.min(yPlots)
    maxPlot = np.max(yPlots)

    # All yPlots have the same value. Perfect condition
    if minPlot == maxPlot:
      plt.bar([2], [len(yPlots)])
      return

    # Divide yPlots into 10 groups
    # it's.... so uglyyyyyy... find a better way.
    ranges = np.linspace(minPlot, maxPlot, 10).tolist()

    accounts = [0] * 10
    for plot in yPlots:
      for i,n in enumerate(ranges):
        if plot <= n:
          accounts[i] += 1
          break

    # Round xticks to shrink the space between ticks
    xTickLabels = ranges;
    for i,n in enumerate(xTickLabels) :
      xTickLabels[i] = round(xTickLabels[i], 3)

    xTickPositions = np.linspace(0.5, 10.5, 10).tolist()
    plt.xticks(xTickPositions, xTickLabels)

    # Draw bar chart.
    barPositions = np.linspace(0., 10., 10).tolist()
    plt.bar(barPositions, accounts)

    plt.title(diagram[0])
    plt.xlabel(diagram[1])
    plt.ylabel("amount")
    plt.show()

  def _DetermineFigureSize(self, samples):
    '''
    A figure in matplotlib means the whole window in the user interface.
    '''
    F = pylab.gcf()
    DPI = F.get_dpi()
    DefaultSize = F.get_size_inches()

    # Display 300 samples, 5 seconds, in 2880-width histogram
    # Which means distance between each sample is 2800 / 300.
    # Keep this density unless we get more then 300 samples
    minWidth = DefaultSize[1] * 1.618034
    maxWidth = 2800 / DPI
    width = maxWidth
    fixHeight = 480 / DPI

    ratio = 300.0 / float(samples)
    if ratio > 1.0:
      width = width / ratio
    if width < minWidth:
      width = minWidth
    plt.figure(figsize=(width, fixHeight))

class SilkProfiler(object):
  """
  1. Aggregate mParser to parser soruce log and pattern
  2. Aggregate mDrawer to generate histogram
  """
  def __init__(self):
    self.mParser = SilkParser()
    self.mDrawer = SilkDrawer()

  def Open(self, pattern, log):
    """
    Open a log file and parse this log file depend on patterns defined in pattern
    file.
    >>> pf.Open(1, 1)
    Traceback (most recent call last):
      ...
    TypeError: pattern Must be a string!

    >>> pf.Open("", 1)
    Traceback (most recent call last):
      ...
    TypeError: source Must be a string!

    >>> pf.Open("", "")
    Traceback (most recent call last):
      ...
    IOError: Pattern file does not exist

    >>> pf.Open("sample/testpattern_pass.pattern", "")
    Traceback (most recent call last):
      ...
    IOError: Log file does not exist

    >>> pf.Open("", "sample/testlog.log")
    Traceback (most recent call last):
      ...
    IOError: Pattern file does not exist

    >>> pf.Open("sample/testpattern_pass.pattern", "sample/testlog.log")
    True
    """
    # Validate parameters
    if not isinstance(pattern, str):
       raise TypeError("pattern Must be a string!")
    if not isinstance(log, str):
       raise TypeError("source Must be a string!")
    if False == os.path.exists(pattern):
      raise IOError("Pattern file does not exist")
    if False == os.path.exists(log):
      raise IOError("Log file does not exist")

    # File resource are ready. Start to parse source files
    return self.mParser.Parse(log, pattern)

  def DumpSamples(self, to = None):
    """
    Print all samples on stdout
    """
    for index, value in enumerate(self.mParser.mTable) :
      print str(index) + ".\t" + self.mParser.mXLabel + " = " + value[0] + " / " + \
      self.mParser.mYLabel + " = " + value[1]

    return True

  def Statistic(self, doPrint = True):
    """
      Print statistic data on stdout.
      1. Total samples: number of silk line-log
      2. stddev
      3. mean value
    """
    dists = []
    for entry in self.mParser.mTable:
      dists.append(float(entry[1]))

    mean  = np.nan
    stdev = np.nan
    maxv  = np.nan
    minv  = np.nan
    cv    = np.nan

    total = len(self.mParser.mTable)
    if 0 != total:
      mean  = np.mean(dists)
      stdev = np.std(dists)
      maxv  = np.max(dists)
      minv  = np.min(dists)
      if 0 != mean:
        cv   = stdev * 100 / mean

    if doPrint:
      print "Total samples            = " + str(total)
      print "Max value                = " + str(maxv)
      print "Min value                = " + str(minv)
      print "Mean value               = " + str(mean)
      print "Standard deviation       = " + str(stdev)
      print "Coefficient of variation = " + str(cv)

    return {  "total"  : total,
              "mean"   : mean,
              "stdev"  : stdev,
              "max"    : maxv,
              "min"    : minv,
              "cv"     : cv }

  def Draw(self, histogram = Histogram.Line):
    yPlots = []
    for entry in self.mParser.mTable:
      yPlots.append(float(entry[1]))

    decorations = (self.mParser.mTitle, self.mParser.mXLabel, self.mParser.mYLabel)
    statistic = self.Statistic(False)

    if 0 == len(yPlots):
      print "There is no valid sample in log file."
      return False;

    if histogram == Histogram.Line:
      self.mDrawer.Line(yPlots, decorations, statistic)
    elif histogram == Histogram.Bar:
      self.mDrawer.Bar(yPlots, decorations, statistic)
    elif histogram == Histogram.All:
      self.mDrawer.Line(yPlots, decorations, statistic)
      self.mDrawer.Bar(yPlots, decorations, statistic)

    return True

  def SaveTo(self, html):
    """
      1. Save matplot image
      2. Save mTable in HTML table
      3. Save statistic data.
    """

    return True

#mscale.register_scale(MeanScale)
profiler = SilkProfiler()

if __name__ == "__main__":
  pf = SilkProfiler()
  import doctest
  doctest.testmod()

