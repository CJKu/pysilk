import sys
import os
import re
import numpy as np
import matplotlib.pyplot as plt
import decimal
import pylab

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
    self.mTable = []        # Store sample data

  def Parse(self, logFile, patternFile):
    """
      Parse patterFile to fetch pattern strings to match logFile.
      Depend on pattern strings aquired from patternFile, fetch matched line log
      from logFile.
    """

    # Clear context before parsing.
    self.mPattern = None    # match pattern
    self.mXLabel = ""       # x-axis label
    self.mYLabel = ""       # y-axis label
    self.mTable = []        # Store sample data

    # Parsing
    if False == self._ParsePattern(patternFile):
      return False
    if False == self._ParseLog(logFile):
      return False

    return True

  def _ParsePattern(self, patternFile):
    """
    1. Read pattern string
    2. Read x-axis label string
    2. Read y-axis label string
    """
    # [Mandatory] Read pattern string and create pattern object accordingly
    for line in patternFile:
      # Search pattern string in pattern file
      m = re.search('^pattern[ ]*=[ ]*(.+)', line)
      if m != None:
        patternLine = m.group(1)
        self.mPattern = re.compile(patternLine)
        break

    # [Option] Read x-label string
    patternFile.seek(0)
    for line in patternFile:
      # Search x-label string in pattern file
      m = re.search('^xlabel[ ]*=[ ]*(.+)', line)
      if m != None:
        self.mXLabel = m.group(1)
        break

    # [Option] Read y-label string
    patternFile.seek(0)
    for line in patternFile:
      # Search y-label string in pattern file
      m = re.search('^ylabel[ ]*=[ ]*(.+)', line)
      if m != None:
        self.mYLabel = m.group(1)
        break

    return (self.mPattern != None)

  def _ParseLog(self, logFile):
    self.mMatches = 0
    self.mMismatches = 0

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

class SilkDrawer(object):
  """
  Histogram drawer
  """
  def Line(self, yPlots, xLabel, yLabel):
    """
      Draw line histogram.
    """
    self._EvaluateHistogramSize(len(yPlots))
    plt.plot(yPlots, color='blue', linestyle='solid', linewidth=2, marker='o',
        markerfacecolor='red', markeredgecolor='blue', markeredgewidth=1,
        markersize=6)

    plt.grid(True)
    plt.xlabel(xLabel)
    plt.ylabel(yLabel)
    plt.show()

  def Bar(self, yPlots, xLabel, yLabel):
    """
      Draw bar histogram
    """
    self._EvaluateHistogramSize(10)
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

    plt.xlabel(yLabel)
    plt.ylabel("amount")
    plt.show()

  def _EvaluateHistogramSize(self, samples):
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

  def Open(self, pattern, source):
    """
    >>> pf.Open("", "")
    Traceback (most recent call last):
      ...
    IOError: [Errno 2] No such file or directory: ''

    >>> pf.Open("sample/testpattern_pass.pattern", "")
    Traceback (most recent call last):
      ...
    IOError: [Errno 2] No such file or directory: ''

    >>> pf.Open("", "sample/testlog.txt")
    Traceback (most recent call last):
      ...
    IOError: [Errno 2] No such file or directory: ''

    >>> pf.Open("sample/testpattern_pass.pattern", "sample/testlog.txt")
    True
    """
    patternFile = None
    logFile = None

    logFile = open(source, 'r')
    patternFile = open(pattern, 'r')

    # File resource are ready. Start to parse source files
    ret = self.mParser.Parse(logFile, patternFile)

    # Clean up resource in the end
    patternFile.close()
    patternFile = None
    logFile.close()
    lofFile = None

    return ret

  def DumpSamples(self):
    """
    Print all samples on stdout
    """
    i = 1
    for entry in self.mParser.mTable:
      print str(i) + ".\t" + self.mParser.mXLabel + " = " + entry[0] + " / " + \
      self.mParser.mYLabel + " = " + entry[1]
      i += 1

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

    total = len(self.mParser.mTable)
    mean = np.mean(dists)
    stdev = np.std(dists)

    if doPrint:
      print "Total samples      = " + str(total)
      print "Mean value         = " + str(mean)
      print "Standard deviation = " + str(stdev)

    return (total, mean, stdev)

  def Draw(self, histogram = Histogram.Line):
    yPlots = []
    for entry in self.mParser.mTable:
      yPlots.append(float(entry[1]))

    if histogram == Histogram.Line:
      self.mDrawer.Line(yPlots, self.mParser.mXLabel, self.mParser.mYLabel)
    elif histogram == Histogram.Bar:
      self.mDrawer.Bar(yPlots, self.mParser.mXLabel, self.mParser.mYLabel)
    elif histogram == Histogram.All:
      self.mDrawer.Line(yPlots, self.mParser.mXLabel, self.mParser.mYLabel)
      self.mDrawer.Bar(yPlots, self.mParser.mXLabel, self.mParser.mYLabel)

    return True

  def SaveTo(self, html):
    """
      1. Save matplot image
      2. Save mTable in HTML table
      3. Save statistic data.
    """

    return True

profiler = SilkProfiler()

if __name__ == "__main__":
  pf = SilkProfiler()
  import doctest
  doctest.testmod()

