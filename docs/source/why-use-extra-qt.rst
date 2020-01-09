Why use ``extra-qt``?
=====================

It makes building UIs targeting Qt extremely simple. On the other hand, it
currently has some limitations:

1. Targets only the **Qt Widgets** API. (other render targets are possible, including HTML)
2. Not all Qt Widgets are supported, but adding them is simple

Give it a try if you're curious, and feel free to contribute code or issues. Consider
``extra-qt`` to be a trial run for a React-like UI library with FFI from any
number of languages to targets like **Qt**, **GTK**, **HTML** and others.

Why did you build this?
-----------------------

I needed a view/UI layer for another project,
`DAQuiri <https://daquiri.readthedocs.io/en/latest/>`_, which is essentially a simple
LabView alternative automating most parts of scientific data acquisition.