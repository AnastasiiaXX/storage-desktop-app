from PyQt5.QtWidgets import (
    QMainWindow, QMessageBox, QWidget, QVBoxLayout
)
from PyQt5.QtCore import pyqtSlot
#from MainMenu import MainMenu
from src import Materials


class MainWindow(QMainWindow):
        def __init__(self, parent=None):
            super().__init__(parent)
            self.setWindowTitle('Материалы')
            #main_menu = MainMenu(parent=self)
            #self.setMenuBar(main_menu)
            self.model = Materials.Model(parent=self)
            self.view = Materials.View(parent=self)
            self.view.setModel(self.model)

            self.pagination = Materials.Pagination(self.model, parent=self)

            central_widget = QWidget()
            layout = QVBoxLayout(central_widget)
            layout.addWidget(self.view)
            layout.addWidget(self.pagination)

            self.setCentralWidget(central_widget)


