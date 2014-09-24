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

  def testOpen(self):
    profiler = SP.SilkProfiler()
    # Open files which do not exist.
    self.failIf(True == profiler.Open("", ""))
    self.failIf(True == profiler.Open("/usr/XXX", "/tmp/YYY"))
    self.failIf(True == profiler.Open("", "sample/log.txt"))
    self.failIf(True == profiler.Open("sample/testpattern_pass.pattern", ""))

    # Open correct files
    self.failIf(False == profiler.Open("sample/testpattern_pass.pattern", "sample/log.txt"))

  def testPatternParsing(self):
    profiler = SP.SilkProfiler()
    # Parse invalid log files should return False
    self.failIf(True == profiler.Open("sample/testpattern_empty.pattern", "sample/log.txt"))
    self.failIf(True == profiler.Open("sample/testpattern_nopattern.pattern", "sample/log.txt"))

    # Parse valid log files
    self.failIf(False == profiler.Open("sample/testpattern_patternonly.pattern", "sample/log.txt"))
    self.failIf(False == profiler.Open("sample/testpattern_pass.pattern", "sample/log.txt"))

    # Repeat parsing patterns. Make sure context is independent between two parsing
    # Parse testpattern_pass, which has xy label and pattern string, and then parse
    # testpattern_patternonly, which has pattern string only. xy label should be
    # cleared.
    profiler = SP.SilkProfiler()
    self.failIf(False == profiler.Open("sample/testpattern_pass.pattern", "sample/log.txt"))
    self.failIf(False == profiler.Open("sample/testpattern_patternonly.pattern", "sample/log.txt"))
    self.failIf("" != profiler.mParser.mXLabel)
    self.failIf("" != profiler.mParser.mYLabel)

  def testLogParsing(self):
    profiler = SP.SilkProfiler()

    # Only one silk ling log in testlog_one.txt
    self.failIf(False == profiler.Open("sample/testpattern_pass.pattern", "sample/testlog_one.txt"))
    statistic = profiler.Statistic(False)
    self.failIf(1 != statistic[0])

    # Open and parse testlog.txt
    self.failIf(False == profiler.Open("sample/testpattern_pass.pattern", "sample/testlog.txt"))
    total, mean, stdev = profiler.Statistic(False)
    self.failIf(10 != total)
    self.failIf(5.5 != mean)

    # Repeat parsing logs. Make sure context is independent between two parsing
    # Keep loading testlog_one two times, total samples should not be accumulated.
    profiler = SP.SilkProfiler()
    self.failIf(False == profiler.Open("sample/testpattern_pass.pattern", "sample/testlog_one.txt"))
    self.failIf(False == profiler.Open("sample/testpattern_pass.pattern", "sample/testlog_one.txt"))
    statistic = profiler.Statistic(False)
    self.failIf(1 != statistic[0])

# Run the unittests
if __name__ == '__main__':
   unittest.main()
