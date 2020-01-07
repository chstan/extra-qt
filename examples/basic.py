from dataclasses import dataclass

from PyQt5.QtCore import QTimer

from extra_qt import Component
from extra_qt.dom.qt_dom import *
from extra_qt.renderers.qt_renderer import render_window


@dataclass
class SimpleComponentState:
    counter: int = 0
    color: str = 'red'
    functions_swapped: bool = False

    def increment(self):
        self.counter += 1

    def double(self):
        self.counter *= 2

    def swap(self):
        self.functions_swapped = not self.functions_swapped

    def reset(self):
        self.counter = 0
        self.color = 'red'


class SimpleComponent(Component):
    @classmethod
    def get_initial_state(cls):
        return SimpleComponentState()

    def after_mount(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.increment)
        self.timer.start(100)

    def before_unmount(self):
        self.timer.stop()

    increment = Component.updates_state(SimpleComponentState.increment)
    double = Component.updates_state(SimpleComponentState.double)
    reset = Component.updates_state(SimpleComponentState.reset)
    swap = Component.updates_state(SimpleComponentState.swap)

    def print(self, *args, **kwargs):
        print('!', *args, **kwargs)

    def render(self):
        first_set = group(dict(title='Grouped',), [
            button(text='Double', on_click=self.reset if self.state.functions_swapped else self.double),
            button(text='Zero', on_click=self.double if self.state.functions_swapped else self.reset),
            button(text='Swap', on_click=self.swap),
            *self.children,
            label(str(self.state.counter), dict(style=f'color: {self.state.color};')),
            label('Full State: ' + str(self.state)),

            check_box(on_change=self.print),
            spin_box(on_change=self.print),
            combo_box(keys=['A', 'B'], values=[1, 2], on_change=self.print),
            line_edit(on_change=self.print),
            dial(on_change=self.print),
            slider(on_change=self.print),
            text_edit(on_change=self.print),
        ])

        return tabs(
            props=dict(labels=['A', 'B'], selected='A'),
            children=[
                first_set,
                label(f'I am also a tab! {self.state.counter % 2}'),
            ],
        )


def main():
    from extra_qt.reconciler import reconciler
    reconciler.configure()  # Use Qt

    render_window(create_element(SimpleComponent, children=[label('a')]))
