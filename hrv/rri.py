import numpy as np


class RRi:
    def __init__(self, rri):
        self.rri = _validate_rri(rri)

    @property
    def values(self):
        return self.rri


def _validate_rri(rri):
    # Use RRi series median value to check if it is in seconds or miliseconds
    rri = np.array(rri)

    if np.median(rri) < 100:
        rri *= 1000

    return rri
