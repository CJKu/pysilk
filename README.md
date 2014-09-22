
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
$ cd /path/to/SiklProfiler.py
$ python
  >>>import SilkProfiler as SP
  >>> profiler = SP.SilkProfiler("Silk input resample")
  >>> profiler.Open("/path/to/logfile")
  True 
  >>> profiler.Parse()
  ## After Parse(), data is ready for presentation.
  # Depend on your need, you may
  # 1. Display trend diagram
  >>> profiler.Draw()
  # 2. Display raw samples
  >>> profiler.Print()
  # 3. Display statistic data
  >>> profiler.Statistic()
```

By calling SilkProfiler.Draw, matplot window popup and display samples in a trend diagram
![img](https://github.com/CJKu/pysilk/blob/master/matplot.png)
