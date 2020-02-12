Contribution start guide
========================

The preferred way to start contributing for the project is creating a virtualenv (you can do by using virtualenv,
virtualenvwrapper, pyenv or whatever tool you'd like). Only **Python 3.x** are supported


Preparing the eviroment
#######################

Create the virtualenv:

.. code-block:: bash

    mkvirtualenv hrv

Install all dependencies:

.. code-block:: bash

    pip install -r requirements.txt

Install development dependencies:

.. code-block:: bash

    pip install -r dev-requirements.txt

Running the tests
#################

In order to run the tests, activate the virtualenv and execute pytest:

.. code-block:: bash

    workon <virtualenv>
    pytest -v
    # or
    make test


Coding and Docstring styles
##########################


Generally, we try to use Python common styles conventions as described
in `PEP 8`_ and `PEP 257`_, which are also followed by the `numpy`_ project.

.. _PEP 8: https://www.python.org/dev/peps/pep-0008/ 
.. _PEP 257: https://www.python.org/dev/peps/pep-0257/
.. _numpy: https://numpydoc.readthedocs.io/en/latest/format.html

Examples
********

We also encourage the  use of code linters, such `isort`_ , `black`_ and `autoflake`_.

.. _isort: https://github.com/timothycrosley/isort
.. _black: https://github.com/psf/black
.. _autoflake: https://github.com/myint/autoflake


.. code-block:: bash

    autoflake --in-place --recursive --remove-unused-variables --remove-all-unused-imports .
    sort -rc .
    black .
    
