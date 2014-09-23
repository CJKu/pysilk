import sys
import os
import re
import numpy
import matplotlib.pyplot as plt


class SilkProfiler(object):
  def __init__(self):
    self.mXLabel = ""       # x-axis label
    self.mYLabel = ""       # y-axis label
    self.mPattern = None    # pattern object
    self.mMatches = 0       # total amount of matched lines.
    self.mMismatches = 0    # total amount of mismatched lines
    self.mTable = []        # Store peformance data
    self.mSource = None     # Soure log file.
    self.mInit = False

  def Open(self, pattern, source):
    patternFile = None
    self.mInit = False
    try:
      self.mSource = open(source, 'r')
      patternFile = open(pattern, 'r')
      if False == self._ReadPattern(patternFile):
        patternFile.close()
        mSource.close()
        return False

    except IOError as e:
      if patternFile != None:
        patternFile.close()
        patternFile = None

      if self.mSource != None:
        self.mSource.close()
        self.mSource = None

      return False

    self.mInit = True
    return True

  def _ReadPattern(self, patternFile):
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

  def Parse(self):
    if False == self.mInit:
      return False

    # Clear mTable
    del self.mTable[:]

    # Validate source file handle
    if self.mSource == None:
      return False

    for line in self.mSource:
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

  def Draw(self):
    if False == self.mInit:
      return False

    yPlots = []
    for entry in self.mTable:
      yPlots.append(float(entry[1]))

    plt.plot(yPlots)
    plt.xlabel(self.mXLabel)
    plt.ylabel(self.mYLabel)
    plt.show()

    return True

  def Print(self):
    if False == self.mInit:
      return False

    for entry in self.mTable:
      print self.mXLabel + " = " + entry[0] + " / " + self.mYLabel + " = " + entry[1]

    return True

  def Statistic(self):
    """
      Print statistic data on standard output.
      1. Total samples: number of silk line-log
      2. stddev
      3. mean value
    """
    if False == self.mInit:
      return False

    dists = []
    for entry in self.mTable:
      dists.append(float(entry[1]))

    print "Total samples = " + str(len(self.mTable))
    print "standard deviation = " + str(numpy.std(dists))
    print "Mean = " + str(numpy.mean(dists))
    return True

  def SaveTo(self, html):
    """
      1. Save matplot image
      2. Save mTable in HTML table
      3. Save statistic data.
    """
    if False == self.mInit:
      return False

    return True
