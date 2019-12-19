Time Slicing
============

It is also possible to slice RRi series with time range information
(in **seconds**).

In the following example, we are taking a slice that starts at `100s ` and ends at `200s`.

.. code-block:: python

    from hrv.io import read_from_text

    rri = read_from_text('path/to/file.txt')
    rri_range = rri.time_range(start=100, end=200)

    fig, ax = rri_range.plot(marker='.')

<img src="docs/figures/rri_range.png" alt="Moving Average Image"  width=600px;>

Time offset can be reset from the RRi series range:

.. code-block:: python

    rri_range.reset_time(inplace=True)

<img src="docs/figures/rri_range_reset.png" alt="Moving Average Image"  width=600px;>
