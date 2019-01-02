import typing

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
