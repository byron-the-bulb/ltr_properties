from .CompoundEditor import CompoundEditor

class EditorList(CompoundEditor):
    def _getProperties(self, targetObject):
        for i in range(len(targetObject)):
            name = str(i)

            value = targetObject[i]

            setter = lambda val, thisI=i: self._setListElem(targetList, thisI, val)

            yield name, value, setter

    # This is a replacement for this, which isn't valid:
    #  setter = lambda val, thisI=i: targetList[thisI] = val
    def _setListElem(self, targetList, i, val):
        targetList[i] = val

class EditorListHorizontal(EditorList):
    isHorizontalLayout = True
