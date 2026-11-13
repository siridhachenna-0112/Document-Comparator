from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QScrollArea
)


class ImageViewer(QWidget):

    def __init__(self, parent=None):

        super().__init__(parent)

        self.left_image = QLabel()
        self.right_image = QLabel()

        self.left_image.setAlignment(
            Qt.AlignCenter
        )

        self.right_image.setAlignment(
            Qt.AlignCenter
        )

        self.left_image.setMinimumSize(
            400,
            300
        )

        self.right_image.setMinimumSize(
            400,
            300
        )

        left_layout = QVBoxLayout()

        left_label = QLabel(
            "FILE 1 IMAGE"
        )

        left_label.setStyleSheet(
            "font-size:18px; font-weight:bold;"
        )

        left_layout.addWidget(
            left_label
        )

        left_layout.addWidget(
            self.left_image
        )

        right_layout = QVBoxLayout()

        right_label = QLabel(
            "FILE 2 IMAGE"
        )

        right_label.setStyleSheet(
            "font-size:18px; font-weight:bold;"
        )

        right_layout.addWidget(
            right_label
        )

        right_layout.addWidget(
            self.right_image
        )

        container = QHBoxLayout()

        container.addLayout(
            left_layout
        )

        container.addLayout(
            right_layout
        )

        self.setLayout(
            container
        )

    def show_images(
        self,
        file1,
        file2
    ):

        self.left_image.clear()
        self.right_image.clear()

        if file1:

            pixmap1 = QPixmap(
                file1
            )

            if not pixmap1.isNull():

                pixmap1 = pixmap1.scaled(
                    600,
                    500,
                    Qt.KeepAspectRatio,
                    Qt.SmoothTransformation
                )

                self.left_image.setPixmap(
                    pixmap1
                )

        if file2:

            pixmap2 = QPixmap(
                file2
            )

            if not pixmap2.isNull():

                pixmap2 = pixmap2.scaled(
                    600,
                    500,
                    Qt.KeepAspectRatio,
                    Qt.SmoothTransformation
                )

                self.right_image.setPixmap(
                    pixmap2
                )