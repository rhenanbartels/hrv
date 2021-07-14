from tempfile import NamedTemporaryFile

import pytest


@pytest.fixture
def text_file_with_floats():
    temp_rri_text = NamedTemporaryFile(suffix=".text")
    content = """
        0.570
        1.125
        0.570
        1.133
    """
    with open(temp_rri_text.name, "w") as fobj:
        fobj.write(content)
        fobj.seek(0)

    yield temp_rri_text
