from .CompoundEditor import CompoundEditor
from .Icons import Icons

class EditorList(CompoundEditor):
    canDeleteElements = True

    def _getProperties(self):
        for i in range(len(self._targetObject)):
            name = str(i)

            value = self._targetObject[i]

            setter = lambda val, thisI=i: self._setListElem(thisI, val)

            yield name, value, setter

    # This is a replacement for this, which isn't valid:
    #  setter = lambda val, thisI=i: targetObject[thisI] = val
    def _setListElem(self, i, val):
        self._targetObject[i] = val

    def _addClicked(self):
        self._targetObject.append(self._targetObject[0])
        self._createWidgetsForObject()
        self.dataChanged.emit(self._targetObject)

    def _deleteClicked(self, name):
        i = int(name)
        del self._targetObject[i]
        self._createWidgetsForObject()
        self.dataChanged.emit(self._targetObject)

    def _getHeaderWidgets(self):
        addButton = self._editorGenerator.createButton(Icons.Add)
        addButton.clicked.connect(self._addClicked)
        return [addButton]

class EditorListHorizontal(EditorList):
    isHorizontalLayout = True
