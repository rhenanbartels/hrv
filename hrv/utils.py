# coding: utf-8
import io
from numbers import Number
import re

import numpy as np
from scipy import interpolate


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


def validate_rri(func):
    def _validate(rri, *args, **kwargs):
        _validate_are_numbers(rri)
        _validate_are_nonzero(rri)
        rri = _transform_rri(rri)
        return func(rri)

    def _validate_are_numbers(rri):
        if not all(map(lambda value: isinstance(value, Number), rri)):
            raise ValueError('rri must be a list or numpy.ndarray of numbers')

    def _validate_are_nonzero(rri):
        if not all(map(lambda value: value > 0, rri)):
            raise ValueError('rri must be a list or numpy.ndarray of numbers')

    return _validate

def _transform_rri(rri):
    rri = _transform_rri_to_miliseconds(rri)
    return np.array(rri)

def validate_frequency_domain_arguments(func):
    def _check_frequency_domain_arguments(rri, method='welch', interp_freq=4,
                                          segment_size=256, overlap_size=128,
                                          window_function='hann'):
        _validate_available_methods(method)
        _validate_is_positive_integer(segment_size)
        _validate_is_positive_integer(overlap_size, 'Overlap size')
        _validate_is_overlap_smaller(segment_size, overlap_size)
        _validate_rri_bigger_than_segment_size(segment_size, rri)
        _validate_window_function(window_function)

        return func(rri, method, interp_freq, segment_size, overlap_size)

    def _validate_available_methods(method):
        if not method == 'welch':
            raise ValueError('Welch method must be chose')

    def _validate_is_positive_integer(segment_size, which='Segment'):
        if not isinstance(segment_size, int) or segment_size < 1:
            raise ValueError(
                '{0} size must be an positive integer'.format(which))

    def _validate_is_overlap_smaller(segment_size, overlap_size):
        if not isinstance(segment_size, int) or segment_size < 1:
            raise ValueError('Segment size must be bigger than overlap size')

    def _validate_rri_bigger_than_segment_size(segment_size, rri):
        if len(rri) < segment_size:
            raise ValueError('Segment size bigger than RRi series')

    def _validate_window_function(window_function):
        pass

    return _check_frequency_domain_arguments


def _create_time_info(rri):
    rri_time = np.cumsum(rri) / 1000.0 # make it seconds
    return rri_time - rri_time[0] # force it to start at zero


def _transform_rri_to_miliseconds(rri):
    if np.median(rri) < 1:
        rri *= 1000
    return rri


@validate_rri
def _interpolate_rri(rri, interp_freq=4):
    time_rri = _create_time_info(rri)
    time_rri_interp = np.arange(0, time_rri[-1], 1 / interp_freq)
    tck = interpolate.splrep(time_rri, rri, s=0)
    rri_interp = interpolate.splev(time_rri_interp, tck, der=0)
    return time_rri_interp, rri_interp
