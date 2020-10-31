import sys
import os
import image_browser
import time
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QFileDialog, QVBoxLayout
from PyQt5.QtGui import QPixmap, QKeyEvent, QCloseEvent
from PyQt5.Qt import Qt
from PyQt5.QtCore import QCoreApplication
from PyQt5 import QtWidgets, QtCore
from PIL.ImageQt import ImageQt

WINDOW_WIDTH = 450
WINDOW_HEIGHT = 450


class MainApp(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.setFixedWidth(WINDOW_WIDTH)
        self.setFixedHeight(WINDOW_HEIGHT)
        self.key_pressed = False
        self.is_processing_images = False

        self.current_file = None
        self.current_cell_index = 0

        self.init_ui()

    def init_ui(self) -> None:
        """
        Initialize user interface, open prompt dialog

        :return: None
        """
        self.select_dir_button = QPushButton("Select directory", self)
        self.select_dir_button.setToolTip("Select directory")
        self.select_dir_button.clicked.connect(self.open_directory_browser)

        self.layout.addWidget(self.select_dir_button)
        self.setLayout(self.layout)

        QtWidgets.qApp.installEventFilter(self)

        self.show()

    def open_directory_browser(self) -> None:
        """
        Open directory selection dialog

        :return: None
        """
        path = "/home/bazyli/projects/dataset_leukocytes"
        self.directory_name = QFileDialog.getExistingDirectory(self, "Select directory", path)
        self.current_file = os.path.join(self.directory_name, os.listdir(self.directory_name)[0])
        self.is_processing_images = True

        self.image = QLabel(self)
        self.image.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.image)

        self.process_annotations_file()

    def process_annotations_file(self) -> None:
        """
        Show all cells contained in the annotations file

        :param current_file: Path of annotations file to process
        :return: New file path
        """
        self.select_dir_button.hide()

        coords_list = image_browser.parse_single_annotations_file(self.current_file)  # list of cells' coords

        if self.current_cell_index < 0 or self.current_cell_index >= len(coords_list):  # go to previous/next file
            old_filename_index = os.listdir(self.directory_name).index(self.current_file.split("/")[-1])
            new_filename_index = old_filename_index - 1 if self.current_cell_index < 0 else old_filename_index + 1
            new_filename_index = new_filename_index % len(
                os.listdir(self.directory_name)
            )  # handle list index out of range

            new_filename = os.listdir(self.directory_name)[new_filename_index]
            self.current_file = os.path.join(self.directory_name, new_filename)

            coords_list = image_browser.parse_single_annotations_file(self.current_file)
            self.current_cell_index = len(coords_list) - 1 if self.current_cell_index < 0 else 0

        print(
            f"Current file: {self.current_file}, "
            f"cell index: {self.current_cell_index}, "
            f"coords length: {len(coords_list)}"
        )
        self.process_cell(self.current_file, coords_list[self.current_cell_index])

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

        self.image.clear()
        self.image.setPixmap(pixmap)
        self.image.resize(pixmap.width(), pixmap.height())
        # self.resize(pixmap.width(), pixmap.height())

        self.update()

    def keyPressEvent(self, event: QKeyEvent) -> None:
        """Key-press event handler"""
        if self.is_processing_images and not event.isAutoRepeat():
            if event.key() == Qt.Key_Right:
                self.current_cell_index += 1
                self.process_annotations_file()
            elif event.key() == Qt.Key_Left:
                self.current_cell_index -= 1
                self.process_annotations_file()

    def eventFilter(self, source, event):
        """Low-level event handler"""
        if event.type() == QtCore.QEvent.KeyPress:
            self.keyPressEvent(event)
            return True
        elif event.type() == QtCore.QEvent.Close:
            self.closeEvent(event)
        return super().eventFilter(source, event)


if __name__ == "__main__":
    app = QApplication([])
    exit_code = MainApp()
    sys.exit(app.exec_())
