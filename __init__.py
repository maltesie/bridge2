from PySide2.QtCore import Qt, QCoreApplication
from PySide2.QtWidgets import QApplication
from .bridge import MainWindow
import sys

def __init_plugin__(app=None):
    from pymol.plugins import addmenuitemqt
    addmenuitemqt('Bridge', run_plugin_gui)

def run_plugin_gui():
    QCoreApplication.setAttribute(Qt.AA_ShareOpenGLContexts)
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
