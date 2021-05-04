import sys
from gui import Pokedex
from PySide2 import QtWidgets


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ui = Pokedex()
    ui.show()
    sys.exit(app.exec_())
