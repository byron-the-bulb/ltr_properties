from PyQt5.QtGui import QIcon, QPixmap

from pkg_resources import resource_filename

def _LoadIcon(pngName):
    return QIcon(resource_filename(__name__, 'icons/' + pngName + '.png'))

class Icons():
    Add = None
    ArrowDown = None
    ArrowRight = None
    Delete = None
    Goto = None
    Open = None
    Revert = None
    Save = None

    @staticmethod
    def LoadIcons():
        if Icons.ArrowDown:
            return
        
        Icons.Add = _LoadIcon("add")
        Icons.ArrowDown = _LoadIcon("arrowDown")
        Icons.ArrowRight = _LoadIcon("arrowRight")
        Icons.Delete = _LoadIcon("delete")
        Icons.Goto = _LoadIcon("goto")
        Icons.Open = _LoadIcon("open")
        Icons.Revert = _LoadIcon("revert")
        Icons.Save = _LoadIcon("save")
