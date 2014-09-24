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
You have two ways to fetch silk log data and process it

####Rub silk.py in console
Execute silk.py in console directly. silk.py is a simple sample of using SilkProfiler
```
$ cd /path/to/silk.py
$ python silk.py /path/to/pattern_file /path/to/log_file
Example
$ python silk.py ./sample/silk_input_resample.pattern ./sample/log.txt
```
####Run create_profiler_in_ipython.py in ipython::qtconsol
In ipython, %run create_profiler_in_ipython.py to open default pattern and log file. It allows you to experience  how to use SilkProfiler's API
```
$ cd /path/to/silk_profiler.py
$ ipython qtconsole --pylab=inline
In [1]: %run create_profiler_in_ipython.py     # Create profiler object
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
* Test cases.
* More statistic result
* Save to DHTML
* adb command to start/ stop silk log dumping
