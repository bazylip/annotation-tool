import sys
import os
import image_browser
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QMessageBox, QFileDialog


class MainApp(QWidget):
    def __init__(self):
        super().__init__()
        self.title = "Annotation tool"
        self.left = 500
        self.top = 500
        self.width = 320
        self.height = 200
        self.init_ui()

    def init_ui(self) -> None:
        """
        Initialize user interface, open prompt dialog

        :return: None
        """
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        select_dir_button = QPushButton("Select directory", self)
        select_dir_button.setToolTip("Select directory")
        select_dir_button.move(100, 70)
        select_dir_button.clicked.connect(self.open_directory_browser)

        select_file_button = QPushButton("Select file", self)
        select_file_button.setToolTip("Select file")
        select_file_button.move(100, 140)
        select_file_button.clicked.connect(self.open_file_browser)

        self.show()

    def process_image(self, file_path: str) -> None:
        """
        Parse single annotation file

        :param file_path: Path to annotation file
        :return: None
        """
        for coords in image_browser.parse_single_image(file_path):
            image_browser.set_label(file_path, coords, "123").write(file_path)
            print(f"x_min: {coords.x_min}, y_min: {coords.y_min}, x_max: {coords.x_max}, y_max: {coords.y_max}")

    def open_file_browser(self) -> None:
        """
        Open file selection dialog

        :return: None
        """
        path = os.getcwd()
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


if __name__ == "__main__":
    app = QApplication([])
    exit_code = MainApp()
    sys.exit(app.exec_())
