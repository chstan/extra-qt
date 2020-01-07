"""
Essentially a tiny experimental port of React to Python to use Qt rendering.
"""

__version__ = '0.1.0'


from PyQt5.QtWidgets import QWidget

from extra_qt.renderers.renderer import ComponentWrapper, WrapperT
from extra_qt.virtual_dom import VirtualNode, TagType
from extra_qt.component import Component
from extra_qt.reconciler import reconciler


def initial_render(element: VirtualNode, container: QWidget) -> QWidget:
    instance = reconciler.wrap(element)
    widget = reconciler.mount(instance, container)
    container.rendered = instance

    return widget


def render(element: VirtualNode, container: QWidget):
    try:
        prev_component: WrapperT = container.rendered
    except AttributeError:
        return initial_render(element, container)

    return update_from_root(prev_component, element)


def update_from_root(previous: WrapperT, element: VirtualNode):
    return reconciler.receive(previous, element)


