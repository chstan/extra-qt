from dataclasses import dataclass

from PyQt5.QtCore import QTimer

from extra_qt.component import Component
from extra_qt.renderers.qt_renderer import render_window
from extra_qt.dom.qt_dom import *


@dataclass
class ComponentAState:
    counter: int = 0

    def update(self):
        self.counter += 5


@dataclass
class ComponentBState:
    counter: int = 0

    def update(self):
        self.counter += 1


class ComponentB(Component):
    @classmethod
    def get_initial_state(cls):
        return ComponentBState()

    update = Component.updates_state(ComponentBState.update)

    def render(self):
        return group(dict(title='Inner Component',), [
            label(f'My count is: {self.state.counter}'),
            label(f'My received prop is: {self.props.get("counter")}'),
            button(text='Increment', on_click=self.update),
        ])


class ComponentA(Component):
    @classmethod
    def get_initial_state(cls):
        return ComponentAState()

    def after_mount(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(100)

    def before_unmount(self):
        self.timer.stop()

    update = Component.updates_state(ComponentAState.update)

    def render(self):
        return group(dict(title='Outer Component',), [
            label(f'My count is: {self.state.counter}'),
            ComponentB.c(dict(counter=self.state.counter)),
            ComponentB.c(dict(counter=2 * self.state.counter)),
        ])


def main():
    from extra_qt.reconciler import reconciler
    reconciler.configure()  # Use Qt

    render_window(create_element(ComponentA))
