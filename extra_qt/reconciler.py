from typing import Type, Any

from extra_qt.virtual_dom import VirtualNode, TagType

__all__ = ('reconciler',)

WrapperT = Type['WrapperT']
HostNode = Any


class Reconciler:
    host_wrapper_cls: Type['HostWrapper'] = None
    host_node_cls: Any = None

    def configure(self, host_wrapper_cls=None, host_node_cls=None):
        from .renderers.qt_renderer import QWidget, QtDOMWrapper
        self.host_wrapper_cls = host_wrapper_cls or QtDOMWrapper
        self.host_node_cls = host_node_cls or QWidget

    def wrap(self, element) -> WrapperT:
        from extra_qt.renderers.renderer import ComponentWrapper
        if isinstance(element.tag_type, TagType):
            return self.host_wrapper_cls(element)

        return ComponentWrapper(element)

    @staticmethod
    def mount(instance: WrapperT, container: HostNode) -> HostNode:
        return instance.mount(container)

    @staticmethod
    def unmount(instance: WrapperT, container: HostNode = None):
        return instance.unmount(container, container)

    @staticmethod
    def receive(instance: WrapperT, latest: VirtualNode) -> HostNode:
        instance.receive(latest)

    @staticmethod
    def update_if_necessary(instance: WrapperT):
        instance.update_if_necessary()


reconciler = Reconciler()