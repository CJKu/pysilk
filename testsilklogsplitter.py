import silklogsplitter as SLP
import unittest

class TestSilkLogSplitter(unittest.TestCase):
  def setUp(self):
    # Perform set up actions (if any)
    pass

  def tearDown(self):
    # Perform clean-up actions (if any)
    pass

  def testCreation(self):
    splitter = SLP.SilkLogSplitter()
    self.assertNotEqual(splitter, None, "Creation test failed")

  def testOpen(self):
    splitter = SLP.SilkLogSplitter()

    # Open and parse valide log files
    splitter.Open("./sample", "./output")

    # Again, open with invalid folders.
    # Assert that splitter context is clear.
    try:
      splitter.Open("", "")
    except:
      pass

    self.assertEqual(splitter.mOutput, "")
    self.assertEqual(splitter.mOutputCount, 0)

# Run the unittests
if __name__ == '__main__':
   unittest.main()
