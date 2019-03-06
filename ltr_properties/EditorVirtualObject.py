from .CompoundEditor import CompoundEditor

from .TypeUtils import getEditablePropertiesSlottedObject

class EditorVirtualObject(CompoundEditor):
    def _getProperties(self):
        yield from getEditablePropertiesSlottedObject(self._targetObject)

        serializer = self._editorGenerator.serializer()
        for objPath in self._targetObject.getSourceObjects(serializer.root()):
            obj = serializer.load(objPath)

            valueDict = {}
            setterDict = {}
            for name, value, setter, typeHint in self._targetObject.getPropertiesFromObject(obj):
                valueDict[name] = value
                setterDict[name] = setter

            setter = lambda newValues, thisSetterDict=setterDict: self._setValues(newValues, thisSetterDict)
            
            yield objPath, valueDict, setter, None

    def _setValues(self, newValues, setterDict):
        for key, value in newValues.items():
            setterDict[key](value)
