import pytest
import sys

import ltr_properties

class Foo:
    __slots__ = "a", "b", "c"
    def __eq__(self, item):
        return slotsEqual(self, item)

class Bar:
    __slots__ = "a", "b"
    def postLoad(self):
        self.a = self.a + 1
        self.b = self.b + " addition"

def roundTripSerialize(obj):
    serialized = ltr_properties.Serializer.encode(obj)
    deserialized = ltr_properties.Serializer.decode(serialized, sys.modules[__name__])
    assert(deserialized == obj)

def slotsEqual(objA, objB):
    assert(objA.__slots__ == objB.__slots__)
    for slot in objA.__slots__:
        assert(getattr(objA, slot) == getattr(objB, slot))
    return True

def testSerializeBasics():
    roundTripSerialize(True)
    roundTripSerialize(1234)
    roundTripSerialize(-25.75)
    roundTripSerialize("Test string")

def testSerializeList():
    roundTripSerialize([1, 2, 3, 4, 5])

def testSerializeDict():
    roundTripSerialize({"a": 1, "b": True, "c": "Test"})

def testSerializeClass():
    foo = Foo()
    foo.a = 1
    foo.b = 4
    foo.c = 9
    roundTripSerialize(foo)

def testSerializePostLoad():
    bar = Bar()
    bar.a = 5
    bar.b = "Test"
    serialized = ltr_properties.Serializer.encode(bar)
    deserialized = ltr_properties.Serializer.decode(serialized, sys.modules[__name__])
    assert(deserialized.a == bar.a + 1)
    assert(deserialized.b == bar.b + " addition")
