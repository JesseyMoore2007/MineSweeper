from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import *
from gui import *
import random

class Logic(QMainWindow, Ui_MainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setupUi(self)
        self.Win_Label.hide()
        self.__flags:int = 3
        self.__time:int = 0
        self.__running:bool = True
        self.grid_rows:list = ["A", "B", "C", "D", "E"]
        self.grid_columns:list = ["1", "2", "3", "4", "5"]
        self.grid:list = [[],[],[],[],[]]
        self.mines:list = []
        self.cleared:int = 0
        self.safe_tiles:int = 22
        self.tiles_cleared:dict = {}
        self.Flags_Label.setText(f"Flags: {self.__flags}")

        first = True
        for button in self.gridLayoutWidget.children():
            if first:
                first = False
                continue
            button.clicked.connect(lambda: self.click())
            button.setStyleSheet("background-color: tan")

        self.create_grid()



    def create_grid(self) -> None:
        '''
        Sets up the grid lists and the mine locations based on the grid
        :return:
        '''
        letter = 0
        for row in self.grid:
            for col in range(5):
              row.append(self.grid_rows[letter] + (str(col+1)))
            letter += 1

        mine1 = random.choice(self.grid_rows) + random.choice(self.grid_columns)
        mine2 = random.choice(self.grid_rows) + random.choice(self.grid_columns)
        mine3 = random.choice(self.grid_rows) + random.choice(self.grid_columns)
        while mine1 == mine2 or mine1 == mine3 or mine2 == mine3:
            mine1 = random.choice(self.grid_rows) + random.choice(self.grid_columns)
            mine2 = random.choice(self.grid_rows) + random.choice(self.grid_columns)
            mine3 = random.choice(self.grid_rows) + random.choice(self.grid_columns)
        self.mines = [mine1, mine2, mine3]

        for row in self.grid:
            for col in row:
                if col not in self.mines:
                    self.tiles_cleared[col] = 0

        print(self.tiles_cleared)


    def click(self) -> None:
        if self.__running:
            button = self.sender()
            tile = button.objectName()
            if tile in self.mines:
                button.setStyleSheet("background-color: red")
                self.lose()
                return
            else:
                for row in self.grid:
                    for col in row:
                        if col == tile:
                            print(f"Location: {self.grid.index(row)} {row.index(col)}")
                            number = str(self.give_number(self.grid.index(row), row.index(col)))
                            print(f"Name: {tile}")
                            self.sender().setStyleSheet("background-color: brown")
                            self.sender().setText(number)
                            print(number)
                            self.tiles_cleared[tile] = 1
                            self.cleared = 0
                            for value in self.tiles_cleared.values():
                                if value == 1:
                                    self.cleared += 1
                                if self.cleared == self.safe_tiles:
                                    self.win()
                                    return
                            if number == "0":
                                print("breaking")
                                self.break_adjacent(self.grid.index(row), row.index(col))

                #print(tile)
                #button.setStyleSheet("background-color: brown")
                #button.setText()
                #return


    def give_number(self, row, col):
        '''
        This function returns the amount of mines around a clicked tile
        :param row:
        :param col:
        :return:
        '''
        number = 0
        places = [-1, 0, 1]
        print("-----")
        for i in places:
            if i == -1 and row == 0:
                continue
            if i == 1 and row == 4:
                continue
            for j in places:
                if j == -1 and col == 0:
                    continue
                if j == 1 and col == 4:
                    continue
                print(self.grid[row + i][col + j])
                if self.grid[row + i][col + j] in self.mines:
                    number += 1
        print("-----")
        return number

    def break_adjacent(self, row, col):
        places = [-1, 0, 1]
        for i in places:
            if i == -1 and row == 0:
                continue
            if i == 1 and row == 4:
                continue
            for j in places:
                if j == -1 and col == 0:
                    continue
                if j == 1 and col == 4:
                    continue
                #if self.give_number(row, col) == 0 and name not in self.mines:
                first = True
                for button in self.gridLayoutWidget.children():
                    if first:
                        first = False
                        continue
                    print(button.objectName())
                    print(self.grid[row+i][col+j])
                    if button.objectName() == self.grid[row+i][col+j] and self.tiles_cleared[button.objectName()] != 1:
                        print("clicked")
                        button.click()
        pass

    def win(self):
        '''
        will be called once all safe tiles have been pressed.
        Will make a cool little win text show up.
        :return:
        '''
        self.Win_Label.show()
        self.Win_Label.setStyleSheet("color: green")
        self.Win_Label.setText("Win!")
        self.__running = False

    def lose(self):
        '''
        Will be called if you hit a mine!
        Will make a cool little lose text show up.
        (It's still Win_Label, but nobody will know...)
        :return:
        '''
        self.Win_Label.show()
        self.Win_Label.setStyleSheet("color: maroon")
        self.Win_Label.setText("Lose!")
        self.__running = False