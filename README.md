#Project Silk Profiler
![img](https://github.com/CJKu/pysilk/blob/master/img/silk.png)

Analysis output data of silk and present in visual way

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
$ python silk.py /path/to/pattern_file /path/to/log_file
Example 
$ python silk.py ./sample/silk_input_resample.pattern ./sample/log.txt
```
####SilkProfiler.py
Import SilkProfiler module and call SileProfiler API on demand.
```
$ cd /path/to/SiklProfiler.py
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

By calling SilkProfiler.Draw(), matplot window popup and display samples in a trend diagram
![img](https://github.com/CJKu/pysilk/blob/master/img/matplot.png)

#Testing
* [Testing framework](https://docs.python.org/2/library/unittest.html#module-unittest)
* Test cases
  * Parser - a source file with matched and mismatched line log. Evalute number of matched ones.
  * Function call dependency - call Parse before Open

#TBD
* Test cases.
* More statistic result
* Save to DHTML
