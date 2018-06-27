import csv
import re

import numpy as np

from hrv.exceptions import EmptyFileError
from hrv.rri import RRi


def read_from_text(pathname):
    with open(pathname, 'r') as fileobj:
        file_content = fileobj.read()
        if not file_content:
            raise EmptyFileError('empty file!')

        values = list(map(float, re.findall(r'[1-9]\d+', file_content)))

    return RRi(values)


def read_from_hrm(pathname):
    with open(pathname, 'r') as fileobj:
        file_content = fileobj.read()
        rri_info_index = file_content.find('[HRData]')
        rri = None
        if rri_info_index < 0:
            raise EmptyFileError('empty file!')
        else:
            rri = np.array(
                    list(
                        map(
                            float,
                            re.findall(r'\d+', file_content[rri_info_index:-1])
                        )
                    ),
                    dtype=np.float64
            )
            if len(rri) == 0:
                raise EmptyFileError('empty file!')

    return RRi(rri)


def read_from_csv(pathname, rri_col_index=0, time_col_index=None,
                  row_offset=0, time_parser=int, sep=None):

    with open(pathname, newline='') as csvfile:
        if sep is None:
            try:
                sep = csv.Sniffer().sniff(csvfile.read(1024)).delimiter
            except csv.Error:
                sep = ','

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
