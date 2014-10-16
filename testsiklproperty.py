import silkproperty as SP
import unittest

class TestSilkPropertyFunction(unittest.TestCase):
  def setUp(self):
    # Perform set up actions (if any)
    self.mProps = SP.SilkAllProps;
    pass

  def tearDown(self):
    # Perform clean-up actions (if any)
    pass

  def testSetProps(self):
    sp = SP.SilkProperty()
    props = SP.SilkAllProps

    for prop in props:
      sp.SetProp((prop[0], 1))
      self.failIf(str("1") != sp.GetProp(prop[0]))

# Run the unittests
if __name__ == '__main__':
   unittest.main()
