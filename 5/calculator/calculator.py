from pathlib import Path

from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox
from calculator_ui import Ui_MainWindow
import sqlite3

class Calculator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self._init_db()
        self.load_styles(Path('../styles/calculator.qss'))
        self.load_history()
        self.ui.btnAdd.clicked.connect(self.add)
        self.ui.btnSub.clicked.connect(self.sub)
        self.ui.btnMul.clicked.connect(self.mul)
        self.ui.btnDiv.clicked.connect(self.div)

    def load_styles(self,path:Path):
        with open(path, "r") as f:
            self.setStyleSheet(f.read())

    def _save_to_db(self, operation, result, expression):
        if self.conn is None or self.cursor is None:
            raise ConnectionError('Database is not exists or not ready')
        self.cursor.execute("INSERT INTO history (operation, result, expression) VALUES (?, ?, ?)",
                            (operation, result, expression))
        self.conn.commit()

        # Оставляем только последние 5
        self.cursor.execute("""
            DELETE FROM history WHERE id NOT IN (
                SELECT id FROM history ORDER BY id DESC LIMIT 5
            )
        """)
        self.conn.commit()
        self.load_history()

    def load_history(self):
        self.cursor.execute("SELECT expression FROM history ORDER BY id DESC")
        rows = self.cursor.fetchall()
        self.ui.listHistory.clear()
        for row in rows:
            self.ui.listHistory.addItem(row[0])

    def _init_db(self):
        self.conn = sqlite3.connect("history.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    operation TEXT,
                    result TEXT,
                    expression TEXT
                )
            """)
        self.conn.commit()

    def get_inputs(self):
        try:
            a = float(self.ui.lineEdit1.text())
            b = float(self.ui.lineEdit2.text())
            return a, b
        except ValueError:
            QMessageBox.critical(self, "Ошибка", "Введите корректные числа")
            return None, None

    def add(self):
        a, b = self.get_inputs()
        if a is not None:

            self.ui.labelResult.setText(str(a + b))
            expression = f"{a} + {b} = {a+b}"
            self._save_to_db("add", str(a+b), expression)

    def sub(self):
        a, b = self.get_inputs()
        if a is not None:
            self.ui.labelResult.setText(str(a - b))
            expression = f"{a} - {b} = {a - b}"
            self._save_to_db("sub", str(a - b), expression)

    def mul(self):
        a, b = self.get_inputs()
        if a is not None:
            self.ui.labelResult.setText(str(a * b))
            expression = f"{a} * {b} = {a * b}"
            self._save_to_db("mul", str(a * b), expression)

    def div(self):
        a, b = self.get_inputs()
        if a is not None:
            try:
                self.ui.labelResult.setText(str(a / b))
                expression=f'{a} / {b} = {a/b}'
                self._save_to_db('div',str(a/b),expression)
            except ZeroDivisionError:
                QMessageBox.warning(self, "Ошибка", "Деление на ноль невозможно")

app = QApplication([])
window = Calculator()
window.show()
app.exec()