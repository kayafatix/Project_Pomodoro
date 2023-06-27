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
        loadUi("UI//login.ui",self)

        self.signUpButton.clicked.connect(self.sign_up_button)
        self.loginButton.clicked.connect(self.login_button)
        self.errorTextLogin.setText("")
        self.errorTextSignUp.setText("")
        
    def go_main_menu(self):
        main_menu = MainMenuUI()
        widget.addWidget(main_menu)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def sign_up_button(self):

        name = self.nameInputSignUp.text()
        user_email = self.emailInputSignUp.text()

        if "@" in user_email:
            db = sqlite3.connect("Database//users.db")
            im = db.cursor()
            im.execute("INSERT INTO users(name,user_email) VALUES(?,?)",(name,user_email))
            db.commit()
            print(f"The user named {name} has been successfully registered.")
        else:
            self.errorTextSignUp.setText("Sorry, your mail address must include '@' character")

    def login_button(self):

        db = sqlite3.connect("Database//users.db")
        im = db.cursor()
        im.execute("Select* FROM users")

        # print(im.fetchall())

        login = self.emailInputLogin.text()
        for i in im.fetchall():
            im.execute("Select* FROM users")
            if login in i: 
                    self.go_main_menu()
            else:
                self.errorTextLogin.setText("Sorry, your email address is not registered")  

class MainMenuUI(QDialog):
    def __init__(self):
        super(MainMenuUI,self).__init__()
        loadUi("UI//mainMenu.ui",self)

        # recipients_add = self.addRecipientInput.text() kullanılacak kod
        
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

class LongBreakUI(QDialog):
    def __init__(self):
        super(LongBreakUI,self).__init__()
        loadUi("UI//longBreak.ui",self)

        self.goToMainMenuButton.clicked.connect(LoginUI.go_main_menu)


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

