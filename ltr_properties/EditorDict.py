from .CompoundEditor import CompoundEditor

class EditorDict(CompoundEditor):
    def _getProperties(self):
        for name, value in self._targetObject.items():
            setter = lambda val, thisName=name: self._setDictElem(thisName, val)
            yield name, value, setter

    # This is a replacement for this, which isn't valid:
    #  setter = lambda val, thisI=i: targetDict[thisName] = val
    def _setDictElem(self, name, val):
        self._targetObject[name] = val
