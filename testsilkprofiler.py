import silkprofiler as SP
import unittest
import numpy as np
import os
import shutil

class TestSilkProfilerFunction(unittest.TestCase):
  def setUp(self):
    # Perform set up actions (if any)
    pass

  def tearDown(self):
    # Perform clean-up actions (if any)
    pass

  def testCreation(self):
    profiler = SP.SilkProfiler()
    self.assertNotEqual(profiler, None, "Creation test failed")

  def testPatternParsing(self):
    profiler = SP.SilkProfiler()

    # Parse invalid log files should return False
    self.failIf(True == profiler.Open("sample/testpattern_empty.pattern",
                                      "sample/log.log"))
    self.failIf(True == profiler.Open("sample/testpattern_nopattern.pattern",
                                      "sample/log.log"))

    # Parse valid log files
    self.failIf(False == profiler.Open("sample/testpattern_patternonly.pattern",
                                       "sample/log.log"))
    self.failIf(False == profiler.Open("sample/testpattern_pass.pattern",
                                       "sample/log.log"))

    # Repeat parsing patterns. Make sure context is independent between two parsing
    # Parse testpattern_pass, which has xy label and pattern string, and then parse
    # testpattern_patternonly, which has pattern string only. xy label should be
    # cleared.
    profiler = SP.SilkProfiler()
    self.failIf(False == profiler.Open("sample/testpattern_pass.pattern",
                                       "sample/log.log"))
    self.failIf(False == profiler.Open("sample/testpattern_patternonly.pattern",
                                       "sample/log.log"))
    self.failIf("" != profiler.mParser.mXLabel)
    self.failIf("" != profiler.mParser.mYLabel)

  def testLogParsing(self):
    # Get statistic data of a profiler which has not parsed any log file yet
    profiler = SP.SilkProfiler()
    statistics = profiler.Statistic(False)
    self.failIf(0 != statistics["total"])
    self.failIf(True != np.isnan(statistics["mean"]))
    self.failIf(True != np.isnan(statistics["stdev"]))
    self.failIf(True != np.isnan(statistics["max"]))
    self.failIf(True != np.isnan(statistics["min"]))
    self.failIf(True != np.isnan(statistics["cv"]))

    # Parse a log file which has only one valid line log
    profiler = SP.SilkProfiler()
    self.failIf(False == profiler.Open("sample/testpattern_pass.pattern",
                                       "sample/testlog_one.log"))
    statistics = profiler.Statistic(False)
    self.failIf(1 != statistics["total"])

    # Parse a log file which has 10 valid line log
    profiler = SP.SilkProfiler()
    self.failIf(False == profiler.Open("sample/testpattern_pass.pattern",
                                       "sample/testlog.log"))
    statistics = profiler.Statistic(False)
    self.failIf(10 != statistics["total"])
    self.failIf(5.5 != statistics["mean"])
    self.failIf(10 != statistics["max"])
    self.failIf(1 != statistics["min"])

    # Parse a log file which has no valid log
    profiler = SP.SilkProfiler()
    self.failIf(False == profiler.Open("sample/testpattern_pass.pattern",
                                       "sample/testlog_zero.log"))
    statistics = profiler.Statistic(False)
    self.failIf(0 != statistics["total"])
    self.failIf(True != np.isnan(statistics["mean"]))
    self.failIf(True != np.isnan(statistics["stdev"]))
    self.failIf(True != np.isnan(statistics["max"]))
    self.failIf(True != np.isnan(statistics["min"]))
    self.failIf(True != np.isnan(statistics["cv"]))

    # Repeat parsing logs. Make sure context is independent between two parsing
    # Keep loading testlog_one two times, total samples should not be accumulated.
    profiler = SP.SilkProfiler()
    self.failIf(False == profiler.Open("sample/testpattern_pass.pattern",
                                       "sample/testlog_one.log"))
    self.failIf(False == profiler.Open("sample/testpattern_pass.pattern",
                                       "sample/testlog_one.log"))
    statistics = profiler.Statistic(False)
    self.failIf(1 != statistics["total"])

  def testDrawing(self):
    # Open a log file which has no valid log again.
    # Expect return False while calling SilkProfiler.Draw()
    profiler = SP.SilkProfiler()
    # Return False before Open a valide config and log file.
    self.failIf(True == profiler.Draw())
    self.failIf(False == profiler.Open("sample/testpattern_pass.pattern",
                                       "sample/testlog_zero.log"))
    self.failIf(True == profiler.Draw())

  def testSave(self):
    profiler = SP.SilkProfiler()
    # Return False before Open a valide config and log file.
    self.failIf(True == profiler.SaveHistogram(SP.Histogram.All, None))

    self.failIf(False == profiler.Open("sample/testpattern_pass.pattern",
                                       "sample/testlog_one.log"))

    dirname = "./savethistogramfolder"
    filename = "test.png"

    # Save to direct filename
    path = filename
    if True == os.path.exists(filename):
      os.remove(filename)

    self.failIf(False == profiler.SaveHistogram(SP.Histogram.Line, path))
    self.failIf(False == os.path.exists(path))

    if True == os.path.exists(filename):
      os.remove(filename)

    # Save to a relative path
    path = os.path.join(dirname, filename)
    if True == os.path.exists(dirname):
      shutil.rmtree(dirname)

    self.failIf(False == profiler.SaveHistogram(SP.Histogram.Line, path))
    self.failIf(False == os.path.exists(path))

    if True == os.path.exists(dirname):
      shutil.rmtree(dirname)

    # Save to an absolute path
    path = os.path.join(dirname, filename)
    path = os.path.abspath(path)
    if True == os.path.exists(dirname):
      shutil.rmtree(dirname)

    self.failIf(False == profiler.SaveHistogram(SP.Histogram.Line, path))
    self.failIf(False == os.path.exists(path))

    if True == os.path.exists(dirname):
      shutil.rmtree(dirname)

# Run the unittests
if __name__ == '__main__':
   unittest.main()
