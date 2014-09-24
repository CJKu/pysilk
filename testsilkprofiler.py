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
    self.failIf(True == profiler.Open("sample/silk_input_resample.pattern", ""))

    # Open correct files
    self.failIf(False == profiler.Open("sample/silk_input_resample.pattern", "sample/log.txt"))

  def testPatternParsing(self):
    profiler = SP.SilkProfiler()
    # Parse invalid log files should return False
    self.failIf(True == profiler.Open("sample/testpattern_empty.pattern", "sample/log.txt"))
    self.failIf(True == profiler.Open("sample/testpattern_nopattern.pattern", "sample/log.txt"))

    # Parse valid log files
    self.failIf(False == profiler.Open("sample/testpattern_patternonly.pattern", "sample/log.txt"))
    self.failIf(False == profiler.Open("sample/silk_input_resample.pattern", "sample/log.txt"))

# Run the unittests
if __name__ == '__main__':
   unittest.main()
