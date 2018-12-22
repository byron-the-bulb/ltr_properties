import json
import inspect

class Serializer():
    # Recommend that you pass in "sys.modules[__name__]"
    # from some file that has all the classes you care about imported.
    def __init__(self, sysModulesName, postLoadMethod="postLoad"):
        self._encoder = Serializer.__Encoder(indent=2)
        self._decoder = json.JSONDecoder(
            object_hook=lambda jsonObject: Serializer.__decodeObjectHook(jsonObject, sysModulesName, postLoadMethod)
            )

    def decode(self, jsonStr):
        return self._decoder.decode(jsonStr)

    def encode(self, obj):
        return self._encoder.encode(obj)
    
    def load(self, filename):
        with open(filename, 'r') as loadFile:
            return self.decode(loadFile.read())

    def save(self, filename, obj):
        with open(filename, 'w') as saveFile:
            saveFile.write(self.encode(obj))

    class __Encoder(json.JSONEncoder):
        def default(self, o):
            if hasattr(o, "__slots__"):
                contents = {}
                for key in o.__slots__:
                    if key != "__dict__":
                        contents[key] = getattr(o, key)
                return { type(o).__name__ : contents }

    def __decodeObjectHook(jsonObject, nameList, postLoadMethod):
        if len(jsonObject) == 1:
            className = next(iter(jsonObject.keys()))
            classType = Serializer.__getClassType(className, nameList)
            if classType:
                classObj = classType()
                for k, v in jsonObject[className].items():
                    setattr(classObj, k, v)
                if hasattr(classObj, postLoadMethod):
                    getattr(classObj, postLoadMethod)()
                return classObj
        
        return jsonObject

    def __getClassType(className, nameList):
        # See if we find the class in this namespace.
        if hasattr(nameList, className):
            maybeClassType = getattr(nameList, className)
            if inspect.isclass(maybeClassType):
                return maybeClassType

        # Otherwise, recurse into any modules we find.
        for k, v in nameList.__dict__.items():
            if inspect.ismodule(v):
                maybeClassType = Serializer.__getClassType(className, v)
                if maybeClassType:
                    return maybeClassType

        # No dice.
        return None
