import sys
import os
import re
import numpy
import matplotlib.pyplot as plt


class SilkProfiler(object):
  def __init__(self):
    self.mXLabel = ""
    self.mYLabel = ""
    self.mPattern = None
    self.mMatches = 0       # total amount of matched lines.
    self.mMismatches = 0    # total amount of mismatched lines
    self.mTable = []        # Store peformance data
    self.mSource = None     # Soure log file.

  def Open(self, pattern, source):
    patternFile = None

    try:
      self.mSource = open(source, 'r')
      patternFile = open(pattern, 'r')
      if False == self._ReadPattern(patternFile):
        patternFile.close()
        mSource.close()
        return False;

    except IOError as e:
      if patternFile != None:
        patternFile.close()
        patternFile = None

      if self.mSource != None:
        self.mSource.close()
        self.mSource = None

      return False

    return True

  def _ReadPattern(self, patternFile):
    """
    1. Read pattern string
    2. Read x-axis label string
    2. Read y-axis label string
    """
    for line in patternFile:
      # Search pattern string in pattern file
      m = re.search('^pattern[ ]*=[ ]*(.+)', line)
      if m != None:
        patternLine = m.group(1)
        self.mPattern = re.compile(patternLine)
        break

    patternFile.seek(0)
    for line in patternFile:
      # Search x-label string in pattern file
      m = re.search('^xlabel[ ]*=[ ]*(.+)', line)
      if m != None:
        self.mXLabel = m.group(1)
        break

    patternFile.seek(0)
    for line in patternFile:
      # Search y-label string in pattern file
      m = re.search('^ylabel[ ]*=[ ]*(.+)', line)
      if m != None:
        self.mYLabel = m.group(1)
        break

    return (self.mPattern != None)

  def Parse(self):
    for line in self.mSource:
      matched = re.match(self.mPattern, line)
      if matched:
        self.mMatches += 1
        x = matched.group('x')
        y = matched.group('y')
        entry = (x, y)
        self.mTable.append(entry)
      else:
        self.mMismatches += 1

  def Draw(self):
    yPlots = []
    for entry in self.mTable:
      yPlots.append(float(entry[1]))

    plt.plot(yPlots)
    plt.xlabel(self.mXLabel)
    plt.ylabel(self.mYLabel)
    plt.show()

  def Print(self):
    for entry in self.mTable:
      print self.mXLabel + " = " + entry[0] + " / " + self.mYLabel + " = " + entry[1]

  def Statistic(self):
    dists = []
    for entry in self.mTable:
      dists.append(float(entry[1]))

    print "Total samples = " + str(len(self.mTable))
    print "standard deviation = " + str(numpy.std(dists))
    print "Mean = " + str(numpy.mean(dists))

