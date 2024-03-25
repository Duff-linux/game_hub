from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QTabWidget, QWidget, QHBoxLayout, QVBoxLayout, QSpacerItem, QSizePolicy

from games.game1 import main as g1
from games.game2 import main as g2

class gameTabs(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.game1 = g1.Game_1()

        # main tabwidget layout
        layout = QVBoxLayout()
        layout.setContentsMargins(0,0,0,0)
        
        # tabs
        self.game_1_tab = QWidget()
        self.game_2_tab = QWidget()

        tab_widget = QTabWidget()
        

        # game 1 layout
        game_1_layout = QHBoxLayout()        
        game_1_layout.addWidget(self.game1)      
        self.game_1_tab.setLayout(game_1_layout)

        # game 2 layout
        game_2_layout = QVBoxLayout()
        game_2_layout.addWidget(self.game_2_tab)

        # add tabs to tabwidget
        tab_widget.addTab(self.game_1_tab, '2048')
        tab_widget.addTab(self.game_2_tab, 'HangMan')

        # Add the tab widget to the main layout
        layout.addWidget(tab_widget)

        # Set the main layout for the window
        self.setLayout(layout)

