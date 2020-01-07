from dataclasses import dataclass, field
from enum import Enum
from typing import List, Dict, Callable, Optional, Union, Tuple, Any

from extra_qt import render
from extra_qt.reconciler import reconciler
from extra_qt.virtual_dom import VirtualNode, TagType
from .renderer import HostWrapper, WrapperT

from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QGroupBox, QPushButton, QMainWindow, QApplication, QTabWidget, \
    QCheckBox, QSpinBox, QLineEdit, QDial, QSlider, QTextEdit, QComboBox

__all__ = ('QtDOMWrapper', 'render_window', 'MarkupFormat',)


class MarkupFormat(Enum):
    TEXT = 0
    HTML = 1
    MARKDOWN = 2


def set_style(w: QWidget, style: any):
    if style is not None:
        if not isinstance(style, str):
            w.setStyleSheet(style.to_stylesheet())
        else:
            w.setStyleSheet(style)


def update_style(w: QWidget, previous_style: any, next_style: any):
    if previous_style == next_style:
        return

    set_style(w, next_style or '{}')


def noop(*_, **__):
    pass


def noop_build(cls):
    def builder(_props, _children):
        return cls()

    return builder


def set_widget_style_and_signals(**signal_map: Dict[str, Union[Tuple[Any, str], str]]):
    """
    Example of how signals and slots are treated:

    @set_..._signals(activated=(str, 'on_change')) <->
         widget.activated[str].connect(props['on_change'])

    @set_..._signals(pressed='on_click')) <->
         widget.pressed.connect(props['on_click'])

    with some extra safety. This is also the behavior on the update decorator.
    """
    signal_map: Dict[str, Tuple[Any, str]] = {
        signal_name: (None, slot_name) if isinstance(slot_name, str) else slot_name
        for signal_name, slot_name in signal_map.items()
    }

    def decorate(build):
        if isinstance(build, type):
            build = noop_build(build)

        def wrapped_build(props, children):
            w = build(props, children)
            set_style(w, props.get('style'))

            for signal_name, (arg, handler_name) in signal_map.items():
                if handler_name in props:
                    signal = getattr(w, signal_name)

                    if arg is not None:
                        signal = signal[arg]

                    signal.connect(props[handler_name])

            return w

        return wrapped_build
    return decorate


def update_widget_style_and_signals(**signal_map):
    signal_map = {
        signal_name: (None, slot_name) if isinstance(slot_name, str) else slot_name
        for signal_name, slot_name in signal_map.items()
    }

    def decorate(updater=None):
        if updater is None:
            updater = noop

        def wrapped_update(w: QWidget, previous: VirtualNode, latest: VirtualNode):
            updater(w, previous, latest)
            update_style(w, previous.props.get('style'), latest.props.get('style'))

            for signal_name, (arg, handler_name) in signal_map.items():
                p_handler, l_handler = previous.props.get(handler_name), latest.props.get(handler_name)
                if p_handler != l_handler:
                    signal = getattr(w, signal_name)
                    if arg is not None:
                        signal = signal[arg]

                    if p_handler:
                        signal.disconnect(p_handler)

                    signal.connect(l_handler)

        return wrapped_update

    return decorate


@set_widget_style_and_signals()
def build_label(props, children):
    return QLabel(props.get('text', ''))


@set_widget_style_and_signals()
def build_group(props, children):
    w = QGroupBox(props.get('title', ''))
    w.setLayout(QVBoxLayout())
    return w


@set_widget_style_and_signals(pressed='on_click')
def build_button(props, children):
    return QPushButton(props.get('text', ''))


def build_tabs(props, children):
    w = QTabWidget()

    labels = props.get('labels', [])
    for p in labels:
        tab = QWidget()
        tab.setLayout(QVBoxLayout())
        w.addTab(tab, p)

    selected = props.get('selected')
    if isinstance(selected, str):
        selected = labels.index(selected)

    if selected is not None:
        w.setCurrentIndex(selected)

    return w


@set_widget_style_and_signals(stateChanged='on_change')
def build_check_box(props, children):
    return QCheckBox(props.get('title', ''))


@set_widget_style_and_signals(activated=(str, 'on_change'))
def build_combo_box(props, children):
    w = QComboBox()
    keys = props.get('keys')
    values = props.get('values', [None] * len(keys))

    for k, v in zip(keys, values):
        w.addItem(k, v)

    return w


