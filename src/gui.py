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

        self.current_file = None
        self.current_cell = None

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
        start_file = os.path.join(self.directory_name, os.listdir(self.directory_name)[0])
        self.finish_browsing = False

        self.image = QLabel(self)
        self.image.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.image)

        while not self.finish_browsing:
            start_file = self.process_annotations_file(start_file)

    def process_annotations_file(self, current_file: str) -> str:
        """
        Show all cells contained in the annotations file

        :param current_file: Path of annotations file to process
        :return: New file path
        """
        self.select_dir_button.hide()

        self.finish_current_file = False
        coords_list = image_browser.parse_single_annotations_file(current_file)  # list of cells' coords

        if not self.current_cell:
            self.current_cell = 0
        elif self.current_cell == -1:  # -1 indicates starting from last cell
            self.current_cell = len(coords_list) - 1

        while not self.finish_current_file:
            print(f"Current file: {current_file}, cell index: {self.current_cell}, coords length: {len(coords_list)}")
            self.process_cell(current_file, coords_list[self.current_cell])

            if self.current_cell < 0 or self.current_cell >= len(coords_list):  # go to previous/next file
                old_filename_index = os.listdir(self.directory_name).index(current_file.split("/")[-1])
                new_filename_index = old_filename_index - 1 if self.current_cell < 0 else old_filename_index + 1
                new_filename_index = new_filename_index % len(
                    os.listdir(self.directory_name)
                )  # handle list index out of range

                new_filename = os.listdir(self.directory_name)[new_filename_index]
                self.current_cell = -1 if self.current_cell < 0 else 0

                return os.path.join(self.directory_name, new_filename)

        return ""

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

        while not self.key_pressed:  # wait for user to press key
            QCoreApplication.processEvents()
            time.sleep(0.05)

        self.key_pressed = False

    def keyPressEvent(self, event: QKeyEvent) -> None:
        """Key-press event handler"""
        if not event.isAutoRepeat() and not self.key_pressed:
            if event.key() == Qt.Key_Right:
                self.current_cell += 1
                self.key_pressed = True
            elif event.key() == Qt.Key_Left:
                self.current_cell -= 1
                self.key_pressed = True

    def closeEvent(self, event: QCloseEvent) -> None:
        """Close application"""
        self.finish_current_file = True
        self.finish_browsing = True
        self.key_pressed = True

    def eventFilter(self, source, event):
        """Low-level event handler"""
        if event.type() == QtCore.QEvent.KeyPress:
            self.keyPressEvent(event)
        elif event.type() == QtCore.QEvent.Close:
            self.closeEvent(event)
        return super().eventFilter(source, event)


if __name__ == "__main__":
    app = QApplication([])
    exit_code = MainApp()
    sys.exit(app.exec_())
