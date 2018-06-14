# coding: utf-8
import io
from numbers import Number
import re

import numpy as np
from scipy import interpolate

from hrv.exceptions import FileNotSupportedError, EmptyFileError
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


def _identify_rri_file_type(file_content):
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
        _validate_positive_numbers(rri)
        rri = _transform_rri(rri)
        return func(rri, *args, **kwargs)

    def _validate_positive_numbers(rri):
        if not all(map(lambda value: isinstance(value, Number) and value > 0,
                       rri)):
            raise ValueError('rri must be a list or numpy.ndarray of positive'
                             ' and non-zero numbers')

    return _validate


def _transform_rri(rri):
    rri = _transform_rri_to_miliseconds(rri)
    return np.array(rri)


def validate_frequency_domain_arguments(func):
    def _check_frequency_domain_arguments(rri, fs=4.0, method='welch',
                                          interp_method='cubic', **kwargs):
        _validate_available_methods(method)
        return func(rri, fs, method, interp_method, **kwargs)

    def _validate_available_methods(method):
        available_methods = ('welch', 'ar')
        if method not in available_methods:
            raise ValueError('Method not supported! Choose among: {}'.format(
                ', '.join(available_methods)))

    return _check_frequency_domain_arguments


def _create_time_info(rri):
    rri_time = np.cumsum(rri) / 1000.0  # make it seconds
    return rri_time - rri_time[0]   # force it to start at zero


def _transform_rri_to_miliseconds(rri):
    if np.median(rri) < 1:
        rri *= 1000
    return rri


def _interpolate_rri(rri, fs=4, interp_method='cubic'):
    if interp_method == 'cubic':
        return _interp_cubic_spline(rri, fs)
    elif interp_method == 'linear':
        return _interp_linear(rri, fs)


def _interp_cubic_spline(rri, fs):
    time_rri = _create_time_info(rri)
    time_rri_interp = _create_interp_time(rri, fs)
    tck = interpolate.splrep(time_rri, rri, s=0)
    rri_interp = interpolate.splev(time_rri_interp, tck, der=0)
    return time_rri_interp, rri_interp


def _interp_linear(rri, fs):
    time_rri = _create_time_info(rri)
    time_rri_interp = _create_interp_time(rri, fs)
    rri_interp = np.interp(time_rri_interp, time_rri, rri)
    return time_rri_interp, rri_interp


def _create_interp_time(rri, fs):
    time_rri = _create_time_info(rri)
    return np.arange(0, time_rri[-1], 1 / float(fs))
