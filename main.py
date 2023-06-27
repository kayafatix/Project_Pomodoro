import sqlite3
from time import time
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication
from PyQt5.uic import loadUi
import sys

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication
from PyQt5.uic import loadUi

class LoginUI(QDialog):
    def __init__(self):
        super(LoginUI,self).__init__()
        loadUi("./UI/login.ui",self)

        # This is example of changing screen
        self.loginButton.clicked.connect(self.go_main_menu)

    def go_main_menu(self):
        main_menu = MainMenuUI()
        widget.addWidget(main_menu)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def sign_up_button(self):

        name = self.nameInputSignUp.text()
        user_email = self.emailInputSignUp.text()

        if "@" in user_email:
            db = sqlite3.connect("C://Users//cfrdm//Desktop//ViT//Pomodoro Project//Database//users.db")
            im = db.cursor()
            im.execute("INSERT INTO users(name,user_email) VALUES(?,?)",(name,user_email))
            db.commit()
            print(f"The user named {name} has been successfully registered.")
        else:
            print("eksik veri girişi")


class MainMenuUI(QDialog):
    def __init__(self):
        super(MainMenuUI,self).__init__()
        loadUi("./UI/mainMenu.ui",self)

class PomodoroUI(QDialog):
    def __init__(self):
        super(PomodoroUI,self).__init__()
        loadUi("./UI/pomodoro.ui",self)


class ShortBreakUI(QDialog):
    def __init__(self):
        super(ShortBreakUI,self).__init__()
        loadUi("./UI/shortBreak.ui",self)

class LongBreakUI(QDialog):
    def __init__(self):
        super(LongBreakUI,self).__init__()
        loadUi("./UI/longBreak.ui",self)


app = QApplication(sys.argv)
UI = LoginUI() # This line determines which screen you will load at first

# You can also try one of other screens to see them.
    # UI = MainMenuUI()
    # UI = PomodoroUI()
    # UI = ShortBreakUI()
    # UI = LongBreakUI()

widget = QtWidgets.QStackedWidget()
widget.addWidget(UI)
widget.setFixedWidth(800)
widget.setFixedHeight(600)
widget.setWindowTitle("Time Tracking App")
widget.show()
sys.exit(app.exec_())
