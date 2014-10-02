from ConfigParser import ConfigParser

class SilkConfig(object):
  def __init__(self):
    self.mConfig = ConfigParser()
    self.mConfig.read("./silkconfig.ini")

  @property
  def PatternDirectory(self):
    pattern = self.mConfig.get('path', 'pattern')
    return pattern

if __name__ == "__main__":
  sc = SilkConfig()
  print sc.PatternDirectory
