import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5 import uic

from game_tabs import gameTabs
from games.game1 import main as g1

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi("game_hub.ui", self)

        # Set initial index of stacked widget to the profile page
        self.app_pages.setCurrentIndex(0)

        self.profile_btn.clicked.connect(self.profile)
        self.games_btn.clicked.connect(self.games)

        # Instantiate game_tabs widget and add it to the games page layout
        self.game_tabs = gameTabs()
        

        # Set layout for the games page
        self.games_page.setLayout(QtWidgets.QHBoxLayout())

        # Set size policy for game widget
        #self.game_tabs.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
      
        self.games_page.layout().addWidget(self.game_tabs)
        
      
        
    def profile(self):
        self.app_pages.setCurrentIndex(0)
    
    def games(self):
        self.app_pages.setCurrentIndex(1)
        self.game_tabs.setFocus()
        self.game_tabs.show()


    def keyPressEvent(self, event):
        # Forward key press event to the GridWidget
        self.game_tabs.game1.game_grid.keyPressEvent(event)

def main():
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()