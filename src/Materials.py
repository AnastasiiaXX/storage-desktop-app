from PyQt5.QtWidgets import (
    QTableView, QMessageBox, QDialog,
    QLabel, QPushButton, QTextEdit, QLineEdit,
    QVBoxLayout, QHBoxLayout, QWidget
)
from PyQt5.QtSql import QSqlQueryModel, QSqlQuery
from PyQt5.QtCore import pyqtSlot, Qt

class Model(QSqlQueryModel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.page_size = 15
        self.current_page = 0
        self.total_pages = 0
        self.refresh()

    def refresh(self):
        count_query = QSqlQuery()
        count_query.exec_('select count(*) from materials')

        if count_query.next():
            total_records = count_query.value(0)
            self.total_pages = (total_records + self.page_size - 1) // self.page_size

        offset = self.current_page * self.page_size
        sql = f'''
            select id, name, material_type, image_path, price, 
            stock_quantity, min_quantity, package_quantity, unit
            from materials
            limit {self.page_size} OFFSET {offset};
        '''
        self.setQuery(sql)

    def set_page(self, page):
        if 0 <= page < self.total_pages:
            self.current_page = page
            self.refresh()

    def select_one(self, id):
        sel_query = QSqlQuery()
        SELECT_ONE = '''
               select id, name, material_type, image_path, price, 
                stock_quantity, min_quantity, package_quantity, unit
                from materials
                where id = :id ;
           '''
        sel_query.prepare(SELECT_ONE)
        sel_query.bindValue(':id', id)
        sel_query.exec_()
        if sel_query.isActive():
            sel_query.first()
            return (sel_query.value('name'), sel_query.value('material_type'),
                    sel_query.value('image_path'), sel_query.value('price'),
                    sel_query.value('stock_quantity'), sel_query.value('min_quantity'),
                    sel_query.value('package_quantity'), sel_query.value('unit'))
        self.refresh()
        return "", "", "", ""

class View(QTableView):
    def __init__(self, parent=None):
        super().__init__(parent)
        model = Model(parent=self)
        self.setModel(model)
        model.setHeaderData(1, Qt.Horizontal, "Название")
        model.setHeaderData(2, Qt.Horizontal, "Тип материала")
        model.setHeaderData(3, Qt.Horizontal, "Изображение")
        model.setHeaderData(4, Qt.Horizontal, "Стоимость")
        model.setHeaderData(5, Qt.Horizontal, "Остаток на складе")
        model.setHeaderData(6, Qt.Horizontal, "Мин. количество")
        model.setHeaderData(7, Qt.Horizontal, "Кол-во в упаковке")
        model.setHeaderData(8, Qt.Horizontal, "Единица измерения")
        self.setSelectionBehavior(self.SelectRows)
        self.setSelectionMode(self.SingleSelection)
        self.hideColumn(0)
        self.setWordWrap(False)
        vh = self.verticalHeader()
        vh.setSectionResizeMode(vh.Fixed)
        hh = self.horizontalHeader()
        hh.setSectionResizeMode(hh.ResizeToContents)
        hh.setSectionResizeMode(7, hh.Stretch)

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

