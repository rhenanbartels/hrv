# coding: utf-8
from numbers import Number
import re

import numpy as np


class EmptyFileError(Exception):
    def __init__(self, value):
        self.value = value
 
    def __str__(self):
        return repr(self.value)

def validate_rri(rri):
    is_list_of_numbers(rri)
    return np.array(rri)

def open_rri(pathname_or_fileobj):
    if isinstance(pathname_or_fileobj, str):
        rri = open_rri_from_path(pathname_or_fileobj)
    return validate_rri(rri)

def open_rri_from_path(pathname):
    if pathname.endswith('.txt'):
        with open(pathname, 'r') as fileobj:
            rri_lines = fileobj.readlines()
            if len(rri_lines) != 0:
                rri = [float(rri.strip()) for rri in rri_lines]
            else:
                raise EmptyFileError('File without rri data')
        return rri
    elif pathname.endswith('.hrm'):
        with open(pathname, 'r') as fileobj:
            rri_lines = fileobj.read()
            begin_of_rri_header = '[HRData]'
            rri_info_index = rri_lines.find(begin_of_rri_header)
            rri_string = re.findall(r'\d+', rri_lines[rri_info_index:-1])
            if len(rri_string) != 0:
                rri = [float(rri.strip()) for rri in rri_string]
            else:
                raise EmptyFileError('File without rri data')
        return rri
    raise IOError('File extension not supported')

def is_list_of_numbers(rri):
    if not all(map(lambda value: isinstance(value, Number), rri)):
        raise ValueError('rri must be a list or numpy.ndarray of numbers')
        response = open_rri(rri_file_name)


