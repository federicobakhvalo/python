import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QLineEdit, QPlainTextEdit, QFileDialog, QMessageBox
)


class TextEditor(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Простой текстовый редактор")
        self.setGeometry(100, 100, 600, 500)

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Верхняя панель с QLabel и QLineEdit
        file_layout = QHBoxLayout()
        self.label = QLabel("Файл:")
        self.file_input = QLineEdit()
        file_layout.addWidget(self.label)
        file_layout.addWidget(self.file_input)

        layout.addLayout(file_layout)

        # Основное текстовое поле
        self.text_area = QPlainTextEdit()
        layout.addWidget(self.text_area)

        # Нижние кнопки
        button_layout = QHBoxLayout()
        self.open_button = QPushButton("Открыть")
        self.save_button = QPushButton("Сохранить")
        self.clear_button = QPushButton("Очистить")

        self.open_button.clicked.connect(self.open_file)
        self.save_button.clicked.connect(self.save_file)
        self.clear_button.clicked.connect(self.clear_text)

        button_layout.addWidget(self.open_button)
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.clear_button)

        layout.addLayout(button_layout)

        self.setLayout(layout)

    def open_file(self):
        path, _ = QFileDialog.getOpenFileName(self, "Открыть файл", "", "Text Files (*.txt);;All Files (*)")
        if path:
            try:
                with open(path, "r", encoding="utf-8") as file:
                    content = file.read()
                    self.text_area.setPlainText(content)
                    self.file_input.setText(path)
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", f"Не удалось открыть файл:\n{e}")

    def save_file(self):
        path = self.file_input.text()
        if not path:
            path, _ = QFileDialog.getSaveFileName(self, "Сохранить файл", "", "Text Files (*.txt);;All Files (*)")
        if path:
            try:
                with open(path, "w", encoding="utf-8") as file:
                    content = self.text_area.toPlainText()
                    file.write(content)
                    self.file_input.setText(path)
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", f"Не удалось сохранить файл:\n{e}")

    def clear_text(self):
        self.text_area.clear()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TextEditor()
    window.show()
    sys.exit(app.exec())
