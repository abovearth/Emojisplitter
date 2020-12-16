import sys
import webbrowser
from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap, QPalette, QMovie
from PySide6.QtWidgets import QApplication, QLabel, QLineEdit, QPushButton, QSpinBox, QVBoxLayout, QHBoxLayout, QDialog, \
    QFileDialog, QScrollArea, QWidget, QCheckBox

import emojisplitter


# filename = ''
# todo: replace bolkvis with demo picture
# todo: show animated preview_split
class Form(QDialog):

    def __init__(self, parent=None):
        super(Form, self).__init__(parent)
        self.title = "Emoji Splitter"
        self.setWindowTitle(self.title)

        # preview_split widget
        self.preview_widget = QLabel()
        # media_preview = QPixmap('C:/Users/roela/PycharmProjects/Emojisplitter/bolkvis.png')
        # media_preview = QMovie('Naamloos.gif')  # QPixmap('Naamloos.gif')
        self.media_preview('Naamloos.gif')

        # embed preview_split in a scrollable window
        self.preview_scroll_area = QScrollArea()
        self.preview_scroll_area.setWidget(self.preview_widget)
        self.preview_scroll_area.setBackgroundRole(QPalette.Dark)
        self.preview_scroll_area.setWidgetResizable(True)

        # Create button widgets
        self.open_file_button = QPushButton("Select &File")
        self.filename = QLineEdit("C:/Users/roela/PycharmProjects/Emojisplitter/Naamloos.gif")
        self.preview_button = QPushButton("&Preview Split")
        self.fit_to_window_checkbox = QCheckBox("Fit Preview Image to &Window")
        self.horizontal_emojis_spinbox = QSpinBox()
        self.horizontal_emojis_spinbox.setMinimum(1)
        self.horizontal_emojis_label = QLabel("Number of &horizontal emojis:")
        self.horizontal_emojis_label.setBuddy(self.horizontal_emojis_spinbox)
        self.vertical_emojis_spinbox = QSpinBox()
        self.vertical_emojis_spinbox.setMinimum(1)
        self.vertical_emojis_label = QLabel("Number of &vertical emojis:")
        self.vertical_emojis_label.setBuddy(self.vertical_emojis_spinbox)
        self.split_emojis_button = QPushButton("&Split Emoji")
        self.results_folder_button = QPushButton("Open folder with &results")

        # give the button_layout a fixed width
        button_container = QWidget()
        button_container.setFixedWidth(256)

        # Create layout and add widgets
        button_layout = QVBoxLayout(button_container)
        button_layout.addWidget(self.open_file_button)
        button_layout.addWidget(self.filename)

        # Put labels next to spinboxes
        horizontal_emojis_layout = QHBoxLayout()
        horizontal_emojis_layout.addWidget(self.horizontal_emojis_label)
        horizontal_emojis_layout.addWidget(self.horizontal_emojis_spinbox)

        vertical_emojis_layout = QHBoxLayout()
        vertical_emojis_layout.addWidget(self.vertical_emojis_label)
        vertical_emojis_layout.addWidget(self.vertical_emojis_spinbox)

        button_layout.addLayout(horizontal_emojis_layout)
        button_layout.addLayout(vertical_emojis_layout)

        button_layout.addWidget(self.preview_button)
        button_layout.addWidget(self.fit_to_window_checkbox)
        button_layout.addWidget(self.split_emojis_button)
        button_layout.addWidget(self.results_folder_button)

        preview_layout = QVBoxLayout()
        # preview_layout.addWidget(self.preview_widget)
        preview_layout.addWidget(self.preview_scroll_area)

        # combine button and preview_split layout
        nested_layout = QHBoxLayout()
        nested_layout.addWidget(button_container)
        nested_layout.addLayout(preview_layout)
        # Set dialog layout
        self.setLayout(nested_layout)

        # Add button functions
        self.open_file_button.clicked.connect(self.open_file)
        self.preview_button.clicked.connect(self.preview_split)
        self.fit_to_window_checkbox.clicked.connect(self.fit_to_window)
        self.split_emojis_button.clicked.connect(self.split)
        self.results_folder_button.clicked.connect(self.open_folder_with_results)

        # update preview_split on changing value of a spinbox
        self.horizontal_emojis_spinbox.valueChanged.connect(self.preview_split)
        self.vertical_emojis_spinbox.valueChanged.connect(self.preview_split)

    # Preview the image.
    def preview_split(self):
        preview_image = emojisplitter.emojisplitter(self.filename.text(),
                                                    self.horizontal_emojis_spinbox.value(),
                                                    self.vertical_emojis_spinbox.value(),
                                                    False)
        self.preview_widget.setPixmap(preview_image)
        if self.fit_to_window_checkbox.checkState():
            self.fit_to_window()

    # Fit the image to the current window
    def fit_to_window(self):
        self.preview_widget.setPixmap(
            self.preview_widget.pixmap().scaled(self.preview_scroll_area.width(),
                                                self.preview_scroll_area.height(),
                                                aspectMode=Qt.KeepAspectRatio))

    # open file
    def open_file(self):
        self.filename.setText(QFileDialog.getOpenFileName(self, "Open Image")[0])
        self.media_preview(self.filename.text())

    def media_preview(self, filename):
        media_preview = QMovie(filename)
        self.preview_widget.setMovie(media_preview)
        self.preview_widget.movie().start()
        self.preview_widget.resize(media_preview.currentPixmap().width(), media_preview.currentPixmap().height())
        # self.preview_split()  # This immediately show where the split would be

    def split(self):
        emojisplitter.emojisplitter(self.filename.text(),
                                    self.horizontal_emojis_spinbox.value(),
                                    self.vertical_emojis_spinbox.value(),
                                    True)

    def open_folder_with_results(self):
        path = Path(self.filename.text()).parent
        webbrowser.open('file:///' + str(path))


if __name__ == '__main__':
    # Create the Qt Application
    app = QApplication(sys.argv)
    # Create and show the form
    form = Form()
    form.show()
    # Run the main Qt loop
    sys.exit(app.exec_())
