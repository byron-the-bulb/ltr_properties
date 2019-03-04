"""ltr_properties - A Qt-based property editor framework"""

from .LtrEditor import LtrEditor
from .Serializer import Serializer
from .PropertyEditorWidget import PropertyEditorWidget
from .ObjectTree import ObjectTree
from .EditorColor import EditorColor
from .EditorSlottedClass import EditorSlottedClassHorizontal
from .Link import Link
from .UIUtils import clearLayout
from .TypeUtils import getDictKVTypeHints, getLinkTypeHint, getListElemTypeHint

__version__ = '0.1.0'
__author__ = 'Bill Clark <bill@skythievesgame.com>'
__all__ = []
