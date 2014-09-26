#Project Silk Profiler
![img](https://github.com/CJKu/pysilk/blob/master/img/silk.png)

To profile project silk, we need a very light-weight tool to analysis output data of gecko::silk and present those data in a visual way.

[What's project silk?](https://wiki.mozilla.org/Project_Silk)

[Where is source code of silk?](https://github.com/JerryShih/gecko-dev/tree/silk-all)

#Prerequisite
* [Install matplot](http://matplotlib.org/users/installing.html)
* Python 2.7
* [html 1.16](https://pypi.python.org/pypi/html)
* [(Optional) Install iPython](http://ipython.org/install.html)
```
Ubuntu setup
$ sudo apt-get install python-pip   # in case you have not ever installed any python packages
$ sudo pip install ipython          # install ipython
$ sudo pip install pyzmq
$ sudo pip install Pygments
Mac setup... Oops...I have forgotten
```
Although iPython is not a must have, I strongly recommend you install this advanced shell, which has qtconsole and better integration with matplot. In qtconsol, output histogram of matplot is embedded inside console
![img](https://github.com/CJKu/pysilk/blob/master/img/ipython.png)

# Steps

Here is an example of how to parse a log file($3) by a pattern file($2)

```
$ cd /path/to/silkprofilerloader.py
$ ipython qtconsole --pylab=inline

In  qtconsole
In [1]: %rub silkprofilerloader.py ./sample/testpattern_pass.pattern ./sample/log.txt
In [2]: SP.profiler.Draw(SP.Histogram.Line)    # Draw line chart
In [3]: SP.profiler.Draw(SP.Histogram.Bar)     # Draw bar chart
In [4]: SP.profiler.Draw(SP.Histogram.All)     # Draw all supported chart
In [5]: SP.profiler.DumpSamples()              # Dump silk raw samples
In [6]: SP.profiler.Statistic(True)            # Dump statistic data
```
![img](https://github.com/CJKu/pysilk/blob/master/img/ipython2.png)

####Result
SilkProfiler.Draw(SP.Histogram.Line)
![img](https://github.com/CJKu/pysilk/blob/master/img/linechart.png)
SilkProfiler.Draw(SP.Histogram.Bar)
![img](https://github.com/CJKu/pysilk/blob/master/img/barchart.png)

SilkProfiler.DumpSamples()
```
1.  frame number = 196826 / touch event distance = 0.016
2.  frame number = 196827 / touch event distance = 0.030
3.  frame number = 196828 / touch event distance = 0.037
4.  frame number = 196829 / touch event distance = 0.029
5.  frame number = 196830 / touch event distance = 0.037
6.  frame number = 196831 / touch event distance = 0.024
```

SilkProfiler.Statistic()
```
Total samples      = 33
Mean value         = 0.0204848484848
Standard deviation = 0.0145458964579
```

#Testing
####doctest
```
$ cd /path/to/pysilk
$ python testsilkprofiler.py -v
```

####unittest
To run test case, simply execute testsilkprofiler.py
```
$ cd /path/to/pysilk
$ python testsilkprofiler.py
....
----------------------------------------------------------------------
Ran 4 tests in 0.002s

OK
```

#TBD
* adb controller
 * Integrate with Jerry's pref setting tool
 * start/ stop logcat
* log splitter
 * split a log file into different ones depend on setup principle
* More statistic result
* Save to DHTML
