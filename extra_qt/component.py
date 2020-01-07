from typing import Dict, Union, Any, Optional, Type

from extra_qt.dom.qt_dom import create_element
from extra_qt.virtual_dom import ChildrenT, VirtualNode


class Component:
    props: Dict[Union[int, str], Any]
    children: ChildrenT

    wrapper: Type['ComponentWrapper'] = None

    initial_state: Optional[Any] = None
    state: Optional[Any] = None

    def __init__(self, props, children):
        self.props = props
        self.children = children

        self.state = self.get_initial_state()

    @classmethod
    def c(cls, *args, **kwargs):
        return create_element(cls, *args, **kwargs)

    @classmethod
    def get_initial_state(cls):
        return cls.initial_state

    @staticmethod
    def updates_state(state_method):
        def perform_set_state(self):
            def call_state_method(s):
                bound_method = getattr(s, state_method.__name__)
                bound_method()
                return s

            self.set_state(call_state_method)

        return perform_set_state

    def set_state(self, latest_state):
        from extra_qt.reconciler import reconciler
        self.wrapper.pending_state.append(latest_state)
        reconciler.update_if_necessary(self.wrapper)

    def render(self) -> VirtualNode:
        raise NotImplementedError()

    def before_receive_props(self, next_props, next_children):
        pass

    def should_update(self, next_props, next_children, next_state):
        return True

    def before_mount(self):
        pass

    def after_mount(self):
        pass

    def before_unmount(self):
        pass

