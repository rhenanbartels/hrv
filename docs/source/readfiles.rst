Read RRi files
==============

Read .txt files
####################

Text files contains a single column with all RRi values.
Example of RRi text file

.. code-block:: bash

    800
    810
    815
    750

.. code-block:: python

    from hrv.io import read_from_text

    rri = read_from_text('path/to/file.txt')

    print(rri)
    RRi array([800., 810., 815., 750.])

Read Polar <sup>&reg;</sup> (.hrm) files
########################################

The .hrm files contain the RRi acquired with Polar <sup>&reg;</sup>

A complete guide for .hrm files can be found polar_

.. _polar: https://www.polar.com/files/Polar_HRM_file%20format.pdf

.. code-block:: python

    from hrv.io import read_from_hrm

    rri = read_from_hrm('path/to/file.hrm')

    print(rri)
    RRi array([800., 810., 815., 750.])

Read .csv files
#####################################
Example of csv file:

.. code-block:: bash

    800,
    810,
    815,
    750,

.. code-block:: python

    from hrv.io import read_from_csv

    rri = read_from_csv('path/to/file.csv')

    print(rri)
    RRi array([800., 810., 815., 750.])

**Note**:
When using **read_from_csv** you can also provide a column containing time information. Let's check it.

.. code-block:: bash

    800,1
    810,2
    815,3
    750,4

.. code-block:: python

    rri = read_from_csv('path/to/file.csv', time_col_index=1)

    print(rri)
    RRi array([800., 810., 815., 750.])

    print(rri.time)
    array([0., 1., 2., 3., 4.])

RRi Sample Data
###############

The hrv module comes with some sample data. It contains:

* RRi collected during rest
* RRi collected during exercise
* RRi containing ectopic beats

**Rest RRi**

.. code-block:: python

    from hrv.sampledata import load_rest_rri

    rri = load_rest_rri()
    rri.plot()

<img src=”docs/figures/rri_hist.png” alt=”Moving Average Image” width=600px;>

**Exercise RRi**

.. code-block:: python

    from hrv.sampledata import load_exercise_rri

    rri = load_exercise_rri()
    rri.plot()

<img src=”docs/figures/rri_hist.png” alt=”Moving Average Image” width=600px;>

**Noisy RRi**

.. code-block:: python

    from hrv.sampledata import load_noisy_rri

    rri = load_noisy_rri()
    rri.plot()

<img src=”docs/figures/rri_hist.png” alt=”Moving Average Image” width=600px;>
