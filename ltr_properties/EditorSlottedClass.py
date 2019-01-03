from PyQt5.QtWidgets import QComboBox

from .CompoundEditor import CompoundEditor

from .TypeUtils import getAllSlots

import typing

class EditorSlottedClass(CompoundEditor):
    def _getProperties(self):
        typeHints = typing.get_type_hints(type(self._targetObject))

        for name in getAllSlots(self._targetObject):
            # Let users add hidden properties (including __dict__).
            if name.startswith("_"):
                continue

            value = getattr(self._targetObject, name, None)

            setter = lambda val, thisName=name: setattr(self._targetObject, thisName, val)

            typeHint = typeHints[name] if name in typeHints else None

            if typeHint and value == None:
                value = typeHint()

            yield name, value, setter, typeHint

    def _getHeaderWidgets(self):
        if self._typeHint and len(self._typeHint.__subclasses__()) > 0:
            classSelector = QComboBox()
            for classType in self._getSelectableClasses():
                classSelector.addItem(classType.__name__)

            classSelector.setCurrentText(type(self._targetObject).__name__)

            classSelector.currentTextChanged.connect(self._classSelected)
            return [classSelector]
        else:
            return []

    def _getSelectableClasses(self):
        yield self._typeHint
        for subclass in self._typeHint.__subclasses__():
            yield subclass

    def _classSelected(self, newClassName):
        if newClassName == type(self._targetObject).__name__:
            return
            
        newClass = next(c for c in self._getSelectableClasses() if c.__name__ == newClassName)
        newObject = newClass()
        newSlots = getAllSlots(newObject)
        for oldName in getAllSlots(self._targetObject):
            if oldName in newSlots:
                setattr(newObject, oldName, getattr(self._targetObject, oldName))
        self._targetObject = newObject
        self.dataChanged.emit(newObject)
        self._createWidgetsForObject()

class EditorSlottedClassHorizontal(EditorSlottedClass):
    isHorizontalLayout = True
