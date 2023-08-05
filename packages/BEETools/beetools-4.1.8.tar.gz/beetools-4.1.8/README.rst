BEE Project
===========

A python library that adds to the long list of "scaffolding" projects already available.  Bright Edge eServices used some (crude) in-house tracking methods.  This module is in support of these crude methods and will evolve over time to be less crude.










.. image:: https://img.shields.io/pypi/v/bee-Project
   :target: https://pypi.org/project/bee-Project/
   :alt: PyPI
.. image:: https://github.com/hendrikdutoit/bee-project/actions/workflows/ci.yaml/badge.svg
   :target: https://github.com/hendrikdutoit/bee-project/actions/workflows/ci.yaml
   :alt: GitHub Actions - CI
.. image:: https://github.com/hendrikdutoit/bee-project/actions/workflows/pre-commit.yaml/badge.svg
   :target: https://github.com/hendrikdutoit/bee-project/actions/workflows/pre-commit.yaml
   :alt: GitHub Actions - pre-commit
.. image:: https://img.shields.io/codecov/c/gh/hendrikdutoit/bee-Project
   :target: https://app.codecov.io/gh/hendrikdutoit/bee-Project
   :alt: Codecov


It adds to the long list of "scaffolding" projects already available.  Bright Edge eServices used some (crude) in-house tracking methods.  This module is in support of these crude methods and will be evolved over time to be less crude.

Installation
------------

.. code-block:: bash

   pip install bee-Project

Testing
-------

This project uses ``pytest`` to run tests and also to test docstring examples.

Install the test dependencies.

.. code-block:: bash

   $ pip install -r requirements_test.txt

Run the tests.

.. code-block:: bash

    $ pytest --doctest-modules tests src\apputils\apputils.py
    === 3 passed in 0.13 seconds ===

Developing
----------

This project uses ``black`` to format code and ``flake8`` for linting. We also support ``pre-commit`` to ensure these have been run. To configure your local environment please install these development dependencies and set up the commit hooks.

.. code-block:: bash

   $ pip install black flake8 pre-commit
   $ pre-commit install

Releasing
---------

Releases are published automatically when a tag is pushed to GitHub.

.. code-block:: bash

   # Set next version number
   export RELEASE=x.x.x

   # Create tags
   git commit --allow-empty -m "Release $RELEASE"
   git tag -a $RELEASE -m "Version $RELEASE"

   # Push
   git push upstream --tags