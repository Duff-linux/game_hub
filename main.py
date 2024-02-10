import sys

from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QLabel, QGridLayout, QWidget

# import game logic from logic file
import logic

# colors for the tiles and their values
colors = {0: (204, 192, 179),     
          2: (238, 228, 218),
          4: (237, 224, 200),
          8: (242, 177, 121),
          16: (245, 149, 99),
          32: (246, 124, 95),
          64: (246, 94, 59),
          128: (237, 207, 114),
          256: (237, 204, 97),
          512: (237, 200, 80),
          1024: (237, 197, 63),
          2048: (237, 194, 46),
          'light text': (249, 246, 242),
          'dark text': (119, 110, 101),
          'other': (0, 0, 0),
          'bg': (187, 173, 160)}

# start the game
mat = logic.start_game()


class GridWidget(QWidget):
    def __init__(self):
        super(GridWidget, self).__init__()

        # Create a grid layout to arrange the labels
        grid_layout = QGridLayout(self)
        self.setStyleSheet(f"background-color : rgb{colors['bg']}")

        # Populate grid layout with labels
        self.tiles = [[None] * 4 for _ in range(4)]  # Create a 2D list to hold tiles
        for i in range(4):
            for j in range(4):
                value = mat[i][j]         
                value_color = colors['light text'] if value > 8 else colors['dark text']
                
                # Create a QLabel for each cell in the grid
                self.tiles[i][j] = QLabel(f"{value}")  # Create QLabel for each cell
                self.tiles[i][j].setMinimumSize(QtCore.QSize(50, 50))
                self.tiles[i][j].setMaximumSize(QtCore.QSize(50, 50))
                font = self.tiles[i][j].font()

                # font sizes
                if len(str(value)) == 1:
                    font.setPointSize(22)
                elif len(str(value)) == 2 :
                    font.setPointSize(18)
                elif len(str(value)) == 3:
                    font.setPointSize(14)
                else:
                    font.setPointSize(8)
                
                self.tiles[i][j].setFont(font)
                
                self.tiles[i][j].setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
                
                # Apply styling using CSS
                self.tiles[i][j].setStyleSheet(f"color: rgb{value_color}; background-color: rgb{colors[value]}; border-radius: 10px;")
                
                # Add the label to the grid layout at the specified row and column
                grid_layout.addWidget(self.tiles[i][j], i, j)

    def update_grid(self):
        # Update the text and styling of tiles based on the game matrix
        for i in range(4):
            for j in range(4):
                value = mat[i][j]
                self.tiles[i][j].setText(str(value))  # Update text
                value_color = colors['light text'] if value > 8 else colors['dark text']
                self.tiles[i][j].setStyleSheet(
                        f"color: rgb{value_color}; background-color: rgb{colors[value]}; border-radius: 10px;"
                    )  # Update styling            


    def keyPressEvent(self, event):
        global mat  # Declare mat as global
        if event.key() == QtCore.Qt.Key_Up:
            mat, flag = logic.move_up(mat)
            status = logic.get_current_state(mat)
            if status == 'GAME NOT OVER' and flag :
                logic.add_new_2(mat)            

        elif event.key() == QtCore.Qt.Key_Down:
            mat, flag = logic.move_down(mat)
            status = logic.get_current_state(mat)
            if status == 'GAME NOT OVER' and flag :
                logic.add_new_2(mat)
                            
        elif event.key() == QtCore.Qt.Key_Left:
            mat, flag = logic.move_left(mat)
            status = logic.get_current_state(mat)
            if status == 'GAME NOT OVER'and flag:   
                logic.add_new_2(mat)

        elif event.key() == QtCore.Qt.Key_Right:
            mat, flag = logic.move_right(mat)
            status = logic.get_current_state(mat)
            if status == 'GAME NOT OVER' and flag:
                logic.add_new_2(mat)

        
        self.update_grid()

        

if __name__ == "__main__":
    # Create a PyQt application instance
    app = QApplication(sys.argv)

    # Create an instance of the GridWidget class
    grid_widget = GridWidget()

    # Show the grid widget
    grid_widget.show()
    
    # Start the event loop
    sys.exit(app.exec_())
