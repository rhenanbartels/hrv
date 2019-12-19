Contribution start guide
========================

The preferred way to start contributing for the project is creating a virtualenv (you can do by using virtualenv,
virtualenvwrapper, pyenv or whatever tool you'd like).


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
