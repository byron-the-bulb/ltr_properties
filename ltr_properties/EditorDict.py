from .CompoundEditor import CompoundEditor

from .TypeUtils import getDictKVTypeHints

class EditorDict(CompoundEditor):
    def _getProperties(self):
        for name, value in self._targetObject.items():
            setter = lambda val, thisName=name: self._setDictElem(thisName, val)

            keyHint, valueHint = getDictKVTypeHints(self._typeHint)

            yield name, value, setter, valueHint

    # This is a replacement for this, which isn't valid:
    #  setter = lambda val, thisI=i: targetDict[thisName] = val
    def _setDictElem(self, name, val):
        self._targetObject[name] = val
