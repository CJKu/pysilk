
#Prerequisite
* [Install mathplot](http://matplotlib.org/users/installing.html)
* Pythob 2.X

# Steps
You have two ways to fetch silk log data and process it

- Execute silk.py directly
```
$ python silk.py /path/to/logfile
```
- Import SilkProfiler module and call SileProfiler API on demand.
```
$ cd ${where SilkProfiler.py locate}
$ python
  >>>import SilkProfiler as SP
  >>> profiler = SP.SilkProfiler("Silk input resample")
  >>> profiler.Open("/path/to/logfile")
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
``` 
