=============
littleworkers
=============

:author: Daniel Lindsley
:date: 2011/11/10
:version: 0.3.1
:license: BSD

Little process-based workers to do your bidding.

Deliberately minimalist, you provide the number of workers to use & a list of
commands (to be executed at the shell) & littleworkers will eat through the
list as fast as it can.


Topics
======

.. toctree::
   :maxdepth: 1

   tutorial
   api


Requirements
============

* Python 2.6+ (may work with Python 2.5)

``littleworkers`` is tested & works on Mac OS X/Linux/BSD. It may work on
Windows (!) but is untested. Feedback welcome.


Installation
============

You can install from PyPI using ``pip`` (or ``easy_install`` if you prefer
broken, unmaintained software)::

    pip install littleworkers

The only dependencies are in Python's stdlib & the code is pure Python, so
there's nothing to compile.


Testing
=======

``littleworkers`` is maintained with a passing test suite at all times. You
should use nose_ or similar tools to run the tests like::

    nosetests tests.py

Output is currently pretty verbose, which will be fixed in the future.

.. _nose:: http://readthedocs.org/docs/nose/en/latest/

Contributions
=============

Contributions are welcome & should be submitted as pull requests on GitHub_.
The pull request must have:

* Only the code needed to add the feature or fix the bug (not several in one)
* Added tests to cover the change
* Internal docs in the form of docstrings
* If it changes the public API, it should include docs
* Must be BSD-licensed code

.. _GitHub:: https://github.com/toastdriven/littleworkers
