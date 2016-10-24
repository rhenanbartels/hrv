# coding: utf-8
import io
from numbers import Number
import re

import numpy as np


class EmptyFileError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class FileNotSupportedError(Exception):
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
    elif isinstance(pathname_or_fileobj, io.TextIOWrapper):
        rri = open_rri_from_fileobj(pathname_or_fileobj)
    return validate_rri(rri)

def open_rri_from_path(pathname):
    if pathname.endswith('.txt'):
        with open(pathname, 'r') as fileobj:
            rri = open_rri_from_fileobj(fileobj)
    elif pathname.endswith('.hrm'):
        with open(pathname, 'r') as fileobj:
            rri = open_rri_from_fileobj(fileobj)
    else:
        raise FileNotSupportedError("File extension not supported")
    return rri

def open_rri_from_fileobj(fileobj):
    file_content = fileobj.read()
    file_type = identify_rri_file_type(file_content)
    if file_type == 'text':
        rri = open_rri_from_text(file_content)
        if not rri:
            raise EmptyFileError('File without rri data')
    else:
        rri = open_rri_from_hrm(file_content)
        if not rri:
            raise EmptyFileError('File without rri data')
    return rri

def open_rri_from_text(file_content):
    rri = list(map(float,
                   re.findall(r'\d+', file_content)))
    return rri

def open_rri_from_hrm(file_content):
    rri_info_index = file_content.find('[HRData]')
    rri = None
    if rri_info_index >= 0:
        rri = list(map(float,
                  re.findall(r'\d+', file_content[rri_info_index:-1])))
    return rri

def identify_rri_file_type(file_content):
    is_hrm_file = file_content.find('[HRData]')
    if is_hrm_file >= 0:
        file_type = 'hrm'
    else:
        rri_lines = file_content.split('\n')
        for line in rri_lines:
            current_line_number = re.findall(r'\d+', line)
            if current_line_number:
                if not current_line_number[0] == line.strip():
                    raise FileNotSupportedError('Text file not supported')
        file_type = 'text'
    return file_type

def is_list_of_numbers(rri):
    if not all(map(lambda value: isinstance(value, Number), rri)):
        raise ValueError('rri must be a list or numpy.ndarray of numbers')
        response = open_rri(rri_file_name)
