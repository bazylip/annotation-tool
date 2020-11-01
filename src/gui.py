import os
import image_browser
from pathlib import Path
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QFileDialog, QVBoxLayout
from PyQt5.QtGui import QPixmap, QKeyEvent, QFont
from PyQt5.Qt import Qt
from PyQt5 import QtWidgets, QtCore
from PIL.ImageQt import ImageQt

WINDOW_WIDTH = 450
WINDOW_HEIGHT = 450
IMG_DIR = "img/"

Labels = {
    Qt.Key_H: "Heterophil",
    Qt.Key_L: "Lymphocyte",
    Qt.Key_M: "Monocyte",
    Qt.Key_B: "Basophil",
    Qt.Key_T: "Thrombocyte",
    Qt.Key_E: "Eosinophil",
    Qt.Key_U: "Unknown",
}

Resize = {Qt.Key_1: 1.5, Qt.Key_2: 2.5, Qt.Key_3: 3.5}


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
        self.prompt_label = QLabel(self)
        self.prompt_label.setText("Please select directory")
        self.prompt_label.setFixedHeight(30)

        self.select_dir_button = QPushButton("Select directory", self)
        self.select_dir_button.setToolTip("Select directory")
        self.select_dir_button.clicked.connect(self.open_directory_browser)

        self.layout.addWidget(self.prompt_label)
        self.layout.addWidget(self.select_dir_button)
        self.layout.setAlignment(Qt.AlignHCenter)
        self.setLayout(self.layout)

        QtWidgets.qApp.installEventFilter(self)

        self.show()

    def open_directory_browser(self) -> None:
        """
        Open directory selection dialog

        :return: None
        """
        path = os.getcwd()
        self.directory_name = QFileDialog.getExistingDirectory(self, "Select directory", path)
        if not self.directory_name or self.directory_name.split("/")[-1] != "xml":  # user did not select correct directory
            self.prompt_label.setText("Wrong directory! Please select annotations/xml")
            return

        self.select_dir_button.hide()
        self.prompt_label.hide()

        self.current_file = os.path.join(self.directory_name, os.listdir(self.directory_name)[0])
        self.is_processing_images = True

        self.image = QLabel(self)
        self.image.setAlignment(Qt.AlignCenter)

        self.label = QLabel(self)
        self.label.setAlignment(Qt.AlignBottom | Qt.AlignCenter)
        self.label.setFont(QFont("Arial", 14))

        self.layout.addWidget(self.image)
        self.layout.addWidget(self.label)

        self.process_annotations_file()

    def process_annotations_file(self) -> None:
        """
        Show cells contained in current annotations file

        :return: None
        """
        self.coords_list = image_browser.parse_single_annotations_file(self.current_file)  # list of cells' coords
        if self.current_cell_index < 0 or self.current_cell_index >= len(self.coords_list):  # go to previous/next file
            separator = "\\" if os.name == "nt" else "/"  # adjust file path separator to linux/windows
            old_filename_index = os.listdir(self.directory_name).index(self.current_file.split(separator)[-1])
            new_filename_index = old_filename_index - 1 if self.current_cell_index < 0 else old_filename_index + 1
            new_filename_index = new_filename_index % len(
                os.listdir(self.directory_name)
            )  # handle list index out of range
            new_filename = os.listdir(self.directory_name)[new_filename_index]
            self.current_file = os.path.join(self.directory_name, new_filename)

            self.coords_list = image_browser.parse_single_annotations_file(self.current_file)
            self.current_cell_index = len(self.coords_list) - 1 if self.current_cell_index < 0 else 0

        # print(f"Current file: {self.current_file}, current cell index: {self.current_cell_index}")
        self.process_cell()

    def process_cell(self, resize: float = 2.5) -> None:
        """
        Display a single cell

        :param resize: Resize factor to make picture bigger/smaller
        :return: None
        """
        coords = self.coords_list[self.current_cell_index]

        image_name = image_browser.get_image_name(self.current_file)
        parent_path = Path(self.current_file).parents[1]
        image_path = os.path.join(parent_path, IMG_DIR, image_name)
        img_path = image_browser.crop_cell_from_image(image_path, coords, parent_path, resize)
        pixmap = QPixmap(img_path)
        self.image.clear()

        self.image.setPixmap(pixmap)
        self.image.resize(pixmap.width(), pixmap.height())

        self.label.setText(
            f"Label: {image_browser.get_label(self.current_file, self.coords_list[self.current_cell_index])}"
        )

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
            elif event.key() in Resize.keys():
                self.process_cell(Resize[event.key()])
            elif event.key() in Labels.keys():
                coords = self.coords_list[self.current_cell_index]
                label = Labels[event.key()]
                image_browser.set_label(self.current_file, coords, label).write(self.current_file)
                self.process_cell()
                print(f"File: {self.current_file}, coords: {coords}, label: {label}")

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
    app.exec_()
