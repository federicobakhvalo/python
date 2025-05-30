from pathlib import Path

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QVBoxLayout
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

        # Текущая выбранная операция, None по умолчанию
        self.current_operation = None

        # Подключаем кнопки операций
        self.buttons = {
            'add': self.ui.btnAdd,
            'sub': self.ui.btnSub,
            'mul': self.ui.btnMul,
            'div': self.ui.btnDiv,
        }
        for op_name, btn in self.buttons.items():
            btn.clicked.connect(lambda checked, op=op_name: self.select_operation(op))

        self.ui.btnCalculate.clicked.connect(self.calculate)

        # По умолчанию кнопка рассчитать отключена
        self.ui.btnCalculate.setEnabled(False)

        # Проверяем inputы при изменении текста
        self.ui.lineEdit1.textChanged.connect(self.check_can_calculate)
        self.ui.lineEdit2.textChanged.connect(self.check_can_calculate)

        # Цвета
        self.selected_color = "background-color: #4CAF50; color: white;"
        self.unselected_color = ""

    def load_styles(self, path: Path):
        if path.exists():
            with open(path, "r") as f:
                self.setStyleSheet(f.read())

    def _save_to_db(self, operation, result, expression):
        if self.conn is None or self.cursor is None:
            raise ConnectionError('Database is not exists or not ready')
        self.cursor.execute(
            "INSERT INTO history (operation, result, expression) VALUES (?, ?, ?)",
            (operation, result, expression)
        )
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
            return None, None

    def select_operation(self, operation):
        self.current_operation = operation
        self.update_operation_buttons()
        self.check_can_calculate()

    def update_operation_buttons(self):
        for op_name, btn in self.buttons.items():
            if op_name == self.current_operation:
                btn.setStyleSheet(self.selected_color)
            else:
                btn.setStyleSheet(self.unselected_color)

    def check_can_calculate(self):
        a, b = self.get_inputs()
        can_calc = a is not None and b is not None and self.current_operation is not None
        self.ui.btnCalculate.setEnabled(can_calc)


    def reset_calculation(self):
        self.ui.lineEdit1.setText(None)
        self.ui.lineEdit2.setText(None)
        self.current_operation=None


    def calculate(self):
        a, b = self.get_inputs()
        if a is None or b is None:
            QMessageBox.critical(self, "Ошибка", "Введите корректные числа")
            return
        if self.current_operation is None:
            QMessageBox.warning(self, "Ошибка", "Выберите операцию")
            return

        try:
            if self.current_operation == 'add':
                result = a + b
                expression = f"{a} + {b} = {result}"
            elif self.current_operation == 'sub':
                result = a - b
                expression = f"{a} - {b} = {result}"
            elif self.current_operation == 'mul':
                result = a * b
                expression = f"{a} * {b} = {result}"
            elif self.current_operation == 'div':
                if b == 0:
                    QMessageBox.warning(self, "Ошибка", "Деление на ноль невозможно")
                    return
                result = a / b
                expression = f"{a} / {b} = {result}"
            else:
                QMessageBox.warning(self, "Ошибка", "Неизвестная операция")
                return

            self.ui.labelResult.setText(str(result))
            self.reset_calculation()
            self._save_to_db(self.current_operation, str(result), expression)
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка вычисления: {e}")

app = QApplication([])
window = Calculator()
window.show()
app.exec()