from typing import Type, Union

from extra_qt.virtual_dom import TagType, VirtualNode

__all__ = (
    'create_element',
    'Label', 'label',
    'Button', 'button',
    'Group', 'group',
    'Tabs', 'tabs',
    'CheckBox', 'check_box',
    'ComboBox', 'combo_box',
    'SpinBox', 'spin_box',
    'LineEdit', 'line_edit',
    'Slider', 'slider',
    'TextEdit', 'text_edit',
    'Dial', 'dial',
)


def create_element(tag_type: Union[TagType, Type['Component']], props=None, children=None) -> VirtualNode:
    if isinstance(props, (list, str)):
        children = props
        props = {}

    if props is None:
        props = dict()

    return VirtualNode(tag_type, props=props, children=children or [])


def _bind_create(tag):
    def _create_element(*args, **kwargs):
        return create_element(tag, *args, **kwargs)

    return _create_element


def _bind_create_input(tag):
    def _create_element(**props):
        return create_element(tag, props=props)

    return _create_element


Label = TagType.LABEL
Button = TagType.BUTTON
Group = TagType.GROUP
Tabs = TagType.TABS
CheckBox = TagType.CHECK_BOX
ComboBox = TagType.COMBO_BOX
SpinBox = TagType.SPIN_BOX
LineEdit = TagType.LINE_EDIT
Dial = TagType.DIAL
Slider = TagType.SLIDER
TextEdit = TagType.TEXT_EDIT

button = _bind_create_input(Button)
group = _bind_create(Group)
tabs = _bind_create(Tabs)
check_box = _bind_create_input(CheckBox)
combo_box = _bind_create_input(ComboBox)
spin_box = _bind_create_input(SpinBox)
line_edit = _bind_create_input(LineEdit)
dial = _bind_create_input(Dial)
slider = _bind_create_input(Slider)
text_edit = _bind_create_input(TextEdit)


def label(text, props=None, children=None):
    props = props or {}
    props['text'] = text
    return create_element(Label, props, [])