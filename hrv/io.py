import csv
import re

import numpy as np

from hrv.exceptions import EmptyFileError
from hrv.rri import RRi


__all__ = ['read_from_text', 'read_from_hrm', 'read_from_csv']


def read_from_text(pathname):
    """
    Read RRi series from text files (*.txt).
    Data must be organized in a single column document as follows:
       800
       789
       831
       ...
       793

    Time information is created using the cumulative sum of the RRi series
        time = np.cumsum(rri) / 1000.0
        time -= time[0]

    Parameters
    ----------
    pathname : str
        string containing the path to the file

    Returns
    -------
    rri : RRi array
        instance of the RRi class containing the RRi values

    See Also
    -------
    read_from_hrm, read_from_csv

    Examples
    --------
    >>> from hrv.io import read_from_text
    >>> rri = read_from_text('/path/to/file.txt')
    RRi array([1114., 1113., 1066., 1119., 1062.])
    """
    with open(pathname, "r") as fileobj:
        file_content = fileobj.read()
        if not file_content:
            raise EmptyFileError("empty file!")

        values = list(map(float, re.findall(r"\d\.?[0-9]+", file_content)))

    return RRi(values)


def read_from_hrm(pathname):
    """
    Read RRi series from Polar file format (*.hrm)
    Time information is created using the cumulative sum of the RRi series
        time = np.cumsum(rri) / 1000.0
        time -= time[0]

    Parameters
    ----------
    pathname : str
        string containing the path to the file

    Returns
    -------
    rri : RRi array
        instance of the RRi class containing the RRi values

    See Also
    -------
    read_from_text, read_from_csv

    Reference
    --------
        https://www.polar.com/sites/default/files/Polar_HRM_file%20format.pdf

    Examples
    --------
    >>> from hrv.io import read_from_hrm
    >>> rri = read_from_hrm('/path/to/file.hrm')
    RRi array([1114., 1113., 1066., 1119., 1062.])
    """
    with open(pathname, "r") as fileobj:
        file_content = fileobj.read()
        rri_info_index = file_content.find("[HRData]")
        rri = None
        if rri_info_index < 0:
            raise EmptyFileError("empty file!")
        else:
            rri = np.array(
                list(map(float, re.findall(r"\d+", file_content[rri_info_index:-1]))),
                dtype=np.float64,
            )
            if len(rri) == 0:
                raise EmptyFileError("empty file!")

    return RRi(rri)


def read_from_csv(
    pathname,
    rri_col_index=0,
    time_col_index=None,
    row_offset=0,
    time_parser=int,
    sep=None,
):
    """
    Read RRi series from CSV file format (*.csv)

    Parameters
    ----------
    pathname : str
        string containing the path to the file
    rri_col_index : int, optional
        position of the column that contains the RRi information. Defaults to 0
    time_col_index: int, optional
        position of the column that contains the RRi information. If None,
        time information is created using the cumulative sum of the RRi series
            time = np.cumsum(rri) / 1000.0
            time -= time[0]
        Defaults to None.
    row_offset : int, optional
        skips first 'row_offset' rows. Used when RRi series does not start
        in the first row. Defaults to 0
    time_parser : callable, optional
        callable used to cast time information. Defaults to int()
    sep : char, optional
        delimiter of the columns in the CSV file. If None, `sep` is defined
        using the first 1024 bytes of the file. Defaults to None

    Returns
    -------
    rri : RRi array
        instance of the RRi class containing the RRi values

    See Also
    -------
    read_from_text, read_from_hrm

    Examples
    --------
    >>> from hrv.io import read_from_csv
    >>> rri = read_from_csv('/path/to/file.hrm', time_col_index=1)
    RRi array([1114., 1113., 1066., 1119., 1062.])
    """
    with open(pathname, newline="") as csvfile:
        if sep is None:
            try:
                sep = csv.Sniffer().sniff(csvfile.read(1024)).delimiter
            except csv.Error:
                sep = ","

            csvfile.seek(0)

        reader = csv.reader(csvfile, delimiter=sep)

        for offset in range(row_offset):
            next(reader)

        if time_col_index is None:
            return RRi([float(r[rri_col_index].strip()) for r in reader])

        rri = []
        time = []
        for row in reader:
            rri.append(float(row[rri_col_index].strip()))
            time.append(time_parser(row[time_col_index].strip()))

        return RRi(rri, time)
