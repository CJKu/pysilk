import sys
import os
import re
import numpy
import matplotlib.pyplot as plt


class SilkProfiler(object):
  def __init__(self, name):
    self.mName = name
    self.mPattern = re.compile(".*" + self.mName + " *, *([0-9]+) *, *([.0-9]+).*")
    self.mMatches = 0       # total amount of matched lines.
    self.mMismatches = 0    # total amount of mismatched lines
    self.mTable = []        # Store peformance data
    self.mSource = None     # Soure log file.

  def Open(self, source):
    try:
      self.mSource = open(source, 'r')
    except IOError as e:
      return False

    return True

  def Parse(self):
    for line in self.mSource:
      matched = re.match(self.mPattern, line)
      if matched:
        self.mMatches += 1
        frame_number = matched.group(1)
        dist = matched.group(2)
        entry = (frame_number, dist)
        self.mTable.append(entry)
      else:
        self.mMismatches += 1

  def Draw(self):
    dists = []
    for entry in self.mTable:
      dists.append(float(entry[1]))

    plt.plot(dists)
    plt.ylabel('touch evet distance')
    plt.show()

  def Print(self):
    for entry in self.mTable:
      print "frame no. = " + entry[0] + ". dist = " + entry[1]

  def Statistic(self):
    dists = []
    for entry in self.mTable:
      dists.append(float(entry[1]))

    print "Total samples = " + str(len(self.mTable))
    print "standard deviation = " + str(numpy.std(dists))
    print "Mean = " + str(numpy.mean(dists))

