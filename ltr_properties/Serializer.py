import json
import os
import typing

from . import TypeUtils
from .Names import Names

class Serializer():
    def __init__(self, root, classDict, indent=None):
        self._root = root
        self._classDict = classDict
        self._encoder = Serializer.__Encoder(indent=indent)
        self._decoder = json.JSONDecoder(object_hook=self._decodeObjectHook)

    def decode(self, jsonStr):
        return self._decoder.decode(jsonStr)

    def encode(self, obj):
        return self._encoder.encode(obj)
    
    def load(self, filename):
        with open(os.path.join(self._root, filename), 'r') as loadFile:
            return self.decode(loadFile.read())

    def root(self):
        return self._root

    def save(self, filename, obj):
        with open(os.path.join(self._root, filename), 'w') as saveFile:
            saveFile.write(self.encode(obj))

    class __Encoder(json.JSONEncoder):
        def default(self, o):
            slots = TypeUtils.getAllSlots(o)

            if slots != None:
                defaultObj = type(o)()

                contents = {}
                for key in slots:
                    if (not key.startswith("_") and hasattr(o, key) and
                        (not hasattr(defaultObj, key) or getattr(o, key) != getattr(defaultObj, key))):
                        contents[key] = getattr(o, key)
                return { type(o).__name__ : contents }

    def _decodeObjectHook(self, jsonObject):
        if len(jsonObject) == 1:
            className = next(iter(jsonObject.keys()))
            if className in self._classDict:
                classType = self._classDict[className]
                typeHints = typing.get_type_hints(classType)
                classObj = classType()
                for k, v in jsonObject[className].items():
                    if k in typeHints:
                        TypeUtils.checkType(v, typeHints[k], className + '.' + k)
                    setattr(classObj, k, v)

                if Names.serializer in classType.__slots__:
                    setattr(classObj, Names.serializer, self)
                if hasattr(classObj, Names.postLoadMethod):
                    getattr(classObj, Names.postLoadMethod)()

                return classObj
        
        return jsonObject
