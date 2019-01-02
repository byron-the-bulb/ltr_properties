from PyQt5.QtGui import QIcon, QPixmap

from pkg_resources import resource_filename

class Icons():
    ArrowDown = None
    ArrowRight = None
    Delete = None

    @staticmethod
    def LoadIcons():
        if Icons.ArrowDown:
            return
        
        Icons.ArrowDown = QIcon(resource_filename(__name__, 'icons/arrowDown.png'))
        Icons.ArrowRight = QIcon(resource_filename(__name__, 'icons/arrowRight.png'))
        Icons.Delete = QIcon(resource_filename(__name__, 'icons/delete.png'))
