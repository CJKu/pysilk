import SilkProfiler as SP
import sys

if len(sys.argv) < 2:
  print "Source log filename is required."
  sys.exit(1)

profiler = SP.SilkProfiler("Silk input resample")
if False == profiler.Open(sys.argv[1]):
  print "Source log file is not exist."
  sys.exit(1)

profiler.Parse()

# Profile data presentattion
#profiler.Print()
profiler.Statistic()
profiler.Draw()
