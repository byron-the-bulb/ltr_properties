import inspect
import json
import os
import typing

from enum import Enum

from . import TypeUtils
from .Names import Names

class Serializer():
    def __init__(self, root, classDict, indent=None):
        self._root = root

        # Allow people to pass in a module and recover from that.
        if inspect.ismodule(classDict):
            classModuleRootFolders = [os.path.dirname(inspect.getfile(classDict))]
            classDict = TypeUtils.getClasses(classDict, classModuleRootFolders)

        self._classDict = classDict
        self._encoder = Serializer.__Encoder(indent=indent)
        self._decoder = json.JSONDecoder(object_hook=self._decodeObjectHook)

        self._loadStack = []
        self._loadedObjects = {}

    def decode(self, jsonStr):
        return self._decoder.decode(jsonStr)

    def encode(self, obj):
        return self._encoder.encode(obj)
    
    # Returns the loaded object, and a list of all filenames that were loaded in the process of loading it
    # (presumably from Link objects). This list can be used to connect signals for other objects changing.
    def loadWithFileList(self, filename):
        # Each stack frame will wind up with the list of all files that were loaded in the process of loading
        # an object. The top of the stack is for the innermost object being loaded.
        for loadStackFrame in self._loadStack:
#            if filename in loadStackFrame:
#                raise Exception("Loop in data: " + filename + " already seen in " + str(loadStackFrame))
            loadStackFrame.append(filename) # Add ourselves to all loading stack frames.
        self._loadStack.append([filename])

        result = None

        if filename in self._loadedObjects:
            result = self._loadedObjects[filename]
        else:
            with open(os.path.join(self._root, filename), 'r') as loadFile:
                result = self.decode(loadFile.read())
                self._loadedObjects[filename] = result
                
        return result, self._loadStack.pop()

    def load(self, filename):
        return self.loadWithFileList(filename)[0]

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

                className = type(o).__name__

                contents = {}
                for key in slots:
                    if (not key.startswith("_") and hasattr(o, key) and
                        (not hasattr(defaultObj, key) or getattr(o, key) != getattr(defaultObj, key))):
                        contents[key] = getattr(o, key)
                    elif (key == Names.saveAsClass):
                        className = getattr(o, key)

                return { className : contents }
            elif isinstance(o, Enum):
                return o.name

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
                    self._setattrOnObj(classObj, k, v, typeHints)

                if Names.serializer in classType.__slots__:
                    setattr(classObj, Names.serializer, self)
                if hasattr(classObj, Names.postLoadMethod):
                    getattr(classObj, Names.postLoadMethod)()

                return classObj
        
        return jsonObject

    def _setattrOnObj(self, classObj, k, v, typeHints):
        if k in typeHints and issubclass(typeHints[k], Enum):
            setattr(classObj, k, typeHints[k][v])
        else:
            setattr(classObj, k, v)
