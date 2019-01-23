import pytest
import sys

import ltr_properties

def testPropertyEditorCreate(qtbot):
    serializer = ltr_properties.Serializer("", sys.modules[__name__])
    editor = ltr_properties.PropertyEditorWidget(serializer)
    qtbot.addWidget(editor)
    assert(editor)
