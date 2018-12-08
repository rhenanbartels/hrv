Pythonic Package for Heart Rate Variability Analysis
===============================

version number: 0.2.0
author: Rhenan Bartels

Overview
--------

The **hrv** is a simple Python module that brings the most widely used techinques to work with RRi series without losing the **Power** of a native Python object.

Installation / Usage
--------------------

To install use pip:

    $ pip install hrv


Or clone the repo:

    $ git clone https://github.com/rhenanbartels/hrv.git
    $ python setup.py install
    

BASIC USAGE
-------
### Crate a RRi instance
Once you create RRi object you will have the power of a native Python itarable object. This means, that you can loop thought it using a **for loop**, get a just a part of the series using native **slicing** and much more. Let us try it:

```python
from hrv.rri import RRi

rri_list = [800, 810, 815, 750, 753, 905]
rri = RRi(rri_list)

print(rri)
RRi array([800., 810., 815., 750., 753., 905.])
```
##### Slicing
```python
print(rri[0])
800.0

print(type(rri[0]))
numpy.float64

print(rri[::1])
array([800., 815., 753.]) # Future versions will return a RRi object
```
##### Loop

```python
for rri_value in rri:
    print(rri_value)
    
800.0
810.0
815.0
750.0
753.0
905.0
```
##### Note:
When time information is not provided, time array will be created using the cumulative sum of successive RRi. After cumulative sum, the time array is subtracted from the value at `t[0]` to make it start from `0s`

##### RRi object and time information
```python
from hrv.rri import RRi

rri_list = [800, 810, 815, 750, 753, 905]
rri = RRi(rri_list)

print(rri.time)
array([0.   , 0.81 , 1.625, 2.375, 3.128, 4.033]) # Cumsum of rri values minus t[0]

rri = RRi(rri_list, time=[0, 1, 2, 3, 4, 5])
print(rri.time)
[0. 1. 2. 3. 4. 5.]
```
##### Note:
Some validation is made in the time list/array provided to the RRi class, for instance: 
 - RRi and time list/array must have the same length;
 - Time list/array can not have negative values;
 - Time list/array must be monotonic increasing.

### Read RRi file

#### From .txt file

Text files contains a single column with all RRi values. 

```python
from hrv.io import read_from_text
rri = read_from_text('path/to/file.txt')
print(rri)
RRi array([800., 810., 815., 750.])
```

#### From .hrm file

The .hrm files contain the RRi acquired with Polar <sup>&reg;</sup>

A complete guide for .hrm files can be found [here](https://www.polar.com/files/Polar_HRM_file%20format.pdf).

```python
from hrv.io import read_from_hrm
rri = read_from_hrm('path/to/file.hrm')
print(rri)
RRi array([800., 810., 815., 750.])
```

<img src="docs/figures/rri_fig.png" alt="RRi Image"  width=600px;>

#### From .csv file
```python
from hrv.io import read_from_csv
rri = read_from_csv('path/to/file.csv')
print(rri)
RRi array([800., 810., 815., 750.])
```
##### Note:
When using **read_from_csv** you can also provide a column containing time information. Let's check it.

### RRi statistics
The RRi object implements some basic statistics information about its values.

```python
from hrv.rri import RRi

rri = RRi([800, 810, 815, 750, 753, 905])

# mean
rri.mean()
805.5

# median
rri.median()
805.0
```
You can all have a complete overview of its statistical charactheristic
```python
desc = rri.describe()
desc
----------------------------------------
                   rri          hr
----------------------------------------
min             750.00       66.30
max             905.00       80.00
mean            805.50       74.78
var            2646.25       20.85
std              51.44        4.57
median          805.00       74.54
amplitude       155.00       13.70

print(desc['std'])
{'rri': 51.44171459039833, 'hr': 4.5662272355549725}
```

### Plot RRi
The RRi class brings a very easy way to visualize your series
```python
from hrv.io import read_from_text

rri = read_from_text('path/to/file.txt')
fig, ax = rri.plot(color='k')

```

### Filters

Moving Average

```python
from hrv.filters import moving_average
filt_rri = moving_average(rri, order=3)
```

<img src="docs/figures/mov_avg.png" alt="Moving Average Image"  width=600px;>

Moving Median

```python
from hrv.filters import moving_median
filt_rri = moving_median(rri, order=3)
```

<img src="docs/figures/mov_median.png" alt="Moving Median Image"  width=600px;>

Quotient

```python
from hrv.filters import moving_average
filt_rri = moving_median(rri, order=3)
```

<img src="docs/figures/quotient.png" alt="Quotient Filter Image"  width=600px;>


## Time Domain Analysis
```python
from hrv.classical import time_domain
from hrv.utils import open_rri

rri = open_rri('path/to/file.txt')
results = time_domain(rri)
print(results)

{'mhr': 66.528130159638053,
 'mrri': 912.50302419354841,
 'nn50': 337,
 'pnn50': 33.971774193548384,
 'rmssd': 72.849900286450023,
 'sdnn': 96.990569261440797}
```

## Frequency Domain Analysis
```python
from hrv.classical import frequency_domain
from hrv.utils import open_rri

rri = open_rri('path/to/file.txt')
results = frequency_domain(
    rri=rri,
    fs=4.0,
    method='welch',
    interp_method='cubic',
    detrend='linear'
)
print(results)

{'hf': 1874.6342520920668,
 'hfnu': 27.692517001462079,
 'lf': 4894.8271587038234,
 'lf_hf': 2.6110838171452708,
 'lfnu': 72.307482998537921,
 'total_power': 7396.0879278950533,
 'vlf': 626.62651709916258}
```
## Non-linear Analysis
```python
from hrv.classical import non_linear
from hrv.utils import open_rri

rri = open_rri('path/to/file.txt')
results = non_linear(rri)
print(results)

{'sd1': 51.538501037146382,
 'sd2': 127.11460955437322}
```
