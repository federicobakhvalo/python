import sys

from PyQt6.QtCore import Qt

from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QPushButton, \
    QFormLayout, QLineEdit, QComboBox, QWidget, QHBoxLayout

import sqlite3
from database import Database

from ui_main_window import Ui_MainWindow








class StudentApp(QMainWindow):
    STUDENTS_PER_PAGE = 10
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.db = Database()
        self.current_page = 1
        self.is_search_mode = False

        # Скрыть формы
        self.ui.registerForm.hide()
        self.ui.searchForm.hide()

        # Подключение кнопок
        self.ui.registerButton.clicked.connect(self.show_register_form)
        self.ui.searchButton.clicked.connect(self.show_search_form)
        self.ui.addStudentButton.clicked.connect(self.add_student)
        self.ui.deleteButton.clicked.connect(self.delete_students)
        self.ui.searchStudentButton.clicked.connect(self.search_students)

        #
        # # Скрыть кнопку удаления по умолчанию
        self.ui.deleteButton.setVisible(False)

        #
        # # Подключаем чекбоксы
        #self.ui.resultsTable.itemChanged.connect(self.check_checkbox_status)
        self.ui.searchStudentButton.setDisabled(True)
        self.ui.searchFirstNameInput.textChanged.connect(self.update_search_button_state)
        self.ui.searchLastNameInput.textChanged.connect(self.update_search_button_state)
        self.ui.groupCombo.currentTextChanged.connect(self.update_search_button_state)

        # Начальная проверка
        self.update_search_button_state()

        # Кнопка сброса фильтров
        self.resetButton = QPushButton("Сбросить фильтр")
        self.resetButton.clicked.connect(self.reset_filters)
        self.ui.verticalLayout.addWidget(self.resetButton)




        # Кнопки пагинации
        self.pagination_widget = QWidget()
        self.pagination_layout = QHBoxLayout()
        self.prevPageButton = QPushButton("← Назад")
        self.nextPageButton = QPushButton("Вперёд →")
        self.prevPageButton.clicked.connect(self.prev_page)
        self.nextPageButton.clicked.connect(self.next_page)

        self.pagination_layout.addWidget(self.prevPageButton)
        self.pagination_layout.addWidget(self.nextPageButton)
        self.pagination_widget.setLayout(self.pagination_layout)
        self.ui.verticalLayout.addWidget(self.pagination_widget)

        self.load_students_page(1)
        self.load_groups()


    def load_groups(self):
        self.ui.groupCombo.clear()
        self.ui.groupCombo.addItem("")

        self.db.execute("SELECT DISTINCT group_name FROM students")
        groups = self.db.fetchall()
        for group in groups:
            self.ui.groupCombo.addItem(group[0])

    def update_search_button_state(self):
        first_name = self.ui.searchFirstNameInput.text().strip()
        last_name = self.ui.searchLastNameInput.text().strip()
        group_name = self.ui.groupCombo.currentText().strip()

        if first_name or last_name or group_name:
            self.ui.searchStudentButton.setEnabled(True)
        else:
            self.ui.searchStudentButton.setDisabled(True)

    def delete_students(self):
        # Получаем выбранные строки из таблицы
        selected_rows = []
        for row in range(self.ui.resultsTable.rowCount()):
            checkbox_item = self.ui.resultsTable.item(row, 0)  # Чекбокс находится в первом столбце
            if checkbox_item and checkbox_item.checkState() == Qt.CheckState.Checked:
                selected_rows.append(row)  # Добавляем индекс строки

        if not selected_rows:
            print("Не выбрано ни одного студента для удаления.")
            return

        # Удаляем студентов из базы данных (если нужно)
        for row in selected_rows:
            student_id_item = self.ui.resultsTable.item(row, 1)  # ID студента во втором столбце
            student_id = student_id_item.text()
            try:
                self.db.execute("DELETE FROM students WHERE id = ?", (student_id,))
                self.db.connection.commit()
                print(f"Студент с ID {student_id} удален из базы данных.")
            except Exception as e:
                print(f"Ошибка при удалении студента из базы данных: {e}")

        # Удаляем строки из таблицы
        self.delete_from_tables(selected_rows)

    def delete_from_tables(self, indexes):
        # Удаляем строки из таблицы по переданным индексам
        for row in reversed(indexes):  # Обрабатываем индексы в обратном порядке, чтобы избежать ошибок при удалении
            self.ui.resultsTable.removeRow(row)

        print(f"Удалено {len(indexes)} строк из таблицы.")

    def check_checkbox_status(self, item):
        if item.column() == 0:  # Проверяем, что изменился чекбокс (первый столбец)
            # Проверяем, есть ли хотя бы один выбранный чекбокс
            selected = any(
                self.ui.resultsTable.item(row, 0).checkState() == Qt.CheckState.Checked
                # Используем Qt.CheckState.Checked
                for row in range(self.ui.resultsTable.rowCount())
            )

            # Если есть выбранные чекбоксы, показываем кнопку удаления, иначе скрываем
            self.ui.deleteButton.setVisible(selected)

    def show_register_form(self):
        self.ui.registerForm.show()
        self.ui.searchForm.hide()

    def show_search_form(self):
        self.ui.searchForm.show()
        self.ui.registerForm.hide()

    def add_student(self):
        first_name = self.ui.firstNameInput.text()
        last_name = self.ui.lastNameInput.text()
        phone_number = self.ui.phoneInput.text()
        group_name = self.ui.groupInput.text()

        if first_name and last_name:
            try:
                # Выполнение запроса на добавление студента в базу данных
                self.db.execute("""
                    INSERT INTO students (first_name, last_name, phone_number, group_name)
                    VALUES (?, ?, ?, ?)
                """, (first_name, last_name, phone_number, group_name))
                self.db.connection.commit()

                # Очистка полей ввода
                self.ui.firstNameInput.clear()
                self.ui.lastNameInput.clear()
                self.ui.phoneInput.clear()
                self.ui.groupInput.clear()

                # Скрытие формы добавления
                self.ui.registerForm.hide()

                # Получение ID последней вставленной строки
                new_student_id = self.db.cursor.lastrowid
                print(new_student_id)
                if new_student_id is None:
                    raise Exception("Failed to retrieve last inserted student ID")

                new_student = {
                    'id': new_student_id,  # Получаем ID только что добавленного студента
                    'first_name': first_name,
                    'last_name': last_name,
                    'phone_number': phone_number
                }

                # Добавляем нового студента в таблицу
                self.add_student_to_table(new_student)

            except Exception as e:
                # Обработка ошибок (например, проблемы с базой данных)
                print(f"Error occurred while adding student: {e}")
                # Можно добавить отображение сообщения пользователю, если нужно
                # self.ui.show_error_message("Error adding student: " + str(e))
            else:
                print(f"Student {first_name} {last_name} added successfully!")

    def add_student_to_table(self, student_data):
        try:
            row_position = self.ui.resultsTable.rowCount()
            self.ui.resultsTable.insertRow(0)  # Вставляем строку в начало таблицы
            checkbox_item = QTableWidgetItem()

            checkbox_item.setFlags(
                checkbox_item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
            checkbox_item.setCheckState(Qt.CheckState.Unchecked)

            self.ui.resultsTable.setItem(0, 0, checkbox_item)

            # Заполняем ячейки новой строки данными студента
            self.ui.resultsTable.setItem(0, 1, QTableWidgetItem(str(student_data['id'])))
            self.ui.resultsTable.setItem(0, 2, QTableWidgetItem(student_data['first_name']))
            self.ui.resultsTable.setItem(0, 3, QTableWidgetItem(student_data['last_name']))
            self.ui.resultsTable.setItem(0, 4, QTableWidgetItem(student_data['phone_number']))

        except Exception as e:
            print(f"Error adding student to table: {e}")


    def search_query(self,first_name,last_name,group):
        conditions = []
        values = []
        debug_parts = []

        if first_name:
            conditions.append("LOWER(first_name) LIKE ?")
            values.append(f"%{first_name}%")
            debug_parts.append(f'first name I like "%{first_name}%"')

        if last_name:
            conditions.append("LOWER(last_name) LIKE ?")
            values.append(f"%{last_name}%")
            debug_parts.append(f'last name I like "%{last_name}%"')

        if group:
            conditions.append("group_name LIKE ?")
            values.append(f"%{group}%")
            debug_parts.append(f'group I like "%{group}%"')

        if not conditions:
            # Ничего не вводили — просто выходим
            return

        # Можно вывести отладочную строку запроса:
        print("Searching for:", " and ".join(debug_parts))

        where_clause = " AND ".join(conditions)
        query = f"SELECT * FROM students WHERE {where_clause}"
        return query,values

    def search_students(self):
        first_name = self.ui.searchFirstNameInput.text().strip()
        last_name = self.ui.searchLastNameInput.text().strip()
        group_name = self.ui.groupCombo.currentText().strip()
        query,values=self.search_query(first_name,last_name,group_name)
        try:
            self.db.execute(query, values)
            table=self.ui.resultsTable
            results = self.db.fetchall()
            if results:
                self.render_students_table(results)
            else:
                table.clearContents()
                table.setRowCount(1)
                table.setColumnCount(table.columnCount())  # сохраняем кол-во колонок

                # Сообщение по центру всей строки
                item = QTableWidgetItem("Ничего не найдено.")
                # item.setTextAlignment(Qt.AlignCenter)
                item.setFlags(Qt.ItemFlag.ItemIsEnabled) # только для отображения

                # Вставляем сообщение в первую колонку
                table.setItem(0, 0, item)

                # Убираем заголовки, если нужно:
                table.setHorizontalHeaderLabels([""] * table.columnCount())
                table.verticalHeader().setVisible(False)
            self.is_search_mode = True

        except Exception as E:

            print(str(E))



    def reset_filters(self):
        if self.is_search_mode:
            try:
                self.ui.searchFirstNameInput.clear()
                self.ui.searchLastNameInput.clear()
                self.ui.groupCombo.setCurrentIndex(0)
                self.load_students_page(1)
            except Exception as E:
                print(str(E))
            self.is_search_mode=False


    def load_students_page(self, page):
        try:
            offset = (page - 1) * self.STUDENTS_PER_PAGE
            self.db.execute("SELECT * FROM students LIMIT ? OFFSET ?", (self.STUDENTS_PER_PAGE, offset))
            students = self.db.fetchall()
            print(students)
            self.render_students_table(students)
            self.current_page = page
        except Exception as e:
            print("Ошибка в load_students_page:", e)


    def prev_page(self):
        if not self.is_search_mode and self.current_page > 1:
            self.load_students_page(self.current_page - 1)

    def next_page(self):
        if self.is_search_mode:
            return  # не менять страницы в режиме поиска

        self.db.execute("SELECT COUNT(*) FROM students")
        total_students = self.db.fetchone()[0]
        if self.current_page * self.STUDENTS_PER_PAGE < total_students:
            self.load_students_page(self.current_page + 1)

    def render_students_table(self, students):
        self.ui.resultsTable.setRowCount(len(students))
        self.ui.resultsTable.setColumnCount(6)
        self.ui.resultsTable.setHorizontalHeaderLabels(["Выбрать", "ID", "Имя", "Фамилия", "Телефон", "Группа"])

        try:
            self.ui.resultsTable.itemChanged.disconnect()
        except TypeError:
            pass

        for row, student in enumerate(students):
            checkbox_item = QTableWidgetItem()
            checkbox_item.setFlags(checkbox_item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
            checkbox_item.setCheckState(Qt.CheckState.Unchecked)
            self.ui.resultsTable.setItem(row, 0, checkbox_item)

            for col, value in enumerate(student, start=1):
                self.ui.resultsTable.setItem(row, col, QTableWidgetItem(str(value)))

        self.ui.resultsTable.itemChanged.connect(self.check_checkbox_status)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = StudentApp()
    window.show()
    sys.exit(app.exec())