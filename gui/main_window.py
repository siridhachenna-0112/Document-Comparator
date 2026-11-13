import os
import tempfile

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLabel,
    QFileDialog,
    QMessageBox,
    QTableWidget,
    QTableWidgetItem,
    QTabWidget,
    QSplitter,
    QGroupBox
)

from core.document_reader import (
    read_document,
    extract_docx_images
)

from core.text_comparator import (
    word_level_diff
)

from core.image_comparator import (
    compare_image_folders
)

from gui.text_viewer import TextViewer
from gui.image_viewer import ImageViewer

from utils.file_utils import (
    is_supported_file
)


class MainWindow(QMainWindow):

    def __init__(self):

        super().__init__()

        self.setWindowTitle(
            "Offline Document Comparator"
        )

        self.setMinimumSize(
            1200,
            750
        )

        self.file1 = None
        self.file2 = None

        self.text1 = ""
        self.text2 = ""

        self.image_folder1 = None
        self.image_folder2 = None

        self.setup_ui()

    def setup_ui(self):

        central = QWidget()

        self.setCentralWidget(
            central
        )

        main_layout = QVBoxLayout()

        # ------------------------------------------------
        # TITLE
        # ------------------------------------------------

        title = QLabel(
            "OFFLINE DOCUMENT COMPARATOR"
        )

        title.setAlignment(
            Qt.AlignCenter
        )

        title.setStyleSheet("""
            QLabel {
                font-size: 26px;
                font-weight: bold;
                padding: 12px;
            }
        """)

        main_layout.addWidget(
            title
        )

        # ------------------------------------------------
        # FILE SELECTION
        # ------------------------------------------------

        file_group = QGroupBox(
            "Select Files"
        )

        file_layout = QVBoxLayout()

        # File 1
        row1 = QHBoxLayout()

        self.file1_label = QLabel(
            "File 1: No file selected"
        )

        self.file1_label.setWordWrap(
            True
        )

        browse1 = QPushButton(
            "Browse File 1"
        )

        browse1.clicked.connect(
            self.browse_file1
        )

        row1.addWidget(
            self.file1_label
        )

        row1.addWidget(
            browse1
        )

        # File 2
        row2 = QHBoxLayout()

        self.file2_label = QLabel(
            "File 2: No file selected"
        )

        self.file2_label.setWordWrap(
            True
        )

        browse2 = QPushButton(
            "Browse File 2"
        )

        browse2.clicked.connect(
            self.browse_file2
        )

        row2.addWidget(
            self.file2_label
        )

        row2.addWidget(
            browse2
        )

        file_layout.addLayout(
            row1
        )

        file_layout.addLayout(
            row2
        )

        file_group.setLayout(
            file_layout
        )

        main_layout.addWidget(
            file_group
        )

        # ------------------------------------------------
        # BUTTONS
        # ------------------------------------------------

        button_layout = QHBoxLayout()

        compare_button = QPushButton(
            "COMPARE FILES"
        )

        compare_button.setStyleSheet("""
            QPushButton {
                font-size: 17px;
                font-weight: bold;
                padding: 10px;
            }
        """)

        compare_button.clicked.connect(
            self.compare_files
        )

        clear_button = QPushButton(
            "CLEAR"
        )

        clear_button.clicked.connect(
            self.clear_all
        )

        button_layout.addWidget(
            compare_button
        )

        button_layout.addWidget(
            clear_button
        )

        main_layout.addLayout(
            button_layout
        )

        # ------------------------------------------------
        # STATISTICS
        # ------------------------------------------------

        statistics_layout = QHBoxLayout()

        self.similarity_label = QLabel(
            "Similarity: --"
        )

        self.added_label = QLabel(
            "Added: 0"
        )

        self.deleted_label = QLabel(
            "Deleted: 0"
        )

        self.modified_label = QLabel(
            "Modified: 0"
        )

        self.unchanged_label = QLabel(
            "Unchanged: 0"
        )

        for label in [
            self.similarity_label,
            self.added_label,
            self.deleted_label,
            self.modified_label,
            self.unchanged_label
        ]:

            label.setStyleSheet("""
                QLabel {
                    font-size: 15px;
                    font-weight: bold;
                    padding: 7px;
                }
            """)

            statistics_layout.addWidget(
                label
            )

        main_layout.addLayout(
            statistics_layout
        )

        # ------------------------------------------------
        # TABS
        # ------------------------------------------------

        self.tabs = QTabWidget()

        # Text comparison
        self.text_viewer = TextViewer()

        self.tabs.addTab(
            self.text_viewer,
            "TEXT COMPARISON"
        )

        # Difference report
        self.report_table = QTableWidget()

        self.report_table.setColumnCount(
            6
        )

        self.report_table.setHorizontalHeaderLabels([
            "No.",
            "Type",
            "File 1 Line",
            "File 2 Line",
            "Original",
            "Modified"
        ])

        self.report_table.setWordWrap(
            True
        )

        self.report_table.setAlternatingRowColors(
            True
        )

        self.tabs.addTab(
            self.report_table,
            "DIFFERENCE REPORT"
        )

        # Image comparison
        self.image_viewer = ImageViewer()

        self.tabs.addTab(
            self.image_viewer,
            "IMAGE COMPARISON"
        )

        # Image report
        self.image_report = QTableWidget()

        self.image_report.setColumnCount(
            5
        )

        self.image_report.setHorizontalHeaderLabels([
            "No.",
            "Image",
            "Status",
            "Similarity",
            "Details"
        ])

        self.image_report.setAlternatingRowColors(
            True
        )

        self.tabs.addTab(
            self.image_report,
            "IMAGE REPORT"
        )

        main_layout.addWidget(
            self.tabs
        )

        central.setLayout(
            main_layout
        )

    # ====================================================
    # FILE BROWSING
    # ====================================================

    def browse_file1(self):

        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select File 1",
            "",
            "Supported Files (*.txt *.docx)"
        )

        if not file_path:
            return

        if not is_supported_file(
            file_path
        ):

            QMessageBox.warning(
                self,
                "Invalid File",
                "Only TXT and DOCX files are supported."
            )

            return

        self.file1 = file_path

        self.file1_label.setText(
            "File 1: " + file_path
        )

    def browse_file2(self):

        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select File 2",
            "",
            "Supported Files (*.txt *.docx)"
        )

        if not file_path:
            return

        if not is_supported_file(
            file_path
        ):

            QMessageBox.warning(
                self,
                "Invalid File",
                "Only TXT and DOCX files are supported."
            )

            return

        self.file2 = file_path

        self.file2_label.setText(
            "File 2: " + file_path
        )

    # ====================================================
    # COMPARISON
    # ====================================================

    def compare_files(self):

        if not self.file1 or not self.file2:

            QMessageBox.warning(
                self,
                "Files Missing",
                "Please select both files."
            )

            return

        try:

            self.text1 = read_document(
                self.file1
            )

            self.text2 = read_document(
                self.file2
            )

        except Exception as error:

            QMessageBox.critical(
                self,
                "Error",
                "Could not read files:\n\n{}".format(
                    error
                )
            )

            return

        # -----------------------------------------------
        # TEXT COMPARISON
        # -----------------------------------------------

        result = word_level_diff(
            self.text1,
            self.text2
        )
        self.text_viewer.set_files(
            self.text1,
            self.text2
        )
        self.text_viewer.set_files(
            self.text1,
            self.text2
        )

        self.text_viewer.highlight_differences(
            result["operations"]
        )

        self.update_statistics(
            result
        )

        self.populate_report(
            result["operations"]
        )

        # -----------------------------------------------
        # IMAGE COMPARISON
        # -----------------------------------------------

        self.compare_images()

        self.tabs.setCurrentIndex(
            0
        )

    # ====================================================
    # STATISTICS
    # ====================================================

    def update_statistics(
        self,
        result
    ):

        self.similarity_label.setText(
            "Similarity: {}%".format(
                result["similarity"]
            )
        )

        self.added_label.setText(
            "Added: {}".format(
                result["added"]
            )
        )

        self.deleted_label.setText(
            "Deleted: {}".format(
                result["deleted"]
            )
        )

        self.modified_label.setText(
            "Modified: {}".format(
                result["modified"]
            )
        )

        self.unchanged_label.setText(
            "Unchanged: {}".format(
                result["unchanged"]
            )
        )

    # ====================================================
    # TEXT REPORT
    # ====================================================

    def populate_report(
        self,
        operations
    ):

        changes = [
            operation
            for operation in operations
            if operation["type"] != "UNCHANGED"
        ]

        self.report_table.setRowCount(
            len(changes)
        )

        for row, operation in enumerate(
            changes
        ):

            values = [
                str(row + 1),
                operation["type"],
                str(operation["line1"]),
                str(operation["line2"]),
                operation["original"],
                operation["modified"]
            ]

            for column, value in enumerate(
                values
            ):

                item = QTableWidgetItem(
                    value
                )

                item.setToolTip(
                    value
                )

                self.report_table.setItem(
                    row,
                    column,
                    item
                )

            change_type = operation["type"]

            if change_type == "ADDED":

                background = QColor(
                    "#C8F7C5"
                )

            elif change_type == "DELETED":

                background = QColor(
                    "#FFC7CE"
                )

            else:

                background = QColor(
                    "#FFF2A8"
                )

            for column in range(6):

                item = self.report_table.item(
                    row,
                    column
                )

                if item:
                    item.setBackground(
                        background
                    )

        self.report_table.resizeColumnsToContents()

    # ====================================================
    # IMAGE COMPARISON
    # ====================================================

    def compare_images(self):

        self.image_report.setRowCount(
            0
        )

        # Temporary folders
        self.image_folder1 = tempfile.mkdtemp(
            prefix="doc_compare_1_"
        )

        self.image_folder2 = tempfile.mkdtemp(
            prefix="doc_compare_2_"
        )

        # Extract images only from DOCX
        if self.file1.lower().endswith(
            ".docx"
        ):

            extract_docx_images(
                self.file1,
                self.image_folder1
            )

        if self.file2.lower().endswith(
            ".docx"
        ):

            extract_docx_images(
                self.file2,
                self.image_folder2
            )

        try:

            results = compare_image_folders(
                self.image_folder1,
                self.image_folder2
            )

        except Exception:

            results = []

        self.image_report.setRowCount(
            len(results)
        )

        for row, result in enumerate(
            results
        ):

            status = result["status"]

            details = ""

            if status == "SAME":

                details = "Image is identical."

            elif status == "MODIFIED":

                details = (
                    "Image content is different."
                )

            elif status == "ADDED":

                details = (
                    "Image exists only in File 2."
                )

            elif status == "DELETED":

                details = (
                    "Image exists only in File 1."
                )

            values = [
                str(row + 1),
                result["image"],
                status,
                "{}%".format(
                    result["similarity"]
                ),
                details
            ]

            for column, value in enumerate(
                values
            ):

                self.image_report.setItem(
                    row,
                    column,
                    QTableWidgetItem(value)
                )

            if status == "SAME":

                background = QColor(
                    "#C8F7C5"
                )

            elif status == "MODIFIED":

                background = QColor(
                    "#FFF2A8"
                )

            else:

                background = QColor(
                    "#FFC7CE"
                )

            for column in range(5):

                item = self.image_report.item(
                    row,
                    column
                )

                if item:
                    item.setBackground(
                        background
                    )

        self.image_report.resizeColumnsToContents()
        # Automatically display the first image pair

        if results:

            first_result = results[0]

            self.image_viewer.show_images(
                first_result["file1"],
                first_result["file2"]
            )

        # Connect selection
        self.image_report.cellClicked.connect(
            self.image_selected
        )

    def image_selected(
        self,
        row,
        column
    ):

        if not self.image_folder1 or not self.image_folder2:
            return

        image_name_item = (
            self.image_report.item(
                row,
                1
            )
        )

        if not image_name_item:
            return

        image_name = (
            image_name_item.text()
        )

        file1 = os.path.join(
            self.image_folder1,
            image_name
        )

        file2 = os.path.join(
            self.image_folder2,
            image_name
        )

        if not os.path.exists(file1):
            file1 = None

        if not os.path.exists(file2):
            file2 = None

        self.image_viewer.show_images(
            file1,
            file2
        )

        self.tabs.setCurrentIndex(
            2
        )

    # ====================================================
    # CLEAR
    # ====================================================

    def clear_all(self):

        self.file1 = None
        self.file2 = None

        self.text1 = ""
        self.text2 = ""

        self.file1_label.setText(
            "File 1: No file selected"
        )

        self.file2_label.setText(
            "File 2: No file selected"
        )

        self.text_viewer.set_files(
            "",
            ""
        )

        self.report_table.setRowCount(
            0
        )

        self.image_report.setRowCount(
            0
        )

        self.similarity_label.setText(
            "Similarity: --"
        )

        self.added_label.setText(
            "Added: 0"
        )

        self.deleted_label.setText(
            "Deleted: 0"
        )

        self.modified_label.setText(
            "Modified: 0"
        )

        self.unchanged_label.setText(
            "Unchanged: 0"
        )

        self.image_viewer.show_images(
            None,
            None
        )