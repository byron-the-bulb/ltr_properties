def clearLayout(layout):
    for i in reversed(range(layout.count())): 
        item = layout.takeAt(i)
        widget = item.widget()
        if widget:
            widget.deleteLater()
        elif hasattr(item, "count"): # QLayout?
            clearLayout(item)
        else: # QSpacerItem?
            pass