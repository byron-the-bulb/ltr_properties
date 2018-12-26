import pytest

import ltr_properties

def testPropertyEditorCreate(qtbot):
    editor = ltr_properties.PropertyEditorWidget()
    qtbot.addWidget(editor)
    assert(editor)
