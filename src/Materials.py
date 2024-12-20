from PyQt5.QtWidgets import (
    QTableView,
    QLabel, QPushButton,
    QHBoxLayout, QWidget
    )
from PyQt5.QtCore import Qt
from PyQt5.QtSql import QSqlQueryModel, QSqlQuery

class Model(QSqlQueryModel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_page = 0
        self.page_size = 15
        self.total_pages = 0
        self.count()
        self.refresh()

    def count(self):
        count_query = QSqlQuery()
        count_query.exec_('SELECT COUNT(*) FROM materials')
        if count_query.next():
            total_records = count_query.value(0)
            self.total_pages = (total_records + self.page_size - 1) // self.page_size

    def set_page(self, page):
        if 0 <= page < self.total_pages:
            self.current_page = page
            self.refresh()

    def refresh(self):
        self.count()
        offset = self.current_page * self.page_size

        sql = f'''
            SELECT 
                mt.title AS material_type, 
                m.title AS name, 
                m.min_quantity, 
                m.stock_quantity,
                (
                    SELECT STRING_AGG(title, ', ') 
                    FROM (
                        SELECT title
                        FROM suppliers
                        WHERE id IN (
                            SELECT supplier_id 
                            FROM materials_suppliers 
                            WHERE material_id = m.id
                        )
                    ) AS supplier_list
                ) AS supplier
            FROM materials AS m
            JOIN material_type AS mt ON m.material_type_id = mt.id
            LIMIT {self.page_size} OFFSET {offset};
        '''
        self.setQuery(sql)

        self.setHeaderData(0, Qt.Horizontal, "Тип")
        self.setHeaderData(1, Qt.Horizontal, "Наименование")
        self.setHeaderData(2, Qt.Horizontal, "Мин. количество")
        self.setHeaderData(3, Qt.Horizontal, "Остаток")
        self.setHeaderData(4, Qt.Horizontal, "Поставщики")


class View(QTableView):
    def __init__(self, parent=None):
        super().__init__(parent)
        model = Model(parent=self)
        self.setModel(model)

        self.setSelectionBehavior(self.SelectRows)
        self.setSelectionMode(self.SingleSelection)
        self.setWordWrap(False)
        vh = self.verticalHeader()
        vh.setSectionResizeMode(vh.Fixed)
        hh = self.horizontalHeader()
        hh.setSectionResizeMode(hh.ResizeToContents)

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
        self.model.set_page(self.model.current_page - 1)
        self.update_ui()

    def next_page(self):
        self.model.set_page(self.model.current_page + 1)
        self.update_ui()
