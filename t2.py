from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, \
    QPushButton, QListWidget, QListWidgetItem, QFormLayout


class Product:
    def __init__(self, name, quantity, weight):
        self.name = name
        self.quantity = quantity
        self.weight = weight

    def get_total_weight(self):
        return self.quantity * self.weight


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Создаем список продуктов
        self.products = []

        # Создаем основной виджет
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Создаем вертикальный лейаут для основного виджета
        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        # Создаем форму для ввода информации о новом продукте
        form_layout = QFormLayout()
        self.name_input = QLineEdit()
        self.quantity_input = QLineEdit()
        self.weight_input = QLineEdit()
        form_layout.addRow('Название:', self.name_input)
        form_layout.addRow('Количество:', self.quantity_input)
        form_layout.addRow('Масса (кг):', self.weight_input)
        layout.addLayout(form_layout)

        # Создаем кнопку для добавления продукта в список
        add_button = QPushButton('Добавить продукт')
        add_button.clicked.connect(self.add_product)
        layout.addWidget(add_button)

        # Создаем список продуктов
        self.products_list = QListWidget()
        layout.addWidget(self.products_list)

        # Задаем заголовок главного окна
        self.setWindowTitle('Список продуктов')

    def add_product(self):
        """
        Функция добавления нового продукта в список
        """
        name = self.name_input.text().strip()
        quantity = float(self.quantity_input.text())
        weight = float(self.weight_input.text())
        product = Product(name, quantity, weight)
        self.products.append(product)
        self.name_input.setText('')
        self.quantity_input.setText('')
        self.weight_input.setText('')
        self.update_products_list()

    def update_products_list(self):
        """
        Функция обновления списка продуктов
        """
        self.products_list.clear()  # Очищаем список продуктов
        total_weight = 0  # Обнуляем суммарный вес продуктов
        for product in self.products:
            # Создаем элемент QListWidgetItem с текстом продукта
            text = f'{product.name} - {product.quantity} шт., {product.weight} кг/шт. = {product.get_total_weight()} кг'
            item = QListWidgetItem(text)
            # Добавляем элемент в список продуктов
            self.products_list.addItem(item)
            # Увеличиваем суммарный вес продуктов
            total_weight += product.get_total_weight()
        # Добавляем элемент с суммарным весом продуктов в список продуктов
        total_weight_text = f'Суммарный вес продуктов: {total_weight} кг'
        total_weight_item = QListWidgetItem(total_weight_text)
        self.products_list.addItem(total_weight_item)


if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
