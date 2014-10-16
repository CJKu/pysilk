import silkreportgenerator as rg
import unittest
import numpy as np
import os
import shutil

class TestReportGenerator(unittest.TestCase):
  def setUp(self):
    # Perform set up actions (if any)
    pass

  def tearDown(self):
    # Perform clean-up actions (if any)
    pass

  def testPopulateSourceFiles(self):

    # There are three files in /sample/generator/has_index folder.
    # Only two of them listed in index file.
    # generator should only gather files which listed in index file
    generator = rg.SilkReportGenerator()
    self.failIf(False ==
        generator._PopulateSourceFiles("./sample/generator/has_index"))
    self.failIf(2 != len(generator.mFileList))

    # There are three log files and a garbage file in /sample/generator/no_index
    # folder.
    # Generator should only collect *.log files.
    generator = rg.SilkReportGenerator()
    self.failIf(False ==
        generator._PopulateSourceFiles("./sample/generator/no_index"))
    self.failIf(3 != len(generator.mFileList))

  def testGenerateReport(self):
    outputDir = "./generator_output"
    sourceDir = "./sample/generator/has_index"

    # Input wrong pattern file.
    if True == os.path.exists(outputDir):
      shutil.rmtree(outputDir)

    generator = rg.SilkReportGenerator()
    generator._PopulateSourceFiles("./sample/generator/has_index")
    files = generator.mFileList
    self.failIf(True == generator._GenerateReport("./not__exist__file.pattern",
                                                  files, outputDir, (0, 0)))

    # Generte figures from a valid folder with index file
    if True == os.path.exists(outputDir):
      shutil.rmtree(outputDir)

    generator = rg.SilkReportGenerator()
    generator._PopulateSourceFiles(sourceDir)
    files = generator.mFileList
    # Expect 2 figures + 1 statistic file
    outputNumber = len(files) + 1
    self.failIf(False == generator._GenerateReport("./sample/testpattern_pass.pattern",
                                                   files, outputDir, (0, 0)))
    self.failIf(outputNumber != len([f for f in os.listdir(outputDir)]))

    shutil.rmtree(outputDir)

  def testRun(self):
    outputDir = "./generator_output"
    sourceDir = "./sample/generator/no_index"

    # Input wrong pattern file.
    if True == os.path.exists(outputDir):
      shutil.rmtree(outputDir)

    generator = rg.SilkReportGenerator()
    self.failIf(generator.Run("./sample/testpattern_pass.pattern", outputDir,
                sourceDir))

    # There are three log files in sourceDir. Two of them are valide log
    # Should generate 2 figures and a statistic file.
    self.failIf(3 != len([f for f in os.listdir(outputDir)]))

    shutil.rmtree(outputDir)

# Run the unittests
if __name__ == '__main__':
   unittest.main()
