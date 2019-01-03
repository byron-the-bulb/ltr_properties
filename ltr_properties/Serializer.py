import json
import typing

from .TypeUtils import checkType, getClassType, getAllSlots

class Serializer():
    fromFile = "_fromFile"
    def decode(jsonStr, module=None, postLoadMethod="postLoad"):
        decoder = json.JSONDecoder(
            object_hook=lambda jsonObject: Serializer.__decodeObjectHook(jsonObject, module, postLoadMethod)
            )
        return decoder.decode(jsonStr)

    def encode(obj, indent=None):
        encoder = Serializer.__Encoder(indent=indent)
        return encoder.encode(obj)
    
    def load(filename, module, postLoadMethod="postLoad"):
        with open(filename, 'r') as loadFile:
            return Serializer.decode(loadFile.read(), module, postLoadMethod)

    def save(filename, obj, indent=None):
        with open(filename, 'w') as saveFile:
            saveFile.write(Serializer.encode(obj, indent))

    class __Encoder(json.JSONEncoder):
        def default(self, o):
            if hasattr(o, Serializer.fromFile):
                return { Serializer.fromFile: getattr(o, Serializer.fromFile) }

            slots = getAllSlots(o)

            if slots != None:
                contents = {}
                for key in slots:
                    if not key.startswith("_") and hasattr(o, key):
                        contents[key] = getattr(o, key)
                return { type(o).__name__ : contents }

    def __decodeObjectHook(jsonObject, module, postLoadMethod):
        if len(jsonObject) == 1:
            className = next(iter(jsonObject.keys()))
            if className == Serializer.fromFile:
                filename = jsonObject[className]
                loadedObj = Serializer.load(filename, module, postLoadMethod)
                setattr(loadedObj, Serializer.fromFile, filename)
                return loadedObj
            elif module:
                checkedModules = []
                classType = getClassType(className, module, checkedModules)
                if classType:
                    typeHints = typing.get_type_hints(classType)
                    classObj = classType()
                    for k, v in jsonObject[className].items():
                        if k in typeHints:
                            checkType(v, typeHints[k], className + '.' + k)
                        setattr(classObj, k, v)
                    if hasattr(classObj, postLoadMethod):
                        getattr(classObj, postLoadMethod)()
                    return classObj
        
        return jsonObject
