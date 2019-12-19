Pre-Processing
==============

Filters
#######

**Moving Average**

.. code-block:: python

    from hrv.filters import moving_average
    filt_rri = moving_average(rri, order=3)

    fig, ax = rri.plot()
    filt_rri.plot(ax=ax)

<img src="docs/figures/mov_avg.png" alt="Moving Average Image"  width=600px;>

**Moving Median**

.. code-block:: python

    from hrv.filters import moving_median
    filt_rri = moving_median(rri, order=3)

    fig, ax = rri.plot()
    filt_rri.plot(ax=ax)

<img src="docs/figures/mov_median.png" alt="Moving Median Image"  width=600px;>

**Quotient**

`Read more`_

.. _Read more: https://www.ncbi.nlm.nih.gov/pubmed/17322593

.. code-block:: python

    from hrv.filters import quotient
    filt_rri = quotient(rri)

    fig, ax = rri.plot()
    filt_rri.plot(ax=ax)

<img src="docs/figures/quotient.png" alt="Quotient Filter Image"  width=600px;>

**Threshold Filter**

This filter is inspired by the threshold-based artifact correction algorithm offered by kubios_ <sup>&reg;</sup> .
To elect outliers in the tachogram series, each RRi is compared to the median value of local RRi (default N=5).
All the RRi which the difference is greater than the local median value plus a threshold is replaced by
cubic_ interpolated RRi.

.. _kubios: https://www.kubios.com/
.. _cubic: https://en.wikiversity.org/wiki/Cubic_Spline_Interpolation

The threshold filter has five pre-defined strength values:

    * Very Low: 450ms
    * Low: 350ms
    * Medium: 250ms
    * Strong: 150ms
    * Very Strong: 50ms

It also accepts custom threshold values (in milliseconds).
The following snippet shows the ectopic RRi removal:

.. code-block:: python

    from hrv.filters import threshold_filter
    filt_rri = threshold_filter(rri, threshold='medium', local_median_size=5)

    fig, ax = rri.plot()
    filt_rri.plot(ax=ax)

<img src="docs/figures/threshold_filter.png" alt="Threshold Filter Image"  width=600px;>

Detrending
##########

The **hrv** module also offers functions to remove the non-stationary trends from the RRi series.
It allows the removal of slow linear or more complex trends using the following approaches:

**Polynomial models**

Given a degree a polynomial filter is applied to the RRi series and subtracted from the tachogram

.. code-block:: python

    from hrv.detrend import polynomial_detrend

    rri_detrended = polynomial_detrend(rri, degree=1)

    fig, ax = rri.plot()
    rri_detrended.plot(ax, color='k')

<img src="docs/figures/polynomial_detrend.png" alt="Polynomial detrend"  width=600px;>

**Smoothness priors**

Developed by Tarvainen *et al*, allow the removal of complex trends. Visit here_ for more information.
It worth noticing that the detrended RRi with the Smoothness priors approach is also interpolated
and resampled using frequency equals to ```fs```.

.. _here: https://ieeexplore.ieee.org/document/979357

.. code-block:: python

    from hrv.detrend import smoothness_priors

    rri_detrended = smoothness_priors(rri, l=500, fs=4.0)

    fig, ax = rri.plot()
    rri_detrended.plot(ax, color='k')

<img src="docs/figures/smoothness_priors.png" alt="Smoothness priors detrend"  width=600px;>

**Note:**
this approach depends on a numpy matrix inversion and due to floating-point precision it might
present round-off errors in the trend calculation

**Savitzky-Golay**

Uses the lowpass filter known as  Savitzky-Golay filter to smooth the RRi series and remove slow components from the tachogram

.. code-block:: python

    from hrv.detrend import sg_detrend

    rri_detrended = sg_detrend(rri, window_size=51, polyorder=3)

    fig, ax = rri.plot()
    rri_detrended.plot(ax, color='k')

<img src="docs/figures/savitzky_golay_detrend.png" alt="Savitzky Golay Detrend"  width=600px;>
