import sys
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QLabel, QGridLayout, QWidget
import logic

colors = {
    0: (204, 192, 179),
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
    'bg': (187, 173, 160)
}

mat = logic.start_game()

class GridWidget(QWidget):
    def __init__(self):
        super(GridWidget, self).__init__()
        self.grid_layout = QGridLayout(self)
        self.setStyleSheet(f"background-color : rgb{colors['bg']}")
        self.tiles = [[None] * 4 for _ in range(4)]
        self.update_grid()

    def update_grid(self):
        for i in range(4):
            for j in range(4):
                value = mat[i][j]
                if value == 0:
                    text = ''
                else:
                    text = str(value)
                if self.tiles[i][j] is None:
                    self.tiles[i][j] = QLabel(text)
                    self.tiles[i][j].setMinimumSize(QtCore.QSize(50, 50))
                    self.tiles[i][j].setMaximumSize(QtCore.QSize(50, 50))
                    self.tiles[i][j].setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
                    self.grid_layout.addWidget(self.tiles[i][j], i, j)
                else:
                    self.tiles[i][j].setText(text)
                value_color = colors['light text'] if value > 8 else colors['dark text']
                self.tiles[i][j].setStyleSheet(
                    f"color: rgb{value_color}; background-color: rgb{colors[value]}; border-radius: 10px;"
                )

                # Set font size based on text length
                font = self.tiles[i][j].font()
                if len(text) == 1:
                    font.setPointSize(22)
                elif len(text) == 2:
                    font.setPointSize(18)
                elif len(text) == 3:
                    font.setPointSize(14)
                else:
                    font.setPointSize(12)
                self.tiles[i][j].setFont(font)


    def keyPressEvent(self, event):
        global mat
        if event.key() == QtCore.Qt.Key_Up:
            mat, flag = logic.move_up(mat)
            if flag:
                logic.add_new_2(mat)
        elif event.key() == QtCore.Qt.Key_Down:
            mat, flag = logic.move_down(mat)
            if flag:
                logic.add_new_2(mat)
        elif event.key() == QtCore.Qt.Key_Left:
            mat, flag = logic.move_left(mat)
            if flag:
                logic.add_new_2(mat)
        elif event.key() == QtCore.Qt.Key_Right:
            mat, flag = logic.move_right(mat)
            if flag:
                logic.add_new_2(mat)
        self.update_grid()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    grid_widget = GridWidget()
    grid_widget.show()
    sys.exit(app.exec_())
