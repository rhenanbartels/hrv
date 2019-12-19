RRi Visualization
=================

The RRi class brings a very easy way to visualize your series:

Plot RRi Series
###############

.. code-block:: python

    from hrv.io import read_from_text

    rri = read_from_text('path/to/file.txt')
    fig, ax = rri.plot(color='k')

<img src="docs/figures/rri_fig.png" alt="RRi Image"  width=600px;>

RRi histogram and Heart Rate Histogram
######################################

.. code-block:: python

    rri.hist()

    rri.hist(hr=True)

<img src="docs/figures/rri_hist.png" alt="Moving Average Image"  width=600px;>


<img src="docs/figures/hr_hist.png" alt="Moving Average Image"  width=600px;>
