from .CompoundEditor import CompoundEditor

import typing

class EditorSlottedClass(CompoundEditor):
    def _getProperties(self):
        slots = self._targetObject.__slots__
        if isinstance(slots, str):
            slots = [slots]

        typeHints = typing.get_type_hints(type(self._targetObject))

        for name in slots:
            # Let users add hidden properties (including __dict__).
            if name.startswith("_"):
                continue

            value = getattr(self._targetObject, name)

            setter = lambda val, thisName=name: setattr(self._targetObject, thisName, val)

            typeHint = typeHints[name] if name in typeHints else None

            yield name, value, setter, typeHint

class EditorSlottedClassHorizontal(EditorSlottedClass):
    isHorizontalLayout = True
