from dataclasses import dataclass

from PyQt5.QtCore import QTimer

from extra_qt.component import Component
from extra_qt.renderers.qt_renderer import render_window
from extra_qt.dom.qt_dom import *


@dataclass
class State:
    counter: int = 0

    def update(self):
        self.counter += 5


class ComponentB(Component):
    initial_state_cls = State
    update = Component.updates_state(State.update)

    def render(self):
        return group(dict(title='Inner Component',), [
            label(f'My count is: {self.state.counter}'),
            label(f'My received prop is: {self.props.get("counter")}'),
            button(text='Increment', on_click=self.update),
        ])


class ComponentA(Component):
    initial_state_cls = State
    update = Component.updates_state(State.update)

    def after_mount(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(100)

    def before_unmount(self):
        self.timer.stop()

    def render(self):
        return group(dict(title='Outer Component',), [
            label(f'My count is: {self.state.counter}'),
            ComponentB.c(dict(counter=self.state.counter)),
            ComponentB.c(dict(counter=2 * self.state.counter)),
        ])


def main():
    render_window(create_element(ComponentA))


if __name__ == '__main__':
    main()