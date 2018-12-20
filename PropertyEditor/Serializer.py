import json

class Serializer():
    # Recommend that you pass in "sys.modules[__name__]"
    # from some file that has all the classes you care about imported.
    def __init__(self, classList):
        self._encoder = Serializer.__Encoder()
        self._decoder = json.JSONDecoder(object_hook=lambda jsonObject: Serializer.__decodeObjectHook(jsonObject, classList))

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
                    contents[key] = getattr(o, key)
                return { type(o).__name__ : contents }

    # I wish that this was symmetric between encode and decode...
    def __decodeObjectHook(jsonObject, classList):
        if len(jsonObject) == 1:
            className = next(iter(jsonObject.keys()))
            if hasattr(classList, className):
                classType = getattr(classList, className)
                classObj = classType()
                for k, v in jsonObject[className].items():
                    setattr(classObj, k, v)
                return classObj
        
        return jsonObject
