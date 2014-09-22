#Project Silk Profiler
![img](https://github.com/CJKu/pysilk/blob/master/img/silk.png)

To profile project silk, we need a very light-weight tool to analysis output data of gecko::silk and present those data in a visual way.

[What's project silk?](https://wiki.mozilla.org/Project_Silk)

[Where is source code of silk?](https://github.com/JerryShih/gecko-dev/tree/silk-all)

#Prerequisite
* [Install matplot](http://matplotlib.org/users/installing.html)
* Pythob 2.7

# Steps
You have two ways to fetch silk log data and process it

####silk.py
An easier way. Just execute silk.py directly.
```
$ cd /path/to/silk.py
$ python silk.py /path/to/pattern_file /path/to/log_file
Example 
$ python silk.py ./sample/silk_input_resample.pattern ./sample/log.txt
```
####SilkProfiler.py
Import SilkProfiler module and call SileProfiler API on demand.
```
$ cd /path/to/SilkProfiler.py
$ python
  >>>import SilkProfiler as SP
  >>> profiler = SP.SilkProfiler()
  >>> profiler.Open("/path/to/patternfile", "/path/to/logfile")
  True << Check this value
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

####Result
SilkProfiler.Draw()
![img](https://github.com/CJKu/pysilk/blob/master/img/matplot.png)

SilkProfiler.Print()
```
frame number = 196826 / touch event distance = 0.016
frame number = 196827 / touch event distance = 0.030
frame number = 196828 / touch event distance = 0.037
frame number = 196829 / touch event distance = 0.029
frame number = 196830 / touch event distance = 0.037
frame number = 196831 / touch event distance = 0.024
```

SilkProfiler.Statistic()
```
Total samples = 33
standard deviation = 0.0145458964579
Mean = 0.0204848484848
```

#Testing
* [Testing framework](https://docs.python.org/2/library/unittest.html#module-unittest)
* Test cases
  * Parser - a source file with matched and mismatched line log. Evalute number of matched ones.
  * Function call dependency - call Parse before Open

#TBD
* Test cases.
* More statistic result
* Save to DHTML
