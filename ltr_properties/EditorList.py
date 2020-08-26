from .CompoundEditor import CompoundEditor
from .Icons import Icons

from .TypeUtils import getListElemTypeHint

import copy

class EditorList(CompoundEditor):
    canDeleteElements = True
    canMoveElements = True

    def _getProperties(self):
        for i in range(len(self._targetObject)):
            name = str(i)

            value = self._targetObject[i]

            setter = lambda val, thisI=i: self._setListElem(thisI, val)

            elemHint = getListElemTypeHint(self._typeHint)

            yield name, value, setter, elemHint

    # This is a replacement for this, which isn't valid:
    #  setter = lambda val, thisI=i: targetObject[thisI] = val
    def _setListElem(self, i, val):
        self._targetObject[i] = val

    def _addClicked(self):
        with self._editorGenerator.threadLock():
            if self._typeHint:
                elemHint = getListElemTypeHint(self._typeHint)
                self._targetObject.append(elemHint())
            else:
                self._targetObject.append(copy.deepcopy(self._targetObject[0]))
            self._createWidgetsForObject()
            self.dataChanged.emit(self._targetObject)

    def _deleteClicked(self, name):
        with self._editorGenerator.threadLock():
            i = int(name)
            del self._targetObject[i]
            self._createWidgetsForObject()
            self.dataChanged.emit(self._targetObject)

    def _moveClicked(self, name, delta):
        with self._editorGenerator.threadLock():
            i = int(name)

            if i + delta < 0 or i + delta >= len(self._targetObject):
                return

            swap = self._targetObject[i + delta]
            self._targetObject[i + delta] = self._targetObject[i]
            self._targetObject[i] = swap
            self._createWidgetsForObject()
            self.dataChanged.emit(self._targetObject)

    def _getHeaderWidgets(self):
        addButton = self._editorGenerator.createButton(Icons.Add)
        addButton.clicked.connect(self._addClicked)
        return [addButton]

class EditorListHorizontal(EditorList):
    isHorizontalLayout = True
