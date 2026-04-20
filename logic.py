from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import *
from gui import *
import random

class Logic(QMainWindow, Ui_MainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setupUi(self)
        self.__flags:int = 3
        self.__time:int = 0
        self.__running:bool = True
        self.grid_rows:list = ["A", "B", "C", "D", "E"]
        self.grid_columns:list = ["1", "2", "3", "4", "5"]
        self.grid:list = [[],[],[],[],[]]
        self.mines:list = []

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
            for i in range(5):
              row.append(self.grid_rows[letter] + (str(i+1)))
            letter += 1

        mine1 = random.choice(self.grid_rows) + random.choice(self.grid_columns)
        mine2 = random.choice(self.grid_rows) + random.choice(self.grid_columns)
        mine3 = random.choice(self.grid_rows) + random.choice(self.grid_columns)
        while mine1 == mine2 or mine1 == mine3 or mine2 == mine3:
            mine1 = random.choice(self.grid_rows) + random.choice(self.grid_columns)
            mine2 = random.choice(self.grid_rows) + random.choice(self.grid_columns)
            mine3 = random.choice(self.grid_rows) + random.choice(self.grid_columns)
        self.mines = [mine1, mine2, mine3]

    def click(self) -> None:
        button = self.sender()
        tile = button.objectName()
        if tile in self.mines:
            button.setStyleSheet("background-color: red")
            return
        else:
            for row in self.grid:
                for col in row:
                    if col == tile:
                        print(f"Location: {self.grid.index(row)} {row.index(col)}")
                        number = str(self.give_number(tile, self.grid.index(row), row.index(col)))
                        print(f"Name: {tile}")
                        self.sender().setStyleSheet("background-color: brown")
                        self.sender().setText(number)
                        return
            #print(tile)
            #button.setStyleSheet("background-color: brown")
            #button.setText()
            #return


    def give_number(self, tile, row, col):
        '''
        This function returns the amount of mines around a clicked tile
        :param tile:
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

        '''
            for row in self.grid:
                for col in row:
                    if row[col] == tile:
                        #number = self.give_number(tile, row, col)
                        number = 1
                        print(tile)
                        self.sender().setStyleSheet("background-color: brown")
                        self.sender().setText(number)
                        return
    '''