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
                    dtype=np.float32
            )
            if len(rri) == 0:
                raise EmptyFileError('empty file!')

    return RRi(rri)