@set_widget_style_and_signals()
def build_text_edit(props, children):
    w = QTextEdit()
    handler = props.get('on_change')
    format = props.get('format', MarkupFormat.TEXT)

    if handler:
        def wrapped_handler():
            if format == MarkupFormat.TEXT:
                handler(w.toPlainText())
            elif format == MarkupFormat.HTML:
                handler(w.toHtml())
            elif format == MarkupFormat.MARKDOWN:
                handler(w.toMarkdown())

        w.textChanged.connect(wrapped_handler)

    return w


component_tag_map: Dict[TagType, Callable[[], QWidget]] = {
    TagType.LABEL: build_label,
    TagType.GROUP: build_group,
    TagType.BUTTON: build_button,
    TagType.TABS: build_tabs,
    TagType.CHECK_BOX: build_check_box,
    TagType.COMBO_BOX: build_combo_box,
    TagType.SPIN_BOX: set_widget_style_and_signals(valueChanged='on_change')(QSpinBox),
    TagType.LINE_EDIT: set_widget_style_and_signals(textChanged='on_change')(QLineEdit),
    TagType.DIAL: set_widget_style_and_signals(valueChanged='on_change')(QDial),
    TagType.SLIDER: set_widget_style_and_signals(valueChanged='on_change')(QSlider),
    TagType.TEXT_EDIT: build_text_edit,
}


@update_widget_style_and_signals()
def update_label(w: QLabel, previous: VirtualNode, latest: VirtualNode):
    w.setText(latest.props.get('text', ''))


@update_widget_style_and_signals()
def update_group(w: QGroupBox, previous: VirtualNode, latest: VirtualNode):
    w.setTitle(latest.props.get('title', ''))


@update_widget_style_and_signals(pressed='on_click')
def update_button(w: QPushButton, previous: VirtualNode, latest: VirtualNode):
    w.setText(latest.props.get('text', ''))


def update_tabs(w: QTabWidget, previous: VirtualNode, latest: VirtualNode):
    p_selected, l_selected = previous.props.get('selected'), latest.props.get('selected')

    if isinstance(p_selected, str):
        p_selected = previous.props.get('labels', []).index(p_selected)

    if isinstance(l_selected, str):
        l_selected = latest.props.get('labels', []).index(l_selected)

    if p_selected != l_selected:
        if l_selected is not None:
            w.setCurrentIndex(l_selected)


@update_widget_style_and_signals()
def update_text_edit(w: QTextEdit, previous: VirtualNode, latest: VirtualNode):
    """
    We don't use textChanged='on_change' in the signal updater here because in Qt
    QTextEdit.textChanged is just a notifier, it does not get the text.

    If this is not performant enough we will have to deal with implementing refs.
    """
    p_handler, l_handler = previous.props.get('on_change'), latest.props.get('on_change')
    p_format, l_format = previous.props.get('format', MarkupFormat.TEXT), \
                         latest.props.get('format', MarkupFormat.TEXT)
    if p_handler != l_handler or p_format != l_format:
        w.textChanged.disconnect()  # disconnect all because we manage the handler here

        if l_handler is not None:
            def wrapped_handler():
                if l_format == MarkupFormat.TEXT:
                    l_handler(w.plainText)
                elif l_format == MarkupFormat.HTML:
                    l_handler(w.html)
                elif l_format == MarkupFormat.MARKDOWN:
                    l_handler(w.markdown)

            w.textChanged.connect(wrapped_handler)


tag_update_map: Dict[TagType, Callable[[QWidget, VirtualNode], None]] = {
    TagType.LABEL: update_label,
    TagType.GROUP: update_group,
    TagType.BUTTON: update_button,
    TagType.TABS: update_tabs,  # TODO, handle changes in number and order of tabs
    TagType.CHECK_BOX: update_widget_style_and_signals(stateChanged='on_change')(),
    TagType.COMBO_BOX: update_widget_style_and_signals(activated=(str, 'on_change'))(),
    TagType.SPIN_BOX: update_widget_style_and_signals(valueChanged='on_change')(),
    TagType.LINE_EDIT: update_widget_style_and_signals(textChanged='on_change')(),
    TagType.SLIDER: update_widget_style_and_signals(valueChanged='on_change')(),
    TagType.DIAL: update_widget_style_and_signals(valueChanged='on_change')(),
    TagType.TEXT_EDIT: update_text_edit,
}


