from .CompoundEditor import CompoundEditor

class EditorSlottedClass(CompoundEditor):
    def _getProperties(self):
        slots = self._targetObject.__slots__
        if isinstance(slots, str):
            slots = [slots]

        for name in slots:
            # Let users add hidden properties (including __dict__).
            if name.startswith("_"):
                continue

            value = getattr(self._targetObject, name)

            setter = lambda val, thisName=name: setattr(self._targetObject, thisName, val)

            yield name, value, setter

class EditorSlottedClassHorizontal(EditorSlottedClass):
    isHorizontalLayout = True
