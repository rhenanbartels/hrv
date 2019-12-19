First Steps
===========

Installation
############

To install use pip:

.. code-block:: bash

   pip install hrv

Or clone the repo:

.. code-block:: bash

   git clone https://github.com/rhenanbartels/hrv.git
   python setup.py install


Basic Usage
######################

**Create an RRi instance**

Once you create an RRi object you will have the power of a native Python iterable object.
This means, that you can loop through it using a **for loop**, get a just a part of the series using native
**slicing** and much more. Let us try it:


.. code-block:: python

    from hrv.rri import RRi

    rri_list = [800, 810, 815, 750, 753, 905]
    rri = RRi(rri_list)

    print(rri)
    RRi array([800., 810., 815., 750., 753., 905.])

**Slicing**

.. code-block:: python

    print(rri[0])
    800.0

    print(type(rri[0]))
    numpy.float64

    print(rri[::2])
    RRi array([800., 815., 753.])

**Logical Indexing**

.. code-block:: python

    from hrv.rri import RRi

    rri = RRi([800, 810, 815, 750, 753, 905])
    rri_ge = rri[rri >= 800]

    rri_ge
    RRi array([800., 810., 815., 905.])

**Loop**

.. code-block:: python

    for rri_value in rri:
        print(rri_value)

    800.0
    810.0
    815.0
    750.0
    753.0
    905.0

**Note:**
When time information is not provided, time array will be created using the cumulative sum of successive RRi. After cumulative sum, the time array is subtracted from the value at `t[0]` to make it start from `0s`

**RRi object and time information**

.. code-block:: python

    from hrv.rri import RRi

    rri_list = [800, 810, 815, 750, 753, 905]
    rri = RRi(rri_list)

    print(rri.time)
    array([0.   , 0.81 , 1.625, 2.375, 3.128, 4.033]) # Cumsum of rri values minus t[0]

    rri = RRi(rri_list, time=[0, 1, 2, 3, 4, 5])
    print(rri.time)
    [0. 1. 2. 3. 4. 5.]

**Note:**
Some validations are made in the time list/array provided to the RRi class, for instance: 

 * RRi and time list/array must have the same length;
 * Time list/array can not have negative values;
 * Time list/array must be monotonic increasing.

**Basic math operations**

With RRi objects you can make math operatins just like a numpy array:

.. code-block:: python

    rri
    RRi array([800., 810., 815., 750., 753., 905.])

    rri * 10
    RRi array([8000., 8100., 8150., 7500., 7530., 9050.])

    rri + 200
    RRi array([1000., 1010., 1015.,  950.,  953., 1105.])

**Works with Numpy functions**

.. code-block:: python

    import numpy as np

    rri = RRi([800, 810, 815, 750, 753, 905])

    sum_rri = np.sum(rri)
    print(sum_rri)
    4833.0

    mean_rri = np.mean(rri)
    print(mean_rri)
    805.5

    std_rri = np.std(rri)
    print(std_rri)
    51.44171459039833
