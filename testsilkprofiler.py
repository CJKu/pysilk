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
    print "TestSilkProfilerFunction::testCreation start..."

    profiler = SP.SilkProfiler()
    self.assertNotEqual(profiler, None, "Creation test failed")

  def testOpen(self):
    print "TestSilkProfilerFunction::testOpen start..."

    profiler = SP.SilkProfiler()
    # Open files which do not exist.
    self.failIf(True == profiler.Open("", ""))
    self.failIf(True == profiler.Open("/usr/XXX", "/tmp/YYY"))
    self.failIf(True == profiler.Open("", "sample/log.txt"))
    self.failIf(True == profiler.Open("sample/testpattern_pass.pattern", ""))

    # Open correct files
    self.failIf(False == profiler.Open("sample/testpattern_pass.pattern", "sample/log.txt"))

  def testPatternParsing(self):
    print "TestSilkProfilerFunction::testPatternParsing start..."

    profiler = SP.SilkProfiler()
    # Parse invalid log files should return False
    self.failIf(True == profiler.Open("sample/testpattern_empty.pattern", "sample/log.txt"))
    self.failIf(True == profiler.Open("sample/testpattern_nopattern.pattern", "sample/log.txt"))

    # Parse valid log files
    self.failIf(False == profiler.Open("sample/testpattern_patternonly.pattern", "sample/log.txt"))
    self.failIf(False == profiler.Open("sample/testpattern_pass.pattern", "sample/log.txt"))

  def testLogParsing(self):
    print "TestSilkProfilerFunction::testLogParsing start..."

    profiler = SP.SilkProfiler()

    # Only one silk ling log in testlog_one.txt
    self.failIf(False == profiler.Open("sample/testpattern_pass.pattern", "sample/testlog_one.txt"))
    total = profiler.Statistic()
    self.failIf(1 != total[0])

    # Open and parse testlog.txt
    self.failIf(False == profiler.Open("sample/testpattern_pass.pattern", "sample/testlog.txt"))
    total, mean, stdev = profiler.Statistic()
    self.failIf(10 != total)
    self.failIf(5.5 != mean)

# Run the unittests
if __name__ == '__main__':
   unittest.main()
