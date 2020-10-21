from .CompoundEditor import CompoundEditor
from .Icons import Icons

from .TypeUtils import getDictKVTypeHints

class EditorDict(CompoundEditor):
    canDeleteElements = True

    def _getProperties(self):
        keyHint, valueHint = getDictKVTypeHints(self._typeHint)

        self._isUserEditableDict = self._typeHint and keyHint == str
        
        for name, value in self._targetObject.items():
            keySetter = lambda val, thisName=name: self._setDictKey(thisName, val)
            valueSetter = lambda val, thisName=name: self._setDictValue(thisName, val)
            if self._isUserEditableDict:
                yield name + " Key", name, keySetter, keyHint
                yield name + " Value", value, valueSetter, valueHint
            else:
                yield name, value, valueSetter, valueHint

    def _setDictKey(self, name, val):
        self._targetObject[val] = self._targetObject[name]
        del self._targetObject[name]
        self._createWidgetsForObject()

    def _setDictValue(self, name, val):
        self._targetObject[name] = val

    def _addClicked(self):
        with self._editorGenerator.threadLock():
            keyHint, valueHint = getDictKVTypeHints(self._typeHint)
            keyInteger = 0
            while str(keyInteger) in self._targetObject:
                keyInteger += 1

            self._targetObject[str(keyInteger)] = valueHint()

            self._createWidgetsForObject()
            self.dataChanged.emit(self._targetObject)

    def _deleteClicked(self, name):
        with self._editorGenerator.threadLock():
            if self._isUserEditableDict:
                del self._targetObject[name.replace(" Key", "").replace(" Value", "")]
            else:
                del self._targetObject[name]
            self._createWidgetsForObject()
            self.dataChanged.emit(self._targetObject)

    def _getHeaderWidgets(self):
        addButton = self._editorGenerator.createButton(Icons.Add)
        addButton.clicked.connect(self._addClicked)
        return [addButton]
