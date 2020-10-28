import sys
import os
import image_browser
import time
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QFileDialog, QVBoxLayout
from PyQt5.QtGui import QPixmap, QKeyEvent
from PyQt5.Qt import Qt
from PyQt5.QtCore import QCoreApplication
from PyQt5 import QtWidgets, QtCore
from PIL.ImageQt import ImageQt


class MainApp(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.key_pressed = False

        self.init_ui()

    def init_ui(self) -> None:
        """
        Initialize user interface, open prompt dialog

        :return: None
        """
        self.select_dir_button = QPushButton("Select directory", self)
        self.select_dir_button.setToolTip("Select directory")
        self.select_dir_button.clicked.connect(self.open_directory_browser)

        self.select_file_button = QPushButton("Select file", self)
        self.select_file_button.setToolTip("Select file")
        self.select_file_button.clicked.connect(self.open_file_browser)

        self.layout.addWidget(self.select_dir_button)
        self.layout.addWidget(self.select_file_button)
        self.setLayout(self.layout)

        QtWidgets.qApp.installEventFilter(self)

        self.show()

    def open_file_browser(self) -> None:
        """
        Open file selection dialog

        :return: None
        """
        #  path = os.getcwd()
        path = "/home/bazyli/projects/dataset_leukocytes/annotations_test"
        file_name, _ = QFileDialog.getOpenFileName(self, "Select file", path)
        self.process_annotations_file(file_name)

    def open_directory_browser(self) -> None:
        """
        Open directory selection dialog

        :return: None
        """
        path = os.getcwd()
        directory_name = QFileDialog.getExistingDirectory(self, "Select directory", path)
        print(directory_name)

    def process_annotations_file(self, file_path: str) -> None:
        """
        Show all cells contained in the annotations file

        :param file_path: Path of annotations file
        :return: None
        """
        self.select_dir_button.hide()
        self.select_file_button.hide()
        self.image = QLabel(self)
        self.layout.addWidget(self.image)

        coords_list = image_browser.parse_single_annotations_file(file_path)
        self.cell_index = 0

        while True:
            self.process_cell(file_path, coords_list[self.cell_index])
            self.cell_index = (
                0
                if self.cell_index < 0
                else len(coords_list) - 1
                if self.cell_index > len(coords_list) - 1
                else self.cell_index
            )  # handle index out of range

    def process_cell(self, file_path: str, coords: image_browser.Coords) -> None:
        """
        Display a single cell

        :param file_path: Path of annotations file
        :param coords: Coordinates of the cell
        :return: None
        """
        image_path = image_browser.get_image_name(file_path)
        cropped_cell = image_browser.crop_cell_from_image(image_path, coords)
        cropped_cell_img = ImageQt(cropped_cell)
        pixmap = QPixmap.fromImage(cropped_cell_img)

        self.image.setPixmap(pixmap)
        self.image.resize(pixmap.width(), pixmap.height())
        self.resize(pixmap.width(), pixmap.height())

        while not self.key_pressed:
            QCoreApplication.processEvents()
            time.sleep(0.05)

        self.key_pressed = False

    def keyPressEvent(self, event: QKeyEvent) -> None:
        """Key-press event handler"""
        if not event.isAutoRepeat() and not self.key_pressed:
            if event.key() == Qt.Key_Right:
                self.cell_index += 1
                self.key_pressed = True
            elif event.key() == Qt.Key_Left:
                self.cell_index -= 1
                self.key_pressed = True

    def eventFilter(self, source, event):
        """Low-level event handler"""
        if event.type() == QtCore.QEvent.KeyPress:
            self.keyPressEvent(event)
        return super().eventFilter(source, event)


if __name__ == "__main__":
    app = QApplication([])
    exit_code = MainApp()
    sys.exit(app.exec_())
