import inspect
import json
import os
import sys
import typing

from enum import Enum

from . import TypeUtils
from .Names import Names

from PyQt5.QtWidgets import QMessageBox

class Serializer():
    def __init__(self, root, classDict, indent=None, widgetParent=None):
        self._root = root

        # Allow people to pass in a module and recover from that.
        if inspect.ismodule(classDict):
            classModuleRootFolders = [os.path.dirname(inspect.getfile(classDict)).replace('\\', '/')]
            classDict = TypeUtils.getClasses(classDict, classModuleRootFolders)

        self._classDict = classDict
        self._encoder = Serializer.__Encoder(indent=indent)
        self._decoder = json.JSONDecoder(object_hook=self._decodeObjectHook)

        self._loadStack = []
        self._loadedObjects = {}

        self._widgetParent = widgetParent

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
            path = os.path.join(self._root, filename)
            if os.path.exists(path):
                with open(path, 'r') as loadFile:
                    result = self.decode(loadFile.read())
                    self._loadedObjects[filename] = result
            elif self._widgetParent:
                QMessageBox.warning(self._widgetParent, "Link to missing object", "Cannot find object at path:\n" + path)
                
        return result, self._loadStack.pop()

    def load(self, filename):
        return self.loadWithFileList(filename)[0]

    def root(self):
        return self._root

    def save(self, filename, obj):
        with open(os.path.join(self._root, filename), 'w') as saveFile:
            saveFile.write(self.encode(obj))
        if hasattr(obj, Names.postSaveMethod):
            getattr(obj, Names.postSaveMethod)(self)

    def saveIfLoaded(self, filename):
        if filename in self._loadedObjects:
            self.save(filename, self._loadedObjects[filename])

    class __Encoder(json.JSONEncoder):
        def default(self, o):
            slots = TypeUtils.getAllSlots(o)

            if slots != None:
                defaultObj = type(o)()

                className = type(o).__name__

                typeHints = typing.get_type_hints(type(o))

                contents = {}
                for key in slots:
                    if not key.startswith("_") and hasattr(o, key):
                        defaultValue = None
                        if hasattr(defaultObj, key):
                            defaultValue = getattr(defaultObj, key)
                        else:
                            defaultValue = TypeUtils.instantiateTypeHint(typeHints[key]) if typeHints and key in typeHints else None

                        if not TypeUtils.dataEqual(getattr(o, key), defaultValue):
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

                for k, v in typeHints.items():
                    if not hasattr(classObj, k):
                        setattr(classObj, k, TypeUtils.instantiateTypeHint(v))

                if Names.serializer in classType.__slots__:
                    setattr(classObj, Names.serializer, self)
                if hasattr(classObj, Names.postLoadMethod):
                    getattr(classObj, Names.postLoadMethod)()

                return classObj
        
        return jsonObject

    def _setattrOnObj(self, classObj, k, v, typeHints):
        doDefaultSet = True
        if k in typeHints:
            if sys.version_info[0] == 3 and sys.version_info[1] >= 8:
                #In version 3.8, things like Link[Color] throw on issubclass
                if typing.get_origin(typeHints[k]) == None and issubclass(typeHints[k], Enum):
                    setattr(classObj, k, typeHints[k][v])
                    doDefaultSet = False
            else: # version 3.7 and earlier
                if issubclass(typeHints[k], Enum):
                    setattr(classObj, k, typeHints[k][v])
                    doDefaultSet = False

        if doDefaultSet:
            try:
                setattr(classObj, k, v)
            except:
                if self._widgetParent:
                    QMessageBox.warning(self._widgetParent, "Failed to set property from json data", "Could not find type for: " + k)
