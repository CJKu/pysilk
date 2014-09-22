#Project Silk Profiler
![img](ttps://github.com/CJKu/pysilk/blob/master/silk.png)

Analysis output data of silk and present in visual way

[What's project silk?](https://wiki.mozilla.org/Project_Silk)

[Where is source code of silk?](https://github.com/JerryShih/gecko-dev/tree/silk-all)

#Prerequisite
* [Install mathplot](http://matplotlib.org/users/installing.html)
* Pythob 2.X

# Steps
You have two ways to fetch silk log data and process it

####silk.py
Execute silk.py directly
```
$ python silk.py /path/to/logfile
```
####SilkProfiler.py
Import SilkProfiler module and call SileProfiler API on demand.
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

#Tesing
* [Testing framework](https://docs.python.org/2/library/unittest.html#module-unittest)
* Test cases
  * Parser - a source file with matched and mismatched line log. Evalute number of matched ones.
  * Function call dependency - call Parse before Open
