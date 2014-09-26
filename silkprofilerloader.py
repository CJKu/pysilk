import silkprofiler as SP
import sys

if __name__ == '__main__':
  if len(sys.argv) != 3:
    print "Positional parameter 1: pattern file."
    print "Positional parameter 2: Source log filename."
    raise SystemExit(1)

  if False == SP.profiler.Open(sys.argv[1], sys.argv[2]):
    print "Pattern file or source log file does not exist."
    raise SystemExit(1)

