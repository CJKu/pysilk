
1. execute silk.py
$ python silk.py ${logfilename}

Or
2. import SilkProfiler
$ cd ${where SilkProfiler.py locate}
$ python
  >>> import SilkProfiler as SP
  >>> profiler = SP.SilkProfiler("Silk input resample")
  >>> profiler.Open("~/Downloads/log.txt")
  True 
  >>> profiler.Parse()
  ## Then, data is ready to be presented.
  # Depend on you need
  # 1. Ifyou want to see trend diagram
  >>> profiler.Draw()
  # 2. For raw sample
  >>> profiler.Print()
  # 3. Statistic data
  >>> profiler.Statistic()
