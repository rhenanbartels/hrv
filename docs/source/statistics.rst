RRi statistics
==============

Basic Statistics
################
The RRi object implements some basic statistics information about its values:

* mean
* median
* standard deviation
* variance
* minimum
* maximum
* amplitude

Some examples:

.. code-block:: python

    from hrv.rri import RRi

    rri = RRi([800, 810, 815, 750, 753, 905])

    # mean
    rri.mean()
    805.5

    # median
    rri.median()
    805.0

You can also have a complete overview of its statistical charactheristic

.. code-block:: python

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

RRi Basic Information
#####################

.. code-block:: python

    rri = RRi([800, 810, 815, 750, 753, 905])
    rri.info()

    N Points: 6
    Duration: 4.03s
    Interpolated: False
    Detrended: False
    Memory Usage: 0.05Kb
