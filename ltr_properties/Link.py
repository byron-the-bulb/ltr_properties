from .Names import Names
from typing import TypeVar, Generic

T = TypeVar("T")

#TODO: Avoid infinite recursion by deduping links
class Link(Generic[T]):
    __slots__ = "filename", "_object", Names.serializer
    def __init__(self):
        self._object = None
        self.filename = ""

    def postLoad(self):
        if self.filename and len(self.filename) > 0:
            self._object = getattr(self, Names.serializer).load(self.filename)

    def setObject(self, filename, obj):
        self.filename = filename
        self._object = obj

    def __getattr__(self, name):
        if not name in Link.__slots__ and self._object:
            return getattr(self._object, name)
        if not self._object:
            raise AttributeError("Link[" + str(T) + "] object has not been loaded to retrieve " + name)
        raise AttributeError("Link[" + str(T) + "] object has no attribute " + name)