@dataclass
class QtDOMWrapper(HostWrapper):
    element: VirtualNode

    host_node: QWidget = None
    host_container: QWidget = None
    wrapped_children: List[WrapperT] = field(default_factory=list)

    def receive(self, element: VirtualNode) -> QWidget:
        return self.update(self.element, element)

    def update(self, previous: VirtualNode, latest: VirtualNode) -> QWidget:
        self.update_properties(previous, latest)

        if self.element.tag_type not in {TagType.BUTTON, TagType.LABEL, }:
            self.update_children(previous, latest)

        self.element = latest

        return self.host_node

    def update_properties(self, previous: VirtualNode, latest: VirtualNode):
        tag_update_map[self.element.tag_type](self.host_node, previous, latest)

    def update_children(self, previous: VirtualNode, latest: VirtualNode):
        """
        Update the children for an actual node. This is naive because it does not
        handle moving children that do not need to be unmounted. This will need
        to be revisited once it becomes a problem.

        This also doesn't handle Tabs appropriately at the moment.
        """
        p_children = previous.children
        p_children: List[VirtualNode] = [p_children] if isinstance(p_children, VirtualNode) \
            else p_children
        l_children = latest.children
        l_children: List[VirtualNode] = [l_children] if isinstance(l_children, VirtualNode) \
            else l_children

        new_wrapped_children = []

        for i, child_elem in enumerate(l_children):
            try:
                previous_wrapped_child = self.wrapped_children[i]
            except IndexError:
                new_wrapped_child = reconciler.wrap(child_elem)
                reconciler.mount(new_wrapped_child, self.host_node)
                new_wrapped_children.append(new_wrapped_child)
                continue

            p_child, l_child = p_children[i], l_children[i]
            if p_child.tag_type != l_child.tag_type:
                # completely unmount the tree
                previous_wrapped_child.unmount()
                next_child = reconciler.wrap(l_child)
                reconciler.mount(next_child, self.host_node)
            else:
                reconciler.receive(previous_wrapped_child, l_child)
                new_wrapped_children.append(previous_wrapped_child)

        for stale_child in self.wrapped_children[len(l_children):]:
            reconciler.unmount(stale_child)

        self.wrapped_children = new_wrapped_children

    def set_text_content(self, text: str):
        label: QLabel = self.host_node
        label.setText(text)

    def inflate(self) -> QWidget:
        dom_element = component_tag_map[self.element.tag_type](self.element.props, self.element.children)
        return dom_element

    def unmount(self, container: QWidget = None):
        if container is None:
            container = self.host_container

        for i, wrapper in enumerate(self.wrapped_children):
            if self.element.tag_type == TagType.TABS:
                reconciler.unmount(wrapper, self.host_node.widget(i))
            else:
                reconciler.unmount(wrapper, self.host_node)

        container.layout().removeWidget(self.host_node)

    def mount(self, container: QWidget):
        self.host_container = container

        dom_element = self.inflate()
        container.layout().addWidget(dom_element)
        self.host_node = dom_element

        children = self.element.children
        if not isinstance(children, str):
            children = (children,) if isinstance(children, VirtualNode) else children
            for i, child in enumerate(children):
                wrapper = reconciler.wrap(child)
                self.wrapped_children.append(wrapper)

                if self.element.tag_type == TagType.TABS:
                    reconciler.mount(wrapper, dom_element.widget(i))
                else:
                    reconciler.mount(wrapper, dom_element)

        return dom_element

    @classmethod
    def use_as_renderer(cls):
        from extra_qt import reconciler
        reconciler.host_wrapper_cls = cls
        reconciler.host_node_cls = QWidget


def render_window(element: VirtualNode, window=None, after_show: Optional[Callable[[QMainWindow], None]] = None):
    old_window = window
    window = build_app_window() if window is None else window
    container = window.centralWidget()

    render(element, container)

    if not old_window:
        window.show()

    try:
        after_show(window)
    except TypeError:
        pass

    if not old_window:
        window.app.exec_()


def build_app_window():
    app = QApplication([])
    window = QMainWindow()
    screen_rect = app.primaryScreen().geometry()
    window.move(screen_rect.left(), screen_rect.top())
    window.resize(600, 600)
    w = QWidget()
    w.setLayout(QVBoxLayout())
    window.setCentralWidget(w)
    window.app = app
    return window