import abc
import os

from typing import List

from . import TypeUtils

# This class can be inherited to create objects that let you edit properties across multiple other objects
class VirtualObjectBase(abc.ABC):
    # Should yield relative paths of objects that should be loaded to get properties from.
    @abc.abstractmethod
    def getSourceObjects(self, rootPath):
        pass

    # Should yield name, value, setter, typeHint for each property.
    @abc.abstractmethod
    def getPropertiesFromObject(self, obj):
        pass

    # Save all the referenced objects when saving this. #TODO: only save changed objects.
    def postSave(self, serializer):
        for sourceObjPath in self.getSourceObjects(serializer.root()):
            serializer.saveIfLoaded(sourceObjPath)
    
# This is a default implementation of the VirtualObject concept that will meet many use cases
class VirtualObject(VirtualObjectBase):
    __slots__ = "folders", "properties"
    folders: List[str]
    properties: List[str]
    def __init__(self):
        self.folders = []
        self.properties = []

    def getSourceObjects(self, rootPath):
        for folder in self.folders:
            if len(folder) == 0:
                continue
            for path in os.listdir(os.path.join(rootPath, folder)):
                if path.endswith(".json"):
                    yield os.path.join(folder, path)

    def getPropertiesFromObject(self, obj):
        for name, value, setter, typeHint in TypeUtils.getEditablePropertiesSlottedObject(obj):
            if name in self.properties:
                yield name, value, setter, typeHint
