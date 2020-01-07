from dataclasses import dataclass, field
from enum import Enum
from typing import List, Any, Dict, Type
import itertools

import typing


@dataclass
class VirtualStyleSettings:
    pass


class TagType(Enum):
    LABEL = 1
    GROUP = 2

    BUTTON = 4

    # partially supported
    TABS = 3

    CHECK_BOX = 5
    COMBO_BOX = 6
    SPIN_BOX = 7

    LINE_EDIT = 8

    DIAL = 9
    SLIDER = 10
    TEXT_EDIT = 11

    # FUTURE, unsupported
    # ========================
    # structural

    # input
    TUMBLER = 12
    FILE_DIALOG = 13


class LayoutType(Enum):
    VERTICAL = 0
    HORIZONTAL = 1
    GRID = 2


ChildrenT = typing.Union['VirtualNode', List['VirtualNode']]


@dataclass
class VirtualNode:
    tag_type: typing.Union[TagType, Type['Component']] = TagType.LABEL
    children: ChildrenT = field(default_factory=list)
    props: Dict[str, Any] = field(default_factory=dict)

    def repr_tree(self):
        return '\n'.join(self.repr_tree_node())

    def repr_tree_node(self) -> List[str]:
        lines = [
            f'{self.tag_type.name if isinstance(self.tag_type, TagType) else self.tag_type.__name__}',
        ]

        def safe_repr_node(node_or_str):
            return node_or_str if isinstance(node_or_str, str) else node_or_str.repr_tree_node()

        if isinstance(self.children, str):
            child_lines = [[self.children]]
        elif isinstance(self.children, list):
            child_lines = [safe_repr_node(child) for child in self.children]
        else:
            child_lines = [[safe_repr_node(self.children)]]

        return lines + ['  ' + l for l in itertools.chain(*child_lines)]
