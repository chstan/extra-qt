========
extra-qt
========

**note:** ``extra_qt`` is not feature complete. Its performance is
untested for large or complex UIs.

``extra_qt`` is a view layer for Python around PyQt5.
It aims to be roughly interface comparable to React in Javascript, and currently
uses a primitive version of the original React stack reconciler.
As a result, you can declare ``Component`` classes with the same lifecycle
methods as in React:

.. code-block:: python
   :linenos:

   from extra_qt import Component, render_into_window, create_element
   from extra_qt.dom.qt_dom import *

   class CustomComponent(Component):
       initial_state = 0

       def update_state(self):
           self.set_state(lambda x: x + 1)

       def render(self):
           return group(dict(title='Inner Component',), [
               label(f'Current value is: {self.state}'),
               button(text='Increment', on_click=self.update_state),
           ])

   render_window(create_element(CustomComponent))  # <- Mount application on a new window

Components can compose, specify lifecycle hooks, and receive arguments (``props``). Have a look
at the examples for specifics.

Installation
============

``extra_qt`` only has a single dependency, ``PyQt5``. However, it requires ``python>=3.5``.
You can get it from PyPI with your favorite Python package manager.

.. code-block:: bash

   $> pip install extra_qt
   $> echo "or..."; poetry add extra_qt

In principal, there's nothing preventing use with earlier Python versions, except that I like
type annotations.

Where's the JavaScript?
=======================

There isn't any, ``extra_qt`` directly targets Qt from Python.

Documentation
-------------

**Getting Started**

* :doc:`why-use-extra-qt`
* :doc:`examples`

.. toctree::
   :maxdepth: 1
   :hidden:
   :caption: Getting Started

   why-use-extra-qt
   examples

**Reference**

* :doc:`differences-from-react`
* :doc:`development-efforts`
* :doc:`contributing`
* :doc:`CHANGELOG`

.. toctree::
   :maxdepth: 1
   :hidden:
   :caption: Reference

   differences-from-react
   development-efforts
   contributing
   CHANGELOG

