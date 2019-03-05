import abc
import os

from .TypeUtils import getEditablePropertiesSlottedObject

class VirtualObject(abc.ABC):
    # Should yield relative paths of objects that should be loaded to get properties from.
    @abc.abstractmethod
    def getSourceObjects(self, rootPath):
        pass

    # Should yield name, value, setter, typeHint for each property.
    @abc.abstractmethod
    def getPropertiesFromObject(self, obj):
        pass
    
class VirtualObjectFoldersAndPropertiesByName(VirtualObject):
    def __init__(self, folders, properties):
        self._folders = folders
        self._properties = properties

    def getSourceObjects(self, rootPath):
        for folder in self._folders:
            for path in os.listdir(os.path.join(rootPath, folder)):
                if path.endswith(".json"):
                    yield path

    def getPropertiesFromObject(self, obj):
        for name, value, setter, typeHint in getEditablePropertiesSlottedObject(obj):
            if name in self._properties:
                yield name, value, setter, typeHint
