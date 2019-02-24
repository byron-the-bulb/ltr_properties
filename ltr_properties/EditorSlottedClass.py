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
                if typeHint.__origin__ == typing.Dict:
                    value = {}
                elif typeHint.__origin__ == typing.List:
                    value = []
                else:
                    value = typeHint()

            yield name, value, setter, typeHint

    def _getHeaderWidgets(self):
        if self._typeHint and len(self._typeHint.__subclasses__()) > 0:
            classSelector = QComboBox()
            for classType in self._getSelectableClasses(self._typeHint):
                classSelector.addItem(classType.__name__)

            classSelector.setCurrentText(type(self._targetObject).__name__)

            classSelector.currentTextChanged.connect(self._classSelected)
            return [classSelector]
        else:
            return []

    def _getSelectableClasses(self, typeHint):
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
