import SilkProfiler as SP
import sys

if len(sys.argv) < 2:
  print "Source log filename is required."
  sys.exit(1)

# You may import SilkProfiler.py in shell directly and
# call the following functions sequentially
# >>> import SilkProfiler as SP
# >>> profiler = SP.SilkProfiler("Silk input resample")
# >>> profiler.Open(sys.argv[1])
# >>> profiler.Parse()
# Then, data is ready to be presented.
# Depend on you need
# 1. Ifyou want to see trend diagram
#    >>> profiler.Draw()
# 2. For raw sample
#    >>> profiler.Print()
# 3. Statistic data
#    >>> profiler.Statistic()
profiler = SP.SilkProfiler("Silk input resample")
if False == profiler.Open(sys.argv[1]):
  print "Source log file is not exist."
  sys.exit(1)

profiler.Parse()
#profiler.Draw()
#profiler.Print()
#profiler.Statistic()
