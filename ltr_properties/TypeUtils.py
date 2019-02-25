import typing
import inspect
from . import Link
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

def getClasses(module, moduleRootFolders):
    classes = {"Link": Link.Link}
    checkedModules = [module]
    _getClassesRecurse(module, moduleRootFolders, classes, checkedModules)
    return classes

def _getClassesRecurse(module, moduleRootFolders, classes, checkedModules):
    for k, v in module.__dict__.items():
        if k.startswith("_"):
            continue
        elif inspect.isclass(v):
            if _isModuleOrClassFromRootFolder(v, moduleRootFolders):
                if k in classes and classes[k] != v:
                    raise TypeError("Multiple classes share the name " + k + "\n" + str(v) + "\n" + str(classes[k]))
                classes[k] = v
        elif inspect.ismodule(v) and not k in checkedModules:
            if _isModuleOrClassFromRootFolder(v, moduleRootFolders):
                checkedModules.append(k)
                _getClassesRecurse(v, moduleRootFolders, classes, checkedModules)

def _isModuleOrClassFromRootFolder(obj, moduleRootFolders):
    try:
        objFile = inspect.getfile(obj)
        for rootFolder in moduleRootFolders:
            if rootFolder in objFile:
                return True
    except:
        pass
    return False

def basicTypeMatches(value, typeHint):
    if isinstance(value, typeHint):
        return True
    elif typeHint == float and isinstance(value, int):
        return True
    elif issubclass(typeHint, Enum) and isinstance(value, str):
        return True
    return False

def checkType(value, typeHint, path):
    success = True
    if hasattr(typeHint, "__origin__"):
        if typeHint.__origin__ == typing.List:
            success = _checkTypeList(value, typeHint)
        elif typeHint.__origin__ == typing.Dict:
            success = _checkTypeDict(value, typeHint)
        elif typeHint.__origin__ == Link.Link:
            success = _checkTypeLink(value, typeHint)
        else:
            raise NotImplementedError("Type checking not implemented for " + str(typeHint))
    elif not basicTypeMatches(value, typeHint):
        success = False
    
    if not success:
        raise TypeError(str(type(value)) + " is not type " + str(typeHint) +
            " required for " + path)

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

def _checkTypeList(value, typeHint):
    if type(value) != list:
        return False
    else:
        elementType = getListElemTypeHint(typeHint)
        for element in value:
            if not basicTypeMatches(element, elementType):
                return False
    return True

def _checkTypeDict(value, typeHint):
    if type(value) != dict:
        return False
    else:
        keyType, valueType = getDictKVTypeHints(typeHint)
        for k, v in value.items():
            if not basicTypeMatches(k, keyType):
                return False
            if not basicTypeMatches(v, valueType):
                return False
    return True

def _checkTypeLink(value, typeHint):
    if type(value) != Link.Link:
        return False
    else:
        linkType = getLinkTypeHint(typeHint)
        linkedObject = value._object
        if linkedObject != None and not isinstance(linkedObject, linkType):
            return False
    return True
