import silk_profiler as SP
import sys

if len(sys.argv) < 3:
  print "Positional parameter 1: pattern file."
  print "Positional parameter 2: Source log filename."
  sys.exit(1)

if False == SP.profiler.Open(sys.argv[1], sys.argv[2]):
  print "Pattern file or source log file is not exist."
  sys.exit(1)


# Profile data presentattion
SP.profiler.DumpSamples()
SP.profiler.Statistic()
SP.profiler.Draw(SP.Histogram.All)
