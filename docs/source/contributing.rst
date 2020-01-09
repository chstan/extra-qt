Contributing to ``extra-qt``
============================

We would gladly appreciate contributions from users and other interested
parties. We also welcome reports of any issues with software or the
clarity of the documentation, and ideas that might advance the core aims
of the project.

If you want to contribute to the code, get in touch and check out some of
the features on our backlog. If you want to poke through the code and make any
changes, you'll want to use `poetry <https://python-poetry.org/>`_.

Installing a development copy
-----------------------------

.. code-block:: bash
   $> git clone https://github.com/chstan/extra-qt.git
   $> pip install --user poetry
   $> cd extra-qt
   $> poetry install

   $> python examples/basic.py

Preferably, you can create an environment to do this in.

Working on a new feature
------------------------

Development will follow *A Successful Git Branching Model*, albeit
with the more standard branch names **develop -> master** and
**master -> release**.

Please contribute new features on feature branches and issue pull/merge requests
in order to make changes.

If you make a large change such as adding a new feature, please contribute or recruit
a willing volunteer to make sure the adjustment is reflected in the documentation
and tests.