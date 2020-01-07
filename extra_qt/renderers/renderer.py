from dataclasses import dataclass, field
from typing import Union, List, Any, Type

from PyQt5.QtWidgets import QWidget

from extra_qt.component import Component
from extra_qt.virtual_dom import VirtualNode
from extra_qt.reconciler import reconciler

__all__ = ('ComponentWrapper', 'HostWrapper', 'WrapperT')

WrapperT = Union['ComponentWrapper', 'HostWrapper']
HostNodeT = Any

Updateable = (dict,)


@dataclass
class ComponentWrapper:
    element: VirtualNode  # virtual markup for this component
    host_container: Any = None # Where the underlying node is mounted
    component: Component = None  # Client Component with lifecycle

    # We hold exactly one child, a wrapper for the contents of ``self.component.render()``
    # this may be a further component, or a host DOM tree.
    wrapped_child: WrapperT = None

    pending_state: List[Any] = field(default_factory=list)

    is_rendering: bool = False

    def receive(self, element: VirtualNode):
        return self.update(self.element, element)

    @property
    def next_state(self):
        latest_state = self.component.state

        for state_update in self.pending_state:
            if isinstance(latest_state, Updateable) and isinstance(state_update, Updateable):
                latest_state.update(state_update)
            elif callable(state_update):
                latest_state = state_update(latest_state)
            else:
                latest_state = state_update

        self.pending_state = []
        return latest_state

    def update(self, previous: VirtualNode, latest: VirtualNode):
        self.is_rendering = True
        if previous != latest:
            self.component.before_receive_props(latest.props, latest.children)

        latest_state = self.next_state
        self.component.props = latest.props
        self.component.children = latest.children
        self.component.state = latest_state

        if self.component.should_update(latest.props, latest.children, latest_state):
            self.element = latest
            self.update_child()

        self.is_rendering = False

    def update_child(self):
        new_element = self.component.render()

        if new_element.tag_type == self.wrapped_child.element.tag_type:
            reconciler.receive(self.wrapped_child, new_element)
        else:
            # uproot our contents and remount onto the parent container
            reconciler.unmount(self.wrapped_child)
            self.wrapped_child = reconciler.wrap(new_element)
            reconciler.mount(self.wrapped_child, self.host_container)

    def mount(self, container: QWidget) -> QWidget:
        component_cls: Type[Component] = self.element.tag_type
        self.component = component_cls(self.element.props, self.element.children)
        self.component.wrapper = self

        self.component.before_mount()
        widget = self.initial_mount(container)
        self.component.after_mount()

        return widget

    def unmount(self, container: QWidget = None):
        self.component.before_unmount()
        reconciler.unmount(self.wrapped_child, container)

    def initial_mount(self, container: reconciler.host_wrapper_cls):
        self.host_container = container
        self.wrapped_child = reconciler.wrap(self.component.render())
        return reconciler.mount(self.wrapped_child, container)

    def update_if_necessary(self):
        # don't rerender if we are already rendering.
        if not self.is_rendering:
            self.update(self.element, self.element)


class HostWrapper:
    """
    Essentially defines the same interface as ReactDOMComponent (not React.Component!)
    Because of this frankly, confusing, terminology in React I call these wrappers here.

    You can subclass this to provide custom renderers. Currently we are working towards
    supporting:

      1. Qt5
      2. Dict-literal (for testing)

    There are a few other pieces of code that may need adjusting depending on the renderer.
    In particular, the virtual DOM we use has typed tags (Enum<int>). This is a very simple fix
    if necessary, and for now I like the control that the Enum provides as opposed to bare
    strings.
    """

    @classmethod
    def use_as_renderer(cls):
        """
        Configure the reconciler to use Qt as the render target. This amounts currently
        just to telling the reconciler what it is supposed to wrap host elements
        (i.e. with ``type(el.tag_type) =inst= TagType``) inside.
        """
        from extra_qt import reconciler
        reconciler.host_wrapper_cls = cls
        reconciler.host_node_cls = QWidget

    element: VirtualNode  # virtual markup for this component
    host_node: HostNodeT = None  # what we rendered to
    host_container: HostNodeT = None  # where the node we rendered to is attached
    wrapped_children: List[WrapperT] = field(default_factory=list)

    def receive(self, element: VirtualNode):
        """
        Called when the wrapper receives new markup in order to trigger an update.
        What happens here depends a lot currently on the render target, i.e. that we are
        targeting Qt, as a result, this is implemented (for instance) in ``.qt_renderer``
        """
        raise NotImplementedError()

    def unmount(self, container: HostNodeT = None):
        """
        Uproot me from the rendered tree. This is highly dependent upon the render target.
        For instance, for the Qt renderer, this amounts to disposing of all downstream
        (children, their children, ...) widgets, removing them, and removing
        ``self.hode_node`` from ``self.host_container`` with

        ``self.host_container.layout().remove_widget(self.host_node)``
        """
        raise NotImplementedError()

    def mount(self, container: HostNodeT):
        """
        Attach me to the render tree. This consists of generating (rendering) the output,
        be it a QWidget, a dictionary, or something else, before ultimately attaching it onto
        the target container.
        """
        raise NotImplementedError()
