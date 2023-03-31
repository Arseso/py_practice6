import re

from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, \
    QPushButton, QListWidget, QListWidgetItem
from PyQt5.QtGui import QTextDocument, QDesktopServices
from PyQt5.QtCore import QUrl


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Создаем список заметок
        self.notes = []

        # Создаем основной виджет
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Создаем вертикальный лейаут для основного виджета
        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        # Создаем поле для ввода текста заметки
        self.text_input = QLineEdit()
        layout.addWidget(self.text_input)

        # Создаем кнопку для добавления заметки в список
        add_button = QPushButton('Добавить заметку')
        add_button.clicked.connect(self.add_note)
        layout.addWidget(add_button)

        # Создаем список заметок
        self.notes_list = QListWidget()
        layout.addWidget(self.notes_list)

        # Устанавливаем обработчик событий при выборе заметки в списке
        self.notes_list.itemClicked.connect(self.delete_note)

        # Задаем заголовок главного окна
        self.setWindowTitle('Заметки')

    def add_note(self):
        """
        Функция добавления новой заметки в список
        """
        note_text = self.text_input.text().strip() # Получаем текст заметки из поля ввода
        if note_text and not(note_text.isspace()): # Проверяем, что текст заметки не пустой
            note_id = len(self.notes) + 1 # Генерируем уникальный идентификатор для заметки
            self.notes.append({'id': note_id, 'text': note_text}) # Добавляем заметку в список
            self.text_input.setText('') # Очищаем поле ввода
            self.update_notes_list() # Обновляем список заметок

    def delete_note(self, item):
        """
        Функция удаления выбранной заметки из списка
        """
        note_id = item.data(32) # Получаем уникальный идентификатор заметки из атрибута data элемента списка
        for note in self.notes:
            if note['id'] == note_id:
                self.notes.remove(note) # Удаляем заметку из списка
                break
        self.update_notes_list() # Обновляем список заметок

    def update_notes_list(self):
        """
        Функция обновления списка заметок
        """
        url_regex = re.compile(r'(https?://\S+)')
        self.notes_list.clear()  # Очищаем список заметок
        for note in self.notes:
            text = note['text']
            # Проверяем наличие ссылок в тексте заметки
            match = url_regex.search(text)
            if match:
                url = match.group(0)
                if QUrl(url).isValid():
                    # Создаем кликабельную ссылку, только если URL валидный
                    text = url_regex.sub(f'<a href="{url}">{url}</a>', text)
                    item = QListWidgetItem(text)
                    item.setData(32, note['id'])
                    self.notes_list.addItem(item)
                    url = QUrl(url)
                    item.setOpenExternalLinks(True)
                    item.linkActivated.connect(lambda _, url=url: QDesktopServices.openUrl(url))
                else:
                    # Если URL невалидный, то заменяем его в тексте заметки на обычный текст
                    text = url_regex.sub(url, text)
                    item = QListWidgetItem(text)
                    item.setData(32, note['id'])
                    self.notes_list.addItem(item)
            else:
                item = QListWidgetItem(text)
                item.setData(32, note['id'])
                self.notes_list.addItem(item)


if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()