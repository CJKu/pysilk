import silkprofiler as sp
import os
import fnmatch

class SilkReportGenerator(object):
  def __init__(self):
    self._Clean()

  def Run(self, patternFile, outputDir, sourceDir, figSize = (0, 0)):
    '''
    1. If there is an "index" file in sourceDir, only generarte figures
       of files in that list. Otherwise,
    2. Generate figures for all *.log files in sourceDir.

    Put generated figures and statistic.txt in outputDir.

    Return False is sourDir does not exists
    >>> rg.Run("./sample/testpattern_pass.pattern", "./", "__folder_not_exist__")
    False

    Return False if sourceDir is a file
    >>> rg.Run("./sample/testpattern_pass.pattern", "./", "silkreportgenerator.py")
    False
    '''
    self._Clean()

    # Populate log filenames as source of SilkProfiler
    if False == self._PopulateSourceFiles(sourceDir):
      return False

    # Parse and generate figures in outputDir
    if False == self._GenerateReport(patternFile, self.mFileList, outputDir, figSize):
      return False

    return True

  def _GenerateReport(self, patternFile, files, outputDir, figSize):
    # Validate patternFile.
    if False == os.path.exists(patternFile) or False == os.path.isfile(patternFile):
      return False

    # For convenience, alwasy destroy output folder, if exists, in the beginning,
    # so that we have a clean output folder
    if True == os.path.exists(outputDir):
      shutil.rmtree(outputDir)

    os.mkdir(outputDir)

    # Use SilkProfiler to generate figure for each source file and put them into
    # outputDir
    for log in files:
      if not os.path.exists(log):
        continue

      profiler = sp.SilkProfiler()
      if not profiler.Open(patternFile, log):
        return False

      # Generate output fullpath
      # XXX: export fileformat config to user?
      (head, tail) = os.path.split(log)
      (root, ext) = os.path.splitext(os.path.join(outputDir, tail))
      root = root + ".png"

      # Generate Line chart for this log
      if False == profiler.SaveHistogram(sp.Histogram.Line, root, figSize):
        return False

      # Generate statistic for this log
      statistic = os.path.join(outputDir, "statistic.txt")
      with open(statistic, 'a+') as statisticFile:
        (head, tail) = os.path.split(root)
        statisticFile.write("[" + tail + "]" + "\n")
        data = profiler.Statistic(False)
        for key in data:
          statisticFile.write(key + " = "+ str(data[key]) + "\n")

    return True

  def _PopulateSourceFiles(self, sourceDir):
    # Validate sourceDir.
    if not os.path.exists(sourceDir) or not os.path.isdir(sourceDir):
      return False

    # If index file exists, parse that file to gather log file list
    # Otherwise, collect all *.log files in sourcDir
    index = os.path.join(sourceDir, "index")
    if True == os.path.exists(index):
      with open(index, 'r') as indexFile:
        for line in indexFile:
          line = line.strip()
          if 0 != len(line):
            if os.path.isabs(line):
              fullname = line
            else:
              fullname = os.path.join(sourceDir, line.strip())

            self.mFileList.append(fullname)
    else:
      for (dirpath, dirnames, filenames) in os.walk(sourceDir):
        for filename in filenames:
          if fnmatch.fnmatch(filename, '*.log'):
            fullname = os.path.join(sourceDir, filename)
            self.mFileList.append(fullname)

        # Only collect top-level files
        break

    print "SilkReportGenerator: Gather " + str(len(self.mFileList)) + " files."

    return True

  def _Clean(self):
    self.mFileList = []

if __name__ == "__main__":
  rg = SilkReportGenerator()
  import doctest
  doctest.testmod()

