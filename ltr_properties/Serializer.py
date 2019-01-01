import json
import inspect
import typing

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

            hasSlots = False
            slots = set()
            for cls in o.__class__.__mro__:
                if hasattr(cls, "__slots__"):
                    hasSlots = True
                    theseSlots = getattr(cls,"__slots__")
                    if isinstance(theseSlots, str):
                        slots.update([theseSlots])
                    else:
                        slots.update(theseSlots)

            if hasSlots:
                contents = {}
                for key in slots:
                    if not key.startswith("_"):
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
                classType = Serializer.__getClassType(className, module, checkedModules)
                if classType:
                    typeHints = typing.get_type_hints(classType)
                    classObj = classType()
                    for k, v in jsonObject[className].items():
                        if k in typeHints and not isinstance(v, typeHints[k]):
                            raise TypeError(str(type(v)) + " is not type " + str(typeHints[k]) +
                                " required for " + str(classType) + "." + k)
                        setattr(classObj, k, v)
                    if hasattr(classObj, postLoadMethod):
                        getattr(classObj, postLoadMethod)()
                    return classObj
        
        return jsonObject

    def __getClassType(className, module, checkedModules):
        # See if we find the class in this namespace.
        if hasattr(module, className):
            maybeClassType = getattr(module, className)
            if inspect.isclass(maybeClassType):
                return maybeClassType

        # Otherwise, recurse into any modules we find.
        for k, v in module.__dict__.items():
            if inspect.ismodule(v) and not k.startswith("_") and not k in checkedModules:
                checkedModules.append(k)
                maybeClassType = Serializer.__getClassType(className, v, checkedModules)
                if maybeClassType:
                    return maybeClassType

        # No dice.
        return None
