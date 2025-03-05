import typing
import inspect
import os
import sys
from . import Link
from . import VirtualObject
from enum import Enum

def getAllSlots(obj):
    slots = None
    for cls in obj.__class__.__mro__:
        if hasattr(cls, "__slots__"):
            if slots == None:
                slots = []
            theseSlots = getattr(cls,"__slots__")
            if isinstance(theseSlots, str):
                theseSlots = [theseSlots]
                
            for slot in theseSlots:
                if not slot in slots:
                    slots.append(slot)
    return slots

def getEditablePropertiesSlottedObject(obj):
    typeHints = typing.get_type_hints(type(obj))

    for name in getAllSlots(obj):
        # Let users add hidden properties (including __dict__).
        if name.startswith("_"):
            continue

        value = getattr(obj, name, None)

        setter = lambda val, thisName=name: setattr(obj, thisName, val)

        typeHint = typeHints[name] if name in typeHints else None

        if typeHint and value == None:
            value = instantiateTypeHint(typeHint)

        yield name, value, setter, typeHint

def getClasses(module, moduleRootFolders):
    classes = {}
    checkedModules = [module]
    _getClassesRecurse(module, moduleRootFolders, classes, checkedModules)
    classes["Link"] = Link.Link
    classes["VirtualObject"] = VirtualObject.VirtualObject
    return classes

def instantiateTypeHint(typeHint):
    if _typeHintIsDict(typeHint):
        return {}
    elif _typeHintIsList(typeHint):
        return []
    elif _typeHintIsLink(typeHint):
        return typeHint()
    elif typeHintIsOptional(typeHint):
        return None
    elif issubclass(typeHint, Enum):
        return list(typeHint)[0]
    elif "default" in typeHint.__dict__:
        return typeHint.default()
    else:
        return typeHint()

def dataEqual(dataA, dataB):
    if type(dataA) != type(dataB):
        return False
    if hasattr(dataA, "__slots__"):
        for slot in getAllSlots(dataA):
            if not slot.startswith("_") and not dataEqual(getattr(dataA, slot, None), getattr(dataB, slot, None)):
                return False
    elif dataA != dataB:
            return False
    return True 

def _getClassesRecurse(module, moduleRootFolders, classes, checkedModules):
    for k, v in module.__dict__.items():
        if k.startswith("_"):
            continue
        elif inspect.isclass(v):
            if _isModuleOrClassFromRootFolder(v, moduleRootFolders):
                if k in classes and classes[k] != v:
                    raise TypeError("Multiple classes share the name " + k + "\n" + str(v) + "\n" + str(classes[k]))
                classes[k] = v
        elif inspect.ismodule(v) and not v.__name__ in sys.builtin_module_names and not k in checkedModules:
            if _isModuleOrClassFromRootFolder(v, moduleRootFolders):
                checkedModules.append(k)
                _getClassesRecurse(v, moduleRootFolders, classes, checkedModules)

def _isModuleOrClassFromRootFolder(obj, moduleRootFolders):
    try:
        objFile = os.path.abspath(inspect.getfile(obj)).replace('\\', '/')
        for rootFolder in moduleRootFolders:
            if rootFolder in objFile:
                return True
    except:
        pass
    return False

def basicTypeMatches(value, typeHint):
    # Check if the type hint is a generic (e.g., MCPLink[Palette])
    if isinstance(typeHint, typing._GenericAlias):
        # Get the base class (e.g., MCPLink)
        origin = typing.get_origin(typeHint)
        if origin is None:
            origin = typeHint

        # Check if the value is an instance of the base class
        if not isinstance(value, origin):
            return False

        # If there are type parameters (e.g., Palette), validate the linked object
        type_args = typing.get_args(typeHint)
        if type_args and hasattr(value, '_object') and value._object is not None:
            expected_type = type_args[0]  # First type parameter (e.g., Palette)
            return isinstance(value._object, expected_type)
        return True

    # Handle non-generic types (existing logic)
    elif isinstance(value, typeHint):
        return True
    elif typeHint == float and isinstance(value, int):
        return True
    # Add any other special cases from your original function
    return False

def checkType(value, typeHint, path):
    success = True

    if hasattr(typeHint, "checkType"):
        success = typeHint.checkType(value)
    elif _typeHintIsList(typeHint):
        success = _checkTypeList(value, typeHint, path)
    elif _typeHintIsDict(typeHint):
        success = _checkTypeDict(value, typeHint, path)
    elif _typeHintIsLink(typeHint):
        success = _checkTypeLink(value, typeHint, path)
    elif typeHintIsOptional(typeHint):
        success = _checkTypeOptional(value, typeHint, path)
    elif not basicTypeMatches(value, typeHint):
        success = False
    
    if not success:
        raise TypeError(str(type(value)) + " is not type " + str(typeHint) +
            " required for " + path)
    return success

def getDictKVTypeHints(typeHint):
    # key, value
    if typeHint:
        return typeHint.__args__[0], typeHint.__args__[1]
    else:
        return None, None

def getListElemTypeHint(typeHint):
    if typeHint:
        return typeHint.__args__[0]
    else:
        return None

def getLinkTypeHint(typeHint):
    if typeHint:
        return typeHint.__args__[0]
    else:
        return None

def getOptionalTypeHint(typeHint):
    if typeHint:
        return typeHint.__args__[0]
    else:
        return None

def _typeHintIsList(typeHint):
    if sys.version_info[0] == 3 and sys.version_info[1] >= 8:
        return typing.get_origin(typeHint) == list
    else:
        return hasattr(typeHint, "__origin__") and typeHint.__origin__ == typing.List

def _typeHintIsDict(typeHint):
    if sys.version_info[0] == 3 and sys.version_info[1] >= 8:
        return typing.get_origin(typeHint) == dict
    else:
        return hasattr(typeHint, "__origin__") and typeHint.__origin__ == typing.Dict

def _typeHintIsLink(typeHint):
    if sys.version_info[0] == 3 and sys.version_info[1] >= 8:
        return typing.get_origin(typeHint) == Link.Link
    else:
        return hasattr(typeHint, "__origin__") and typeHint.__origin__ == Link.Link

def typeHintIsOptional(typeHint):
    if sys.version_info[0] == 3 and sys.version_info[1] >= 8:
        return typing.get_origin(typeHint) == typing.Union
    else:
        return hasattr(typeHint, "__origin__") and typeHint.__origin__ == typing.Union

def _checkTypeList(value, typeHint, path):
    if type(value) != list:
        return False
    else:
        elementType = getListElemTypeHint(typeHint)
        for i, element in enumerate(value):
            if not checkType(element, elementType, path + "[" + str(i) + "]"):
                return False
    return True

def _checkTypeDict(value, typeHint, path):
    if type(value) != dict:
        return False
    else:
        keyType, valueType = getDictKVTypeHints(typeHint)
        for k, v in value.items():
            if not checkType(k, keyType, path + " key[" + str(k) + "]"):
                return False
            if not checkType(v, valueType, path + "[" + str(k) + "]"):
                return False
    return True

def _checkTypeLink(value, typeHint, path):
    if type(value) != Link.Link:
        return False
    else:
        linkType = getLinkTypeHint(typeHint)
        linkedObject = value._object
        if linkedObject != None and not isinstance(linkedObject, linkType):
            return False
    return True

def _checkTypeOptional(value, typeHint, path):
    if value == None:
        return True

    optionalType = getOptionalTypeHint(typeHint)
    if  not checkType(value, optionalType, path):
        return False

    return True
