from pokeApi import get_pokemon, get_flavor_text, get_sprite_url
from PIL import Image
from PyQt5 import QtWidgets, QtCore, QtGui

import requests
import os
import urllib3
import csv
import io
import sys

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class Pokedex(QtWidgets.QDialog):
    def __init__(self):
        super(Pokedex, self).__init__()
        self.setWindowTitle("pokedex UI")
        self.setStyleSheet("background-color: red")
        self.setWindowIcon(QtGui.QIcon('icon2.jpg'))
        self.setFixedSize(330, 420)
        self.setWindowTitle("Pokedex V2")
        self.setWindowFlags(self.windowFlags()
                    ^ QtCore.Qt.WindowContextHelpButtonHint)
        self.index_arr = []
        self.label = QtWidgets.QLabel()
        self.label.setScaledContents(True)
        self.label.setFixedSize(150, 150)
        self.names = self.get_names()
        self.checkboxes = []
        self.buildUI()

    def buildUI(self):
        # Creating a VerticleBox Layout initially
        layout = QtWidgets.QVBoxLayout(self)

        # Adding in a image widget to display sprites
        imageWidget = QtWidgets.QWidget()
        imageLayout = QtWidgets.QHBoxLayout(imageWidget)
        # Adding the imageWidget to layout
        layout.addWidget(imageWidget)
        imageLayout.addWidget(self.label)

        # Adding in the checkboxLayout
        scrollWidget = QtWidgets.QWidget()
        # creating the scrollArea
        self.scroll_area = QtWidgets.QScrollArea()
        # creating the verticle layout for the scroll Area
        self.scrollLayout = QtWidgets.QVBoxLayout(scrollWidget)
        # Turning VerticleBar Policy to On
        self.scroll_area.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        # Turn off the Horizontal Policy
        self.scroll_area.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.scroll_area.setWidgetResizable(True)
        # Changing the BG to become white
        self.scroll_area.setStyleSheet("background-color: white")
        # Adding the scroll Widget to Image Layout
        imageLayout.addWidget(scrollWidget)
        self.scrollLayout.addWidget(self.scroll_area)

        checkBoxWidget = QtWidgets.QWidget()
        self.checkboxLayout = QtWidgets.QVBoxLayout(checkBoxWidget)
        self.scrollLayout.addWidget(checkBoxWidget)
        for i in self.names:
            self.add_checkbox(i)
        self.scroll_area.setWidget(checkBoxWidget)

        # Adding in text Field widget to display flavor text
        textWidget = QtWidgets.QWidget()
        textLayout = QtWidgets.QHBoxLayout(textWidget)
        self.text_field = QtWidgets.QTextEdit()
        # Creating a fixed size for the text area
        self.text_field.setFixedSize(290, 100)
        self.text_field.setStyleSheet("background-color: white")
        # adding it to the layout
        textLayout.addWidget(self.text_field)
        layout.addWidget(textWidget)

        # Creating save widgets to save sprite and csv data
        saveWidget = QtWidgets.QWidget()
        saveLayout = QtWidgets.QHBoxLayout(saveWidget)

        dwnld_Btn = QtWidgets.QPushButton("Download CSV")
        dwnld_Btn.setStyleSheet("background-color: white")
        dwnldS_Btn = QtWidgets.QPushButton("Download Sprite")
        dwnldS_Btn.setStyleSheet("background-color: white")
        layout.addWidget(saveWidget)
        saveLayout.addWidget(dwnld_Btn)
        saveLayout.addWidget(dwnldS_Btn)
        dwnldS_Btn.clicked.connect(self.download_sprite)
        dwnld_Btn.clicked.connect(self.download_csv)
        return None

    def get_flavor_text(self, name):
        self.text_field.setReadOnly(True)
        self.text_field.setWordWrapMode(True)
        self.text_field.setText(get_flavor_text(name))
        return None

    def download_csv(self):
        Save_pref = "Python Files (*.csv)"
        file_name = QtWidgets.QFileDialog.getSaveFileName(self,
                                                          'Save File',
                                                          Save_pref)
        data_list = []
        for index in self.index_arr:
            data_dict = dict({})
            data_dict["name"] = self.names[index]
            data_dict["index"] = index
            data_dict["flavor_text"] = get_flavor_text(self.names[index])
            data_list.append(data_dict)
        csv_columns = ["name",
                       "index",
                       "flavor_text"]
        with open(file_name[0], "w") as csvfile:
            writer = csv.DictWriter(csvfile,
                                    fieldnames=csv_columns)
            writer.writeheader()
            for data in data_list:
                writer.writerow(data)
            return None

    def download_sprite(self):
        SEL_DIR = "Select Directory"
        file_name = QtWidgets.QFileDialog.getExistingDirectory(self,
                                                               SEL_DIR)
        for index in self.index_arr:
            directory = os.path.join(file_name, self.names[index])
            sprite_url = get_sprite_url(self.names[index])
            image = requests.get(sprite_url).content
            image = Image.open(io.BytesIO(image))
            image.save(directory+".png", format="png")
        return None

    def add_checkbox(self, name):
        checkbox = QtWidgets.QCheckBox(name)
        checkbox.stateChanged.connect(self.set_image)
        self.checkboxLayout.addWidget(checkbox)
        self.checkboxes.append(checkbox)
        return None

    def set_image(self, state):
        image = QtGui.QImage()
        if state == QtCore.Qt.Checked:
            self.old_state = []
            for index, checkbox in enumerate(self.checkboxes):
                if checkbox.isChecked():
                    self.old_state.append(index)
                    if index not in self.index_arr:
                        self.index_arr.append(index)
            self.get_flavor_text(self.names[self.index_arr[-1]])
            sprite_url = get_sprite_url(self.names[self.index_arr[-1]])
            image.loadFromData(requests.get(sprite_url).content)
            self.img = QtGui.QPixmap(image)

            self.label.setPixmap(self.img)
        return None

    def get_names(self):
        data = get_pokemon()
        n_names = len(data)
        names = []
        for index in range(n_names):
            names.append(data[index]["name"])
        return names


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ui = Pokedex()
    ui.show()
    sys.exit(app.exec_())
