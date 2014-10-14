import sys
import os
import re
import shutil

splitpatterns = [("input", ".* Begin .*", ".* End .*")]

class SilkLogSplitter(object):
  """
  1. Find *.log file in specific folder
  2. Split each log file into different log segment
  3. Generat diagrams for each segment
  """
  def __init__(self):
    self.mOutput = ""
    self.mOutputCount = 0

  def Open(self, logdirectory, outputdirectory):
    """
    >>> slp.Open("", "")
    Traceback (most recent call last):
      ...
    OSError: logdirectory must be an existed directory.

    >>> slp.Open("", "./output")
    Traceback (most recent call last):
      ...
    OSError: logdirectory must be an existed directory.

    >>> slp.Open("./silklogsplitter.py", "./output")
    Traceback (most recent call last):
      ...
    OSError: logdirectory must be an existed directory.

    >>> slp.Open("./sample", "./silklogsplitter.py")
    Traceback (most recent call last):
      ...
    OSError: outputdirectory can not be an existed file.

    >>> slp.Open("./sample", "./output")
    ...
    True
    """
    self._Clear()

    # Validate logdirectory
    if False == os.path.exists(logdirectory) or False == os.path.isdir(logdirectory):
      raise OSError("logdirectory must be an existed directory.")

    # Validate outputdirectory and create the destination directory, if need,
    # to store splitted log files
    if os.path.exists(outputdirectory):
      if os.path.isfile(outputdirectory):
        raise OSError("outputdirectory can not be an existed file.")
      else:
        shutil.rmtree(outputdirectory, ignore_errors=True)

    os.mkdir(outputdirectory);
    self.mOutput = outputdirectory

    # iterate *.log files in directory
    self.mOutputCount = 0
    for root, dirs, files in os.walk(logdirectory):
      for filename in files:
        if filename.endswith('.log'):
          self._Split(os.path.join(root, filename))

    return True

  def _Clear(self):
    self.mOutput = ""
    self.mOutputCount = 0

  def _Split(self, filename):
    file = open(filename, 'r')
    for pattern in splitpatterns:
      self._SplitByPattern(pattern, file)

  def _SplitByPattern(self, pattern, file):
    name = pattern[0]
    begin = pattern[1]
    end = pattern[2]
    file.seek(0)

    # Find begin and end line
    # Dump lines between into a file
    for line in file:
      matched = re.match(begin, line)
      if matched:
        logfilename = os.path.join(self.mOutput, name + "_" + str(self.mOutputCount) + ".log")
        output = open(logfilename, "w")
        output.write("# matched pattern begin:" + begin + "\n");
        output.write("# matched pattern end:" + end + "\n");
        self.mOutputCount =  self.mOutputCount + 1

        for line in file:
          matched = re.match(end, line)
          if matched:
            break
          else:
            output.write(line);
        output.close()

if __name__ == "__main__":
  slp = SilkLogSplitter()
  import doctest
  doctest.testmod()

