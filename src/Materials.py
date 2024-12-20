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
