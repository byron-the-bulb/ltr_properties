from PyQt5.QtWidgets import QComboBox

from .CompoundEditor import CompoundEditor
from .TypeUtils import getOptionalTypeHint, getAllSlots, getEditablePropertiesSlottedObject
from enum import Enum

import typing

class EditorOptional(CompoundEditor):
    def __init__(self, editorGenerator, targetObject, name, setter, typeHint):
        self._name = name
        self._setter = setter
        super().__init__(editorGenerator, targetObject, name, typeHint)

    def _getProperties(self):
        if self._targetObject != None:
            if hasattr(self._targetObject, "__slots__"):
                yield from getEditablePropertiesSlottedObject(self._targetObject)
            else:
                yield self._name, self._targetObject, self._setter, getOptionalTypeHint(self._typeHint)

    def _getHeaderWidgets(self):
        classSelector = QComboBox()
        classSelector.addItem("None")
            
        for classType in self._getSelectableClasses(getOptionalTypeHint(self._typeHint)):
            classSelector.addItem(classType.__name__)

        classSelector.setCurrentText(type(self._targetObject).__name__)

        classSelector.currentTextChanged.connect(self._classSelected)
        return [classSelector]

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
            for c in self._getSelectableClasses(getOptionalTypeHint(self._typeHint)):
                if c.__name__ == newClassName:
                    newClass = c

            if newClass == None:
                self._targetObject = None
            else:
                newObject = newClass()
                newSlots = getAllSlots(newObject)
                oldSlots = getAllSlots(self._targetObject)
                if newSlots != None and oldSlots != None:
                    for oldName in oldSlots:
                        if oldName in newSlots and hasattr(self._targetObject, oldName):
                            setattr(newObject, oldName, getattr(self._targetObject, oldName))
                self._targetObject = newObject

            self.dataChanged.emit(self._targetObject)
            self._createWidgetsForObject()
