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
