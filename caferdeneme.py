import sqlite3
from time import time
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication
from PyQt5.uic import loadUi
import sys

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication
from PyQt5.uic import loadUi

from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout

class LoginUI(QDialog):

    def __init__(self):
        super(LoginUI,self).__init__()
        loadUi("UI//login.ui",self)

        
        self.signUpButton.clicked.connect(self.sign_up_button)
        self.loginButton.clicked.connect(self.login_button)
        self.errorTextLogin.setText("")
        self.errorTextSignUp.setText("")
        
        self.db = None

        
    def go_main_menu(self):
        main_menu = MainMenuUI(self.login)
        widget.addWidget(main_menu)
        widget.setCurrentIndex(widget.currentIndex()+1)       

    def sign_up_button(self):
        self.name = self.nameInputSignUp.text()
        self.user_email = self.emailInputSignUp.text()

        if "@" in self.user_email:
            with sqlite3.connect("Database//caferdatabase.db") as db:
                im = db.cursor()
                im.execute("INSERT INTO users(name,user_email) VALUES(?,?)",(self.name,self.user_email))
                db.commit()
                print(f"The user named {self.name} has been successfully registered.")
        else:
            self.errorTextSignUp.setText("Sorry, your mail address must include '@' character")

    def login_button(self):
        with sqlite3.connect("Database//caferdatabase.db") as db:
            im = db.cursor()
            im.execute("SELECT * FROM users")

            self.login = self.emailInputLogin.text()
            print(self.login)
            for i in im.fetchall():
                im.execute("SELECT * FROM users")
                if self.login in i:
                    self.go_main_menu()
                    break
            else:
                if self.login == "":
                    self.errorTextLogin.setText("")
                else:
                    self.errorTextLogin.setText("Sorry, your email address is not registered")

class MainMenuUI(QDialog):
    def __init__(self, login):
        super(MainMenuUI, self).__init__()
        loadUi("UI//mainMenu.ui", self)
        self.login = login
        self.addProjectButton.clicked.connect(self.add_new_Project)
        self.db = None
 
    def add_new_Project(self):
        project_name = self.addProjectInput.text()
        # print(LoginUI.user_name)
        with sqlite3.connect("Database//caferdatabase.db") as db:
            cursor = db.cursor()
            cursor.execute("SELECT user_id FROM users WHERE user_email = ?",(self.login,))
            user_id = cursor.fetchone()[0]
            im = db.cursor()
            im.execute("INSERT INTO projects(project_name, user_id) VALUES (?, ?)", (project_name, user_id))
            db.commit()

        print(f"The Project named {project_name} has been successfully added.")

class PomodoroUI(QDialog):
    def __init__(self):
        super(PomodoroUI,self).__init__()
        loadUi("UI//pomodoro.ui",self)

        self.goToMainMenuButton.clicked.connect(LoginUI.go_main_menu)


class ShortBreakUI(QDialog):
    def __init__(self):
        super(ShortBreakUI,self).__init__()
        loadUi("UI//shortBreak.ui",self)

        self.goToMainMenuButton.clicked.connect(LoginUI.go_main_menu)
        self.startButton.clicked.connect(self.short_break)
        self.skipButton.clicked.connect(self.skip_button)

        self.count_minutes = 5  
        self.count_seconds = 0
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_count)
        
    def short_break(self):
        self.timer.start(1000)

    def update_count(self):
        if self.count_minutes == 0 and self.count_seconds == 0:
            self.timer.stop()
            self.accept()
            pomodoro_menu = PomodoroUI()
            widget.addWidget(pomodoro_menu)
            widget.setCurrentIndex(widget.currentIndex()+1)
        else:
            if self.count_seconds == 0:
                self.count_minutes -= 1
                self.count_seconds = 59
            else:
                self.count_seconds -= 1
            self.timeLabel.setText(f"{self.count_minutes:01d}:{self.count_seconds:02d}")

    def skip_button(self):

        pomodoro_menu = PomodoroUI()
        widget.addWidget(pomodoro_menu)
        widget.setCurrentIndex(widget.currentIndex()+1)         




class LongBreakUI(QDialog):
    def __init__(self):
        super(LongBreakUI,self).__init__()
        loadUi("UI//longBreak.ui",self)

        self.goToMainMenuButton.clicked.connect(LoginUI.go_main_menu)

        self.startButton.clicked.connect(self.long_break)
        self.skipButton.clicked.connect(self.skip_button)

        self.count_minutes = 30  
        self.count_seconds = 0
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_count)
        
    def long_break(self):
        self.timer.start(1000)

    def update_count(self):
        if self.count_minutes == 0 and self.count_seconds == 0:
            self.timer.stop()
            self.accept()
            pomodoro_menu = PomodoroUI()
            widget.addWidget(pomodoro_menu)
            widget.setCurrentIndex(widget.currentIndex()+1)
        else:
            if self.count_seconds == 0:
                self.count_minutes -= 1
                self.count_seconds = 59
            else:
                self.count_seconds -= 1
            self.timeLabel.setText(f"{self.count_minutes:01d}:{self.count_seconds:02d}")

    def skip_button(self):

        pomodoro_menu = PomodoroUI()
        widget.addWidget(pomodoro_menu)
        widget.setCurrentIndex(widget.currentIndex()+1)



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

