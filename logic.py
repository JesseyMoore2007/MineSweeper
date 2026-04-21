from PyQt6.QtCore import QTimer, QTime, Qt
from PyQt6.QtWidgets import *
from gui import *
import random
import csv

#End screen
#reset button
#Track best times


class Logic(QMainWindow, Ui_MainWindow):
    def __init__(self) -> None:
        #Basic initiations and variables
        super().__init__()
        self.setupUi(self)
        self.Win_Label.hide()
        self.page.showFullScreen()
        self.__flags:int = 3 #The amount of "flags" or mines
        self.time = QTime(0,0,0,0)
        self.timer = QTimer()
        self.__running:bool = True
        self.__timer_running:bool = False

        #set up grid in a list so I can later track mine positions and clicked locations
        self.grid_rows:list = ["A", "B", "C", "D", "E"]
        self.grid_columns:list = ["1", "2", "3", "4", "5"]
        self.grid:list = [[],[],[],[],[]]

        self.mines:list = [] #Which tiles are mines
        self.cleared:int = 0 #How many tiles are currently cleared
        self.safe_tiles:int = 22 #The amount of tiles that are safe based on the fact there are 3 mines (25 - 3)
        self.tiles_cleared:dict = {} #A dictionary to track which tile positions have already been clicked or not

        self.Flags_Label.setText(f"Mines: {self.__flags}")
        self.create_grid()
        self.Reset_Button.clicked.connect(lambda: self.create_grid())

        self.timer.timeout.connect(self.update_timer)



    def create_grid(self) -> None:
        '''
        Sets up the grid lists and the mine locations based on the grid
        :return:
        '''
        self.time = QTime(0,0,0,0)
        self.Timer_Label.setText(f"Time: 00:00:00")
        self.__running = True
        self.page_2.hide()
        self.page.showFullScreen()
        self.tiles_cleared.clear()
        self.cleared = 0

        first = True
        for button in self.gridLayoutWidget.children():
            if first:
                first = False
                continue
            button.clicked.connect(lambda: self.click())
            button.setText("")
            button.setStyleSheet("background-color: tan")


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
        '''
        Definately the most complex function here.
        This will check if a clicked button is a mine or not.
        mines will broadcast lose, otherwise the tile will be
        revealed.
        :return:
        '''
        if self.__running:
            if not self.__timer_running:
                self.timer.start(10)
            ##Set name of the button, and location of the tile on the grid
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

    def give_number(self, row, col) -> int:
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
        '''
        will click all adjacent tiles that aren't already revealed.
        :param row:
        :param col:
        :return:
        '''
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
        self.timer.stop()
        self.__timer_running = False
        self.page_2.showFullScreen()
        self.page.hide()
        self.Times_Label.setGeometry(QtCore.QRect(25, 60, 250, 20))
        self.Times_Label.setText(f"Your Time: {self.time.hour():02}:{self.time.minute():02}:{self.time.second():02}")
        with open("best_times.csv", "a", newline="") as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow([f"{self.time.hour():02}:{self.time.minute():02}:{self.time.second():02}"])
        with open("best_times.csv", "r", newline="") as csvfile:
            csv_reader = csv.reader(csvfile)
            first = None
            second = None
            third= None
            for time in csv_reader:
                if first == None:
                    first = time[0]
                    continue
                if time[0] < first:
                    third = second
                    second = first
                    first = time[0]
                elif time[0] < second:
                    third = second
                    second = time[0]
                elif time[0] < third:
                    third = time[0]
        self.Best_Times_Label.setText(f"Top 3 Times:\n{first:>12}\n{second:>12}\n{third:>12}")
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
        self.timer.stop()
        self.__timer_running = False
        self.page_2.showFullScreen()
        self.page.hide()
        self.Times_Label.setGeometry(QtCore.QRect(15, 60, 250, 20))
        self.Times_Label.setText(f"You lost! No time saved!")
        with open("best_times.csv", "r", newline="") as csvfile:
            csv_reader = csv.reader(csvfile)
            first = None
            second = None
            third= None
            for time in csv_reader:
                if first == None:
                    first = time[0]
                    continue
                if time[0] < first:
                    third = second
                    second = first
                    first = time[0]
                elif time[0] < second:
                    third = second
                    second = time[0]
                elif time[0] < third:
                    third = time[0]
        self.Best_Times_Label.setText(f"Top 3 Times:\n{first:>12}\n{second:>12}\n{third:>12}")
        self.Win_Label.show()
        self.Win_Label.setStyleSheet("color: maroon")
        self.Win_Label.setText("Lose!")
        self.__running = False

    def update_timer(self):
        self.__timer_running = True
        self.time = self.time.addMSecs(10)
        self.Timer_Label.setText(f"Time: {self.time.hour():02}:{self.time.minute():02}:{self.time.second():02}")
