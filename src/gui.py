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
        self.process_image(file_name)

    def open_directory_browser(self) -> None:
        """
        Open directory selection dialog

        :return: None
        """
        path = os.getcwd()
        directory_name = QFileDialog.getExistingDirectory(self, "Select directory", path)
        print(directory_name)

    def process_image(self, file_path: str) -> None:
        """
        Parse single annotation file

        :param file_path: Path to annotation file
        :return: None
        """
        self.select_dir_button.hide()
        self.select_file_button.hide()
        self.image = QLabel(self)
        self.layout.addWidget(self.image)

        for coords in image_browser.parse_single_image(file_path):
            image_path = image_browser.get_image_name(file_path)
            cropped_cell = image_browser.crop_cell_from_image(image_path, coords)
            cropped_cell_img = ImageQt(cropped_cell)
            pixmap = QPixmap.fromImage(cropped_cell_img)

            print(image_path, coords)

            self.image.setPixmap(pixmap)
            self.image.resize(pixmap.width(), pixmap.height())
            self.resize(pixmap.width(), pixmap.height())

            while not self.key_pressed:
                QCoreApplication.processEvents()
                time.sleep(0.05)

            self.key_pressed = False

            #  image_browser.set_label(file_path, coords, "123").write(file_path)
            # print(f"x_min: {coords.x_min}, y_min: {coords.y_min}, x_max: {coords.x_max}, y_max: {coords.y_max}")

    def keyPressEvent(self, event: QKeyEvent) -> None:
        """Key-press event handler"""
        if event.key() == Qt.Key_Right:
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
