from pokeApi import get_pokemon, get_flavor_text, get_sprite_url
from PIL import Image
from PySide2 import QtWidgets, QtCore, QtGui

import requests
import os
import urllib3
import csv
import io

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class Pokedex(QtWidgets.QDialog):
    def __init__(self):
        super(Pokedex, self).__init__()
        self.setWindowTitle("pokedex UI")
        self.setStyleSheet("background-color: red")
        self.setWindowIcon(QtGui.QIcon('icon2.jpg'))
        self.setFixedSize(340, 420)
        self.setWindowTitle("Pokedex V2")
        self.setWindowFlags(self.windowFlags()
                    ^ QtCore.Qt.WindowContextHelpButtonHint)
        self.index_arr = []
        self.label = QtWidgets.QLabel()
        self.label.setScaledContents(True)
        self.label.setFixedSize(140, 140)
        self.names = self.get_names()
        self.checkboxes = []
        self.buildUI()

    def buildUI(self):
        """
        Desc: Builds User Interface 
        Return:
            None
        """
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
        # Adding in checkbox per pokemon Name
        for index, name in enumerate(self.names):
            box_name = "{}. {}".format(index, name)
            self.add_checkbox(box_name)
        # Putting the checkbox inside ScrollArea
        self.scroll_area.setWidget(checkBoxWidget)

        clearWidget = QtWidgets.QWidget()
        clearLayout = QtWidgets.QVBoxLayout(clearWidget)
        self.clearBtn = QtWidgets.QPushButton("Clear All")
        layout.addWidget(clearWidget)
        clearLayout.addWidget(self.clearBtn)
        self.clearBtn.clicked.connect(self.set_all_unchecked)


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

        # Creating the button for export of Sprite and CSV
        dwnld_Btn = QtWidgets.QPushButton("Download CSV")
        dwnld_Btn.setStyleSheet("background-color: white")
        dwnldS_Btn = QtWidgets.QPushButton("Download Sprite")
        dwnldS_Btn.setStyleSheet("background-color: white")
        layout.addWidget(saveWidget)
        saveLayout.addWidget(dwnld_Btn)
        saveLayout.addWidget(dwnldS_Btn)
        # connecting the button functionality.
        dwnldS_Btn.clicked.connect(self.download_sprite)
        dwnld_Btn.clicked.connect(self.download_csv)
        return None

    def set_all_unchecked(self):
        """
        Desc: Set all checkboxes to uncheck
        Return:
            None
        """
        for checkbox in self.checkboxes:
            if checkbox.isChecked():
                checkbox.setChecked(False)
                self.index_arr = []
                self.old_state = []
        return None

    def set_flavor_text(self, name):
        """
        Desc: Obtains the requested flavor text for Pokemon
        Args:
            name: name of selected pokemon
        Return:
            None
        """
        self.text_field.setReadOnly(True)
        self.text_field.setText(get_flavor_text(name))
        return None

    def download_csv(self):
        """
        Desc: This function downloads the csv into a folder of choice
        Return:
            None
        """
        # creating a QFileDialog for filebrowser export
        Save_pref = "Python Files (*.csv)"
        file_name = QtWidgets.QFileDialog.getSaveFileName(self,
                                                          'Save File',
                                                          Save_pref)
        # adding data to a dictionary and list for export
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
        # Exporting file as csv
        with open(file_name[0], "w") as csvfile:
            writer = csv.DictWriter(csvfile,
                                    fieldnames=csv_columns)
            writer.writeheader()
            for data in data_list:
                writer.writerow(data)
            return None

    def download_sprite(self):
        """
        Desc: Opens FileBrowser for download of pokemon 
        Return:
            None
        """
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
        """
        Desc: add checkBox Widget to Layout per name
        Args:
            name: pokemon name
        Return:
            None
        """
        checkbox = QtWidgets.QCheckBox(name)
        checkbox.stateChanged.connect(self.set_image)
        self.checkboxLayout.addWidget(checkbox)
        self.checkboxes.append(checkbox)
        return None

    def set_image(self, state):
        """
        Desc: check state, and change image and flav_text of pokemon
        Args:
            state: current state of checkbox
        Return:
            None
        """
        image = QtGui.QImage()
        if state == QtCore.Qt.Checked:
            self.old_state = []
            for index, checkbox in enumerate(self.checkboxes):
                if checkbox.isChecked():
                    self.old_state.append(index)
                    if index not in self.index_arr:
                        self.index_arr.append(index)
            self.set_flavor_text(self.names[self.index_arr[-1]])
            sprite_url = get_sprite_url(self.names[self.index_arr[-1]])
            image.loadFromData(requests.get(sprite_url).content)
            self.img = QtGui.QPixmap(image)

            self.label.setPixmap(self.img)
        return None

    def get_names(self):
        """
        Desc: obtains  the names all pokemon
        Return:
            names
        """
        data = get_pokemon()
        n_names = len(data)
        names = []
        for index in range(n_names):
            names.append(data[index]["name"])
        return names
