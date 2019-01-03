import typing
import inspect

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

def getClassType(className, module, checkedModules):
    # See if we find the class in this namespace.
    if hasattr(module, className):
        maybeClassType = getattr(module, className)
        if inspect.isclass(maybeClassType):
            return maybeClassType

    # Otherwise, recurse into any modules we find.
    for k, v in module.__dict__.items():
        if inspect.ismodule(v) and not k.startswith("_") and not k in checkedModules:
            checkedModules.append(k)
            maybeClassType = getClassType(className, v, checkedModules)
            if maybeClassType:
                return maybeClassType

    # No dice.
    return None

def checkType(value, typeHint, path):
    success = True
    if hasattr(typeHint, "__origin__"):
        if typeHint.__origin__ == typing.List:
            success = _checkTypeList(value, typeHint)
        elif typeHint.__origin__ == typing.Dict:
            success = _checkTypeDict(value, typeHint)
        else:
            raise NotImplementedError("Type checking not implemented for " + str(typeHint))
    elif not isinstance(value, typeHint):
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

def _checkTypeList(value, typeHint):
    if type(value) != list:
        return False
    else:
        elementType = getListElemTypeHint(typeHint)
        for element in value:
            if not isinstance(element, elementType):
                return False
    return True

def _checkTypeDict(value, typeHint):
    if type(value) != dict:
        return False
    else:
        keyType, valueType = getDictKVTypeHints(typeHint)
        for k, v in value.items():
            if not isinstance(k, keyType):
                return False
            if not isinstance(v, valueType):
                return False
    return True
