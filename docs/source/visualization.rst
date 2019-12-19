RRi Visualization
=================

The RRi class brings a very easy way to visualize your series:

Plot RRi Series
###############

.. code-block:: python

    from hrv.io import read_from_text

    rri = read_from_text('path/to/file.txt')
    fig, ax = rri.plot(color='k')

.. image:: ../figures/rri_fig.png
   :width: 500 px

RRi histogram and Heart Rate Histogram
######################################

.. code-block:: python

    rri.hist()

    rri.hist(hr=True)

.. image:: ../figures/rri_hist.png
   :width: 500 px

.. image:: ../figures/hr_hist.png
   :width: 500 px
