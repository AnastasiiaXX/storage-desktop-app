from PyQt5.QtWidgets import (
    QTableView, QMessageBox, QDialog,
    QLabel, QPushButton, QTextEdit, QLineEdit,
    QVBoxLayout, QHBoxLayout, QWidget
)
from PyQt5.QtCore import Qt
from PyQt5.QtSql import QSqlQueryModel, QSqlQuery


class Model(QSqlQueryModel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_page = 0
        self.page_size = 15
        self.total_pages = 0
        self.refresh()

    def refresh(self):
        sql = f'''
            SELECT mt.title, m.title, m.min_quantity, m.stock_quantity,
            (
            SELECT STRING_AGG(title, ', ') FROM (
                SELECT title
                FROM suppliers
                WHERE id IN (SELECT supplier_id from materials_suppliers
                WHERE material_id = m.id))
                ) as supplier
            FROM materials AS m, material_type as mt
            WHERE m.material_type_id = mt.id;
        '''
        self.setQuery(sql)

    def count_pages(self):
        # Запрос для подсчета общего количества строк
        count_query = """
            SELECT COUNT(*) FROM materials
        """
        self.setQuery(count_query)
        if self.lastError().isValid():
            print("Ошибка выполнения запроса:", self.lastError().text())
            return
        total_items = self.query().value(0)
        if total_items is None:
            total_items = 0
        self.total_pages = (total_items + self.page_size - 1) // self.page_size

    def set_page(self, page):
        self.current_page = page
        self.count_pages()
        # Запрос для получения данных для текущей страницы
        offset = self.current_page * self.page_size
        sql = f"""
            SELECT mt.title, m.title, m.min_quantity, m.stock_quantity,
            (
            SELECT STRING_AGG(title, ', ') FROM (
                SELECT title
                FROM suppliers
                WHERE id IN (SELECT supplier_id from materials_suppliers
                WHERE material_id = m.id))
                ) as supplier
            FROM materials AS m, material_type as mt
            WHERE m.material_type_id = mt.id
            LIMIT {self.page_size} OFFSET {offset}
        """
        self.setQuery(sql)

class View(QTableView):
    def __init__(self, parent=None):
        super().__init__(parent)
        model = Model(parent=self)
        self.setModel(model)
        model.setHeaderData(0, Qt.Horizontal, "Тип")
        model.setHeaderData(1, Qt.Horizontal, "Наименование")
        model.setHeaderData(2, Qt.Horizontal, "Мин. количество")
        model.setHeaderData(3, Qt.Horizontal, "Остаток")
        model.setHeaderData(4, Qt.Horizontal, "Поставщики")
        self.setSelectionBehavior(self.SelectRows)
        self.setSelectionMode(self.SingleSelection)
        self.setWordWrap(False)
        vh = self.verticalHeader()
        vh.setSectionResizeMode(vh.Fixed)
        hh = self.horizontalHeader()
        hh.setSectionResizeMode(hh.ResizeToContents)
        #hh.setSectionResizeMode(2, hh.Stretch)

from PyQt5.QtWidgets import QWidget, QHBoxLayout, QPushButton, QLabel
from PyQt5.QtCore import Qt

class Pagination(QWidget):
    def __init__(self, model, parent=None):
        super().__init__(parent)
        self.model = model
        self.layout = QHBoxLayout(self)

        self.prev_button = QPushButton('Назад')
        self.prev_button.clicked.connect(self.prev_page)
        self.layout.addWidget(self.prev_button)

        self.page_label = QLabel()
        self.layout.addWidget(self.page_label)

        self.next_button = QPushButton('Вперед')
        self.next_button.clicked.connect(self.next_page)
        self.layout.addWidget(self.next_button)

        self.update_ui()

    def update_ui(self):
        self.page_label.setText(f"Страница {self.model.current_page + 1} из {self.model.total_pages}")
        self.prev_button.setEnabled(self.model.current_page > 0)
        self.next_button.setEnabled(self.model.current_page < self.model.total_pages - 1)

    def prev_page(self):
        if self.model.current_page > 0:
            self.model.set_page(self.model.current_page - 1)
            self.update_ui()

    def next_page(self):
        if self.model.current_page < self.model.total_pages - 1:
            self.model.set_page(self.model.current_page + 1)
            self.update_ui()
