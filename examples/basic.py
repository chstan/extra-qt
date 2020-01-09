from datetime import datetime

from extra_qt.component import Component
from extra_qt.renderers.qt_renderer import render_window
from extra_qt.dom.qt_dom import group, label, create_element


class MyComponent(Component):
    def render(self):
        return group(dict(title='My Boring Component',), [
            label(f'When I started it was {self.props.get("start_time")}'),
        ])


def main():
    render_window(create_element(MyComponent, dict(start_time=datetime.now().isoformat())))


if __name__ == '__main__':
    main()