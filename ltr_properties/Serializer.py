import json
import typing

from . import TypeUtils
from .Names import Names

class Serializer():
    def decode(jsonStr, module=None):
        decoder = json.JSONDecoder(
            object_hook=lambda jsonObject: Serializer.__decodeObjectHook(jsonObject, module)
            )
        return decoder.decode(jsonStr)

    def encode(obj, indent=None):
        encoder = Serializer.__Encoder(indent=indent)
        return encoder.encode(obj)
    
    def load(filename, module):
        with open(filename, 'r') as loadFile:
            return Serializer.decode(loadFile.read(), module)

    def save(filename, obj, indent=None):
        with open(filename, 'w') as saveFile:
            saveFile.write(Serializer.encode(obj, indent))

    class __Encoder(json.JSONEncoder):
        def default(self, o):
            slots = TypeUtils.getAllSlots(o)

            if slots != None:
                contents = {}
                for key in slots:
                    if not key.startswith("_") and hasattr(o, key):
                        contents[key] = getattr(o, key)
                return { type(o).__name__ : contents }

    def __decodeObjectHook(jsonObject, module):
        if len(jsonObject) == 1:
            className = next(iter(jsonObject.keys()))
            if module:
                checkedModules = []
                classType = TypeUtils.getClassType(className, module, checkedModules)
                if classType:
                    typeHints = typing.get_type_hints(classType)
                    classObj = classType()
                    for k, v in jsonObject[className].items():
                        if k in typeHints:
                            TypeUtils.checkType(v, typeHints[k], className + '.' + k)
                        setattr(classObj, k, v)

                    if Names.loadModule in classType.__slots__:
                        setattr(classObj, Names.loadModule, module)
                    if hasattr(classObj, Names.postLoadMethod):
                        getattr(classObj, Names.postLoadMethod)()

                    return classObj
        
        return jsonObject
