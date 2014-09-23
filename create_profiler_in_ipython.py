import silk_profiler as SP
import sys

profiler = SP.SilkProfiler()
if False == profiler.Open("./sample/silk_input_resample.pattern", "./sample/log.txt"):
  print "Pattern file or source log file is not exist."
  sys.exit(1)

