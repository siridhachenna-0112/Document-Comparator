from tracemalloc import start

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QTextCharFormat
from PyQt5.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QLabel,
    QTextEdit,
    QPlainTextEdit,
    QSplitter
)


class LineNumberTextEdit(QPlainTextEdit):

    def __init__(self, parent=None):

        super().__init__(parent)

        self.setReadOnly(True)

        self.setLineWrapMode(
            QPlainTextEdit.NoWrap
        )

        self.setStyleSheet("""
            QPlainTextEdit {
                font-size: 15px;
                padding: 8px;
            }
        """)


class TextViewer(QWidget):
    def highlight_word(
        self,
        editor,
        start,
        end,
        color
    ):
        print("START:", repr(start), type(start))
        print("END:", repr(end), type(end))
        if start >= end:
            return

        selection = QTextEdit.ExtraSelection()

        selection.cursor = editor.textCursor()

        selection.cursor.setPosition(start)

        selection.cursor.setPosition(
            end,
            selection.cursor.KeepAnchor
        )

        selection.format.setBackground(
            QColor(color)
        )

        selections = editor.extraSelections()

        selections.append(selection)

        editor.setExtraSelections(selections)
    
    def __init__(self, parent=None):

        super().__init__(parent)

        self.old_editor = LineNumberTextEdit()

        self.new_editor = LineNumberTextEdit()

        self.old_label = QLabel(
            "FILE 1 - ORIGINAL"
        )

        self.new_label = QLabel(
            "FILE 2 - MODIFIED"
        )

        self.old_label.setStyleSheet(
            "font-size:18px; font-weight:bold;"
        )

        self.new_label.setStyleSheet(
            "font-size:18px; font-weight:bold;"
        )

        old_layout = QVBoxLayout()

        old_layout.addWidget(
            self.old_label
        )

        old_layout.addWidget(
            self.old_editor
        )

        new_layout = QVBoxLayout()

        new_layout.addWidget(
            self.new_label
        )

        new_layout.addWidget(
            self.new_editor
        )

        old_widget = QWidget()

        old_widget.setLayout(
            old_layout
        )

        new_widget = QWidget()

        new_widget.setLayout(
            new_layout
        )

        splitter = QSplitter(
            Qt.Horizontal
        )

        splitter.addWidget(
            old_widget
        )

        splitter.addWidget(
            new_widget
        )

        splitter.setSizes(
            [500, 500]
        )

        main_layout = QHBoxLayout()

        main_layout.addWidget(
            splitter
        )

        self.setLayout(
            main_layout
        )

    def set_files(
        self,
        old_text,
        new_text
    ):

        self.old_editor.setPlainText(
            old_text
        )

        self.new_editor.setPlainText(
            new_text
        )

    def clear_highlighting(self):

        self.old_editor.setExtraSelections([])

        self.new_editor.setExtraSelections([])

    def highlight_line(
        self,
        editor,
        line_number,
        color
    ):

        document = editor.document()

        block = document.findBlockByNumber(
            line_number - 1
        )

        if not block.isValid():
            return

        selection = QTextEdit.ExtraSelection()

        selection.cursor = editor.textCursor()

        selection.cursor.setPosition(
            block.position()
        )

        selection.cursor.movePosition(
            selection.cursor.EndOfBlock,
            selection.cursor.KeepAnchor
        )

        selection.format.setBackground(
            QColor(color)
        )

        selections = (
            editor.extraSelections()
        )

        selections.append(
            selection
        )

        editor.setExtraSelections(
            selections
        )

    def highlight_differences(self, operations):

        self.clear_highlighting()

        for operation in operations:

            change_type = operation["type"]

            if change_type == "ADDED":

                self.highlight_word(
                    self.new_editor,
                    operation["start2"],
                    operation["end2"],
                    "#C8F7C5"
                )

            elif change_type == "DELETED":

                self.highlight_word(
                    self.old_editor,
                    operation["start1"],
                    operation["end1"],
                    "#FFC7CE"
                )

            elif change_type == "MODIFIED":

                self.highlight_word(
                    self.old_editor,
                    operation["start1"],
                    operation["end1"],
                    "#FFF2A8"
                )

                self.highlight_word(
                    self.new_editor,
                    operation["start2"],
                    operation["end2"],
                    "#FFF2A8"
                )