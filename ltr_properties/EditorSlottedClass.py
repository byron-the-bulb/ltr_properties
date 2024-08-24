from PyQt5.QtWidgets import QComboBox
from PyQt5.QtCore import Qt, QEvent

from .CompoundEditor import CompoundEditor
from .TypeUtils import getAllSlots, getEditablePropertiesSlottedObject
from enum import Enum

import typing

class ClassSelector(QComboBox):
    def __init__(self):
        super().__init__()        
        self.setFocusPolicy(Qt.StrongFocus)
        self.installEventFilter(self)
            
    def eventFilter(self, obj, event):
        if event.type() == QEvent.Wheel:
            return True
        return False

class EditorSlottedClass(CompoundEditor):
    def _getProperties(self):
        return getEditablePropertiesSlottedObject(self._targetObject)

    def _getHeaderWidgets(self):
        if self._typeHint and len(self._typeHint.__subclasses__()) > 0:
            classSelector = ClassSelector()
            for classType in self._getSelectableClasses(self._typeHint):
                classSelector.addItem(classType.__name__)

            classSelector.setCurrentText(type(self._targetObject).__name__)

            classSelector.currentTextChanged.connect(self._classSelected)
            return [classSelector]
        else:
            return []

    def _getSelectableClasses(self, typeHint):
        if not getattr(typeHint, "__abstractmethods__", False):
            yield typeHint
        for subclass in typeHint.__subclasses__():
            yield from self._getSelectableClasses(subclass)

    def _classSelected(self, newClassName):
        if newClassName == type(self._targetObject).__name__:
            return

        with self._editorGenerator.threadLock():
            newClass = None
            for c in self._getSelectableClasses(self._typeHint):
                if c.__name__ == newClassName:
                    newClass = c

            newObject = newClass()
            newSlots = getAllSlots(newObject)
            for oldName in getAllSlots(self._targetObject):
                if oldName in newSlots and hasattr(self._targetObject, oldName):
                    setattr(newObject, oldName, getattr(self._targetObject, oldName))
            self._targetObject = newObject
            self.dataChanged.emit(newObject)
            self._createWidgetsForObject()

class EditorSlottedClassHorizontal(EditorSlottedClass):
    isHorizontalLayout = True
