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
    self._ResetConfig()

  def GetConfig(self):
    return { "title":       self.mTitle,
             "xlabel":      self.mXLabel,
             "ylabel":      self.mYLabel,
             "drawTable":   self.mStatisticTable,
             "yLimit":      self.mYLimit,
             "yUpperbound": self.mYUpperbound,
             "yLowerbound": self.mYLowerbound}

  def ParseConfig(self, config):
    # Clear context before parsing.
    self._ResetConfig()

    cp = ConfigParser.ConfigParser()
    cp.read(config)

    # [Mandatory] Read config string and create config object accordingly
    try:
      patternOption = cp.get('pattern', 'pattern')
      self.mPattern = re.compile(patternOption)
    except (ConfigParser.NoOptionError, ConfigParser.NoSectionError) as e:
      return False

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

    try:
      self.mStatisticTable = cp.getboolean('diagram', 'drawStatistic')
    except (ConfigParser.NoOptionError, ConfigParser.NoSectionError) as e:
      pass

    try:
      self.mYLimit = cp.get('diagram', 'yLimit')
    except (ConfigParser.NoOptionError, ConfigParser.NoSectionError) as e:
      pass

    if self.mYLimit == "FIXED" or self.mYLimit == "STDEVMULTIPLE":
      try:
        self.mYUpperbound = cp.getfloat('diagram', 'yUpperbound')
      except (ConfigParser.NoOptionError, ConfigParser.NoSectionError) as e:
        return False

      try:
        self.mYLowerbound = cp.getfloat('diagram', 'yLowerbound')
      except (ConfigParser.NoOptionError, ConfigParser.NoSectionError) as e:
        return False

    return (self.mPattern != None)

  def ParseLog(self, log):
    '''
    Parse source log and put matched lines into self.mTable
    '''
    self.mMatches = 0
    self.mMismatches = 0

    with open(log, 'r') as logFile:
      for line in logFile:
        matched = re.match(self.mPattern, line)
        if matched:
          try:
            x = matched.group('x')
            y = matched.group('y')
            entry = (x, y)
            self.mTable.append(entry)

            self.mMatches += 1
          except IndexError as e:
            print "Parse Error : " + line
        else:
          self.mMismatches += 1

    return True

  def _ResetConfig(self):
    self.mPattern = None    # match pattern
    self.mXLabel = ""       # x-axis label
    self.mYLabel = ""       # y-axis label
    self.mTitle = ""        # diagram title
    self.mTable = []        # Store sample data
    self.mStatisticTable = False # display statistic table
    self.mYLimit="NOLIMIT"
    self.mYUpperbound=0
    self.myLowerbound=0

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
  def Line(self, yPlots, config, statistics):
    """
      Draw line histogram.
    """
    # active figure 0
    fig = plt.figure(0)

    # Adjust margin
    params = fig.subplotpars
    params.update(left = 0.05, right = 0.95, top = 0.95, bottom = 0.05)

    # Draw sample trend axes
    ax1 = plt.subplot2grid((4, 4), (0, 0), rowspan = 3, colspan = 4)
    self._DrawSampleAxes(yPlots, ax1, config, statistics)

    # Draw smoothness diagram axes
    if True ==  config["drawTable"]:
      ax2 = plt.subplot2grid((4, 4), (3, 0), colspan = 3)
    else:
      ax2 = plt.subplot2grid((4, 4), (3, 0), colspan =4)

    self._DrawSmoothnessAxes(yPlots, ax2, config, statistics)

    # Draw statistic table
    if True ==  config["drawTable"]:
      ax3 = plt.subplot2grid((4, 4), (3, 3))
      ax3.set_axis_off()
      self._DrawStatisticTable(ax3, statistics)

    # Display figures
    plt.show()

  def Bar(self, yPlots, config, statistics):
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

    plt.title(config["title"])
    plt.xlabel(config["xlabel"])
    plt.ylabel("amount")
    plt.show()

  def _DrawStatisticTable(self, ax, statistics):
    row_labels=['total','mean','stdev', 'max', 'min', 'cv']
    table_vals=[[statistics["total"]],
                [statistics["mean"]],
                [statistics["stdev"]],
                [statistics["max"]],
                [statistics["min"]],
                [statistics["cv"]]
               ]

    colors = plt.cm.BuPu(np.linspace(0, 0.5, len(table_vals)))
    the_table = plt.table(cellText=table_vals,
                          colWidths = [0.4],
                          rowColours=colors,
                          rowLabels = row_labels,
                          cellLoc = 'center',
                          loc='center')
    #the_table.set_fontsize(80)
    the_table.scale(2, 1)
    ax.add_table(the_table)
    ax.set_title('Statistics')

  def _DrawSmoothnessAxes(self, yPlots, ax, config, statistics):
    upperBound = 0
    lowerBound = 0
    y = []
    for index, value in enumerate(yPlots) :
      diff = 0
      if 0 < index:
        diff = value - yPlots[index - 1]
      if diff > upperBound:
        upperBound = diff
      elif diff < lowerBound:
        lowerBound = diff

      y.append(diff)

    x = np.arange(0, len(y), 1)
    ax.set_ylim(lowerBound, upperBound)
    ax.bar(x, y, label = 'y diff', color = 'red', edgecolor = 'red')

    # Draw decorations.
    ax.legend(loc='best', framealpha=0.5)
    ax.set_xlabel(config["xlabel"])
    ax.set_ylabel('smoothness')

  def _DrawSampleAxes(self, yPlots, ax, config, statistics):
    # Draw mean and stddev decoration
    upperBound = min(statistics["mean"] + statistics["stdev"], statistics["max"])
    lowerBound = max(statistics["mean"] - statistics["stdev"], statistics["min"])
    # hot zone area rectangle
    hotZoneTrans = mtransforms.blended_transform_factory(ax.transAxes, ax.transData)
    hotZone = patches.Rectangle((0, lowerBound), width = 1,
            height = upperBound - lowerBound,
            transform = hotZoneTrans, alpha = 0.3, color = 'yellow')
    ax.add_patch(hotZone)
    # mean line
    ax.axhline(y = statistics["mean"], label='mean', linewidth= 1, color='red', ls = '--')
    # stdev line
    ax.axhline(y = upperBound, label='+- stdev', linewidth= 1, color='black', alpha=0.5, ls = '-')
    ax.axhline(y = lowerBound, linewidth= 1, color='black', alpha=0.5, ls = '-')

    # According to config setting, setup limitation of y-axis
    if config["yLimit"] == "FIXED":
      upperBound = config["yUpperbound"]
      lowerBound = config["yLowerbound"]
      ax.set_ylim(lowerBound, upperBound)
    elif config["yLimit"] == "STDEVMULTIPLE":
      upperBound = min(statistics["mean"] + (config["yUpperbound"] * statistics["stdev"]),
                   statistics["max"])
      lowerBound = max(statistics["mean"] - (config["yLowerbound"] * statistics["stdev"]),
                   statistics["min"])
      ax.set_ylim(lowerBound, upperBound)

    # Draw sample plot
    affine = mtransforms.Affine2D().translate(0, 0) + ax.transData
    ax.plot(yPlots, color = 'blue', linestyle = 'solid', linewidth = 1, transform = affine)
        # , marker='o', markerfacecolor='red', markeredgecolor='blue',
        # markeredgewidth=1,markersize=4)
    xPlots = np.arange(0, len(yPlots), 1)
    upperBound = min(statistics["mean"] + statistics["stdev"], statistics["max"])
    lowerBound = max(statistics["mean"] - statistics["stdev"], statistics["min"])
    ax.fill_between(xPlots, upperBound, yPlots, where=yPlots>=upperBound,
                    facecolor = 'blue', interpolate = True, alpha = 0.7)
    ax.fill_between(xPlots, lowerBound, yPlots, where=yPlots<=lowerBound,
                    facecolor = 'blue', interpolate = True, alpha = 0.7)

    # Draw decorations.
    ax.legend(loc='best', framealpha=0.5)
    ax.grid(True)
    ax.set_title(config["title"])
    ax.set_xlabel(config["ylabel"])
    ax.set_ylabel(config["xlabel"])

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

  def Open(self, config, log):
    """
    Open a log file and parse this log file depend on patterns defined in pattern
    file.
    >>> pf.Open(1, 1)
    Traceback (most recent call last):
      ...
    TypeError: config Must be a string!

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
    if not isinstance(config, str):
       raise TypeError("config Must be a string!")
    if not isinstance(log, str):
       raise TypeError("source Must be a string!")
    if False == os.path.exists(config):
      raise IOError("Pattern file does not exist")
    if False == os.path.exists(log):
      raise IOError("Log file does not exist")

    # File resource are ready. Start to parse source files
    success = self.mParser.ParseConfig(config)
    if False == success:
      return success

    success = self.mParser.ParseLog(log)

    return success

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
      print "Coefficient of variation = " + str(cv) + "%"

    return {  "total"  : total,
              "mean"   : mean,
              "stdev"  : stdev,
              "max"    : maxv,
              "min"    : minv,
              "cv"     : cv }

  def Draw(self, histogram = Histogram.Line):
    if 0 == len(self.mParser.mTable):
      print "There is no valid sample in log file."
      return False;

    yPlots = []
    for entry in self.mParser.mTable:
      yPlots.append(float(entry[1]))

    config     = self.mParser.GetConfig()
    statistics = self.Statistic(False)

    if histogram == Histogram.Line:
      self.mDrawer.Line(yPlots, config, statistics)
    elif histogram == Histogram.Bar:
      self.mDrawer.Bar(yPlots, config, statistics)
    elif histogram == Histogram.All:
      self.mDrawer.Line(yPlots, config, statistics)
      self.mDrawer.Bar(yPlots, config, statistics)

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

