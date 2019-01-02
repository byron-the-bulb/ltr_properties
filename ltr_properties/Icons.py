from PyQt5.QtGui import QIcon, QPixmap

from pkg_resources import resource_filename

def _LoadIcon(pngName):
    return QIcon(resource_filename(__name__, 'icons/' + pngName + '.png'))

class Icons():
    Add = None
    ArrowDown = None
    ArrowRight = None
    Delete = None

    @staticmethod
    def LoadIcons():
        if Icons.ArrowDown:
            return
        
        Icons.Add = _LoadIcon("add")
        Icons.ArrowDown = _LoadIcon("arrowDown")
        Icons.ArrowRight = _LoadIcon("arrowRight")
        Icons.Delete = _LoadIcon("delete")
