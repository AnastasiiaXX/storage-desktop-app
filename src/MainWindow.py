from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QComboBox, QPushButton, QLabel
)
from PyQt5.QtCore import Qt
from src import Materials

class MainWindow(QWidget):
        def __init__(self, parent=None):
            super().__init__(parent)
            self.setWindowTitle('Материалы')

            layout = QVBoxLayout(self)

            search_layout = QHBoxLayout()
            search_label = QLabel("")

            self.search_input = QLineEdit()
            self.search_input.setFixedWidth(200)
            self.search_input.setPlaceholderText("Введите для поиска:")
            search_layout.addWidget(search_label)
            search_layout.addWidget(self.search_input)

            sort_layout = QHBoxLayout()
            sort_label = QLabel("Сортировка:")
            self.sort_combo = QComboBox()
            self.sort_combo.addItem("По названию")
            self.sort_combo.addItem("По типу")
            self.sort_combo.addItem("По количеству")
            sort_layout.addWidget(sort_label)
            sort_layout.addWidget(self.sort_combo)

            filter_layout = QHBoxLayout()
            filter_label = QLabel("Фильтрация:")
            self.filter_combo = QComboBox()
            self.filter_combo.addItem("Все материалы")
            self.filter_combo.addItem("Материалы с низким остатком")
            self.filter_combo.addItem("Материалы по типу")
            filter_layout.addWidget(filter_label)
            filter_layout.addWidget(self.filter_combo)

            main_layout = QHBoxLayout()
            main_layout.addLayout(search_layout)
            main_layout.addLayout(sort_layout)
            main_layout.addLayout(filter_layout)

            layout.addLayout(main_layout)

            view = Materials.View(self)
            layout.addWidget(view)

            bottom_box = QHBoxLayout()

            add_btn = QPushButton("Добавить материал", parent=self)
            bottom_box.addWidget(add_btn, alignment=Qt.AlignLeft)

            pagination_box = QHBoxLayout()
            prev_btn = QPushButton("<", parent=self)
            next_btn = QPushButton(">", parent=self)

            pagination_box.addWidget(prev_btn)
            pagination_box.addWidget(next_btn)

            bottom_box.addLayout(pagination_box)
            bottom_box.addStretch()
            layout.addLayout(bottom_box)

            self.setLayout(layout)
