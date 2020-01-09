Differences from React
======================

At a high level, there are some important differences: ``extra_qt`` only targets **Qt**,
unlike React which has many renderers now available. Additionally, I anticipate that
React is significantly faster for applications of equal complexity. This is due to:

1. A much more sophisticated diff algorithm in React
2. Fast and mature JavaScript runtimes compared to interpreted Python
3. Few performance optimizations: ``extra_qt.Component`` defines ``should_update``
   essentially as ``lambda _: True`` in the base class (though you can implement
   this of course).

At the same time, for many realistic workloads you probably shouldn't worry too much.

The other main differences concern internal terminology. You can very safely skip all of the
information below unless you want to look through the library code.

Terminology
-----------

To see how the terminology differs you should have some familiarity with the React terminology.
You can read about that at
`React Components, Elements, and Instances <https://reactjs.org/blog/2015/12/18/react-components-elements-and-instances.html>`_.

Element
^^^^^^^

In React, an **element** declares part of the tree by specifying what host
(platform/renderer specific) node implements it, or what ``Component`` renders it,
together with the state and props. An **element** in ``extra_qt`` is the same, it is
an instance of ``extra_qt.virtual_dom.VirtualNode`` this is approximately:

.. code-block:: python

   @dataclass
   class VirtualNode:
       tag_type: Union[TagType, Type['Component']] = None
       props = None
       children = None


Components, components, and instances
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The class defining the behavior is called a ``Component`` with a capital C. This is standard
in many object-oriented languages, including modern JavaScript and in Python, and React and
``extra_qt`` agree on this. React calls the result of ``Component()`` an "instance".
Because this term is overloaded elsewhere, I prefer to call this a **component** (lowercase c).

**Note on internals (safe to skip):** Internally, React also calls a few other things
components: ``DOMComponent`` and ``CompositeComponent``. These wrap elements and instances
of ``Components``. This terminology is too close so I call these ``HostWrapper`` and
``ComponentWrapper`` respectively because of their function to hold and manage lifecycle and
renders for the contained **element** or **component**.