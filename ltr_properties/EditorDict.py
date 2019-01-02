from .CompoundEditor import CompoundEditor

class EditorDict(CompoundEditor):
    def _getProperties(self, targetObject):
        for name, value in targetObject.items():
            setter = lambda val, thisName=name: self._setDictElem(targetDict, thisName, val)
            yield name, value, setter

    # This is a replacement for this, which isn't valid:
    #  setter = lambda val, thisI=i: targetDict[thisName] = val
    def _setDictElem(self, targetDict, name, val):
        targetDict[name] = val
