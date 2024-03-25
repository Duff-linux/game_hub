from PyQt5 import QtCore
from PyQt5.QtWidgets import QLabel, QGridLayout, QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QSpacerItem, QSizePolicy


from games.game1 import logic

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

class ScoreKeeper(QtCore.QObject):
    score_changed = QtCore.pyqtSignal(int)

    def __init__(self) -> None:
        super().__init__()
        self.score = 0
    
    def update_score(self, new_score):
        self.score += new_score
        self.score_changed.emit(self.score)
    
    def reset_score(self):
        self.score = 0
        self.score_changed.emit(self.score)


class GridWidget(QWidget):
    def __init__(self):
        super(GridWidget, self).__init__()
        self.setMaximumSize(QtCore.QSize(250, 250))
        self.game_grid_layout = QGridLayout(self)
        self.setStyleSheet(f"background-color : rgb{colors['bg']}")
        self.tiles = [[None] * 4 for _ in range(4)]
        self.update_grid()
        self.score_keeper = ScoreKeeper()

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
                    self.game_grid_layout.addWidget(self.tiles[i][j], i, j)
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
            mat, flag, score = logic.move_up(mat)
            if flag:
                logic.add_new_2(mat)
        elif event.key() == QtCore.Qt.Key_Down:
            mat, flag, score = logic.move_down(mat)
            if flag:
                logic.add_new_2(mat)
        elif event.key() == QtCore.Qt.Key_Left:
            mat, flag, score = logic.move_left(mat)
            if flag:
                logic.add_new_2(mat)
        elif event.key() == QtCore.Qt.Key_Right:
            mat, flag, score = logic.move_right(mat)
            if flag:
                logic.add_new_2(mat)

        # update grid after a move and get the score
        self.update_grid()
        self.score_keeper.update_score(score)        

        # get the state of the game
        game_state = logic.get_current_state(mat)
        print(game_state)

    def reset_grid(self):
        global mat 
        mat = logic.start_game()
        self.update_grid()
        
        


class Game_1(QWidget):
    def __init__(self):
        super(Game_1, self).__init__()
        
        self.score = 0
        self.highest_score = 0

        # grid instance
        self.game_grid = GridWidget()
        self.game_grid_layout = QHBoxLayout()
        self.game_grid_layout.addWidget(self.game_grid, alignment= QtCore.Qt.AlignCenter)

        # score keeper instance from GridWidget class
        self.score_keeper = self.game_grid.score_keeper
        self.score_keeper.score_changed.connect(self.update_score_labels)


        # main layout
        self.main_layout = QHBoxLayout()

        # side layout and content
        self.side_layout = QVBoxLayout()
        self.side_layout.setContentsMargins(0,0,0,0)
        
        # score label
        self.score_label = QLabel()
        self.score_label.setStyleSheet('color: white')
        
        # highest score label
        self.highest_score_label = QLabel()
        self.highest_score_label.setStyleSheet('color: rgb(255,255,255)')
        
        # reset game btn
        self.reset_btn = QPushButton('Reset Game')
        self.reset_btn.setStyleSheet('color: white; background-color:green')
        self.reset_btn.clicked.connect(self.reset_game)

        # side layout spacer
        spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        # side layout setup
        self.side_layout.addWidget(self.score_label, alignment= QtCore.Qt.AlignLeft)
        self.side_layout.addWidget(self.highest_score_label, alignment= QtCore.Qt.AlignLeft)
        self.side_layout.addItem(spacer)
        self.side_layout.addWidget(self.reset_btn, alignment = QtCore.Qt.AlignLeft)

        # main layout setup: put game grid and side layout together
        self.main_layout.addLayout(self.side_layout, 5)
        self.main_layout.addLayout(self.game_grid_layout, 95)
        self.setLayout(self.main_layout)

        # update score UI
        self.update_score_labels(self.score)

    def update_score_labels(self, score):

        self.score = score
        if score > self.highest_score:
            self.highest_score = score

        self.score_label.setText(f"Score : {str(self.score)}")
        self.highest_score_label.setText(f"Record Score : {str(self.highest_score)}")

    def reset_game(self):
        self.game_grid.reset_grid()
        self.game_grid.setFocus()
        self.game_grid.score_keeper.reset_score()
        self.update_score_labels(self.score)

        
