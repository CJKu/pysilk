import silkprofiler as SP
import unittest

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
    self.failIf(True == profiler.Open("sample/testpattern_empty.pattern", "sample/log.log"))
    self.failIf(True == profiler.Open("sample/testpattern_nopattern.pattern", "sample/log.log"))

    # Parse valid log files
    self.failIf(False == profiler.Open("sample/testpattern_patternonly.pattern", "sample/log.log"))
    self.failIf(False == profiler.Open("sample/testpattern_pass.pattern", "sample/log.log"))

    # Repeat parsing patterns. Make sure context is independent between two parsing
    # Parse testpattern_pass, which has xy label and pattern string, and then parse
    # testpattern_patternonly, which has pattern string only. xy label should be
    # cleared.
    profiler = SP.SilkProfiler()
    self.failIf(False == profiler.Open("sample/testpattern_pass.pattern", "sample/log.log"))
    self.failIf(False == profiler.Open("sample/testpattern_patternonly.pattern", "sample/log.log"))
    self.failIf("" != profiler.mParser.mXLabel)
    self.failIf("" != profiler.mParser.mYLabel)

  def testLogParsing(self):
    # Only one silk ling log in testlog_one.log
    profiler = SP.SilkProfiler()
    self.failIf(False == profiler.Open("sample/testpattern_pass.pattern", "sample/testlog_one.log"))
    statistic = profiler.Statistic(False)
    self.failIf(1 != statistic[0])

    # Open and parse testlog.log
    profiler = SP.SilkProfiler()
    self.failIf(False == profiler.Open("sample/testpattern_pass.pattern", "sample/testlog.log"))
    total, mean, stdev, maxv, minv = profiler.Statistic(False)
    self.failIf(10 != total)
    self.failIf(5.5 != mean)
    self.failIf(10 != maxv)
    self.failIf(1 != minv)

    # Open and parse testlog_zero.log, which is an empty file
    profiler = SP.SilkProfiler()
    self.failIf(False == profiler.Open("sample/testpattern_pass.pattern", "sample/testlog_zero.log"))
    total, mean, stdev, maxv, minv = profiler.Statistic(False)
    self.failIf(0 != total)
    self.failIf(0 != mean)
    self.failIf(0 != stdev)
    self.failIf(0 != maxv)
    self.failIf(0 != minv)


    # Repeat parsing logs. Make sure context is independent between two parsing
    # Keep loading testlog_one two times, total samples should not be accumulated.
    profiler = SP.SilkProfiler()
    self.failIf(False == profiler.Open("sample/testpattern_pass.pattern", "sample/testlog_one.log"))
    self.failIf(False == profiler.Open("sample/testpattern_pass.pattern", "sample/testlog_one.log"))
    statistic = profiler.Statistic(False)
    self.failIf(1 != statistic[0])

# Run the unittests
if __name__ == '__main__':
   unittest.main()
