from .CompoundEditor import CompoundEditor

class EditorVirtualObject(CompoundEditor):
    def _getProperties(self):
        serializer = self._editorGenerator.serializer()
        for objPath in self._targetObject.getSourceObjects(serializer.root()):
            obj = serializer.load(objPath)

            yield from self._targetObject.getPropertiesFromObject(obj)
