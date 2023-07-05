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
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout, QComboBox


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

        if self.name == "" or self.user_email == "":
            self.errorTextSignUp.setText("'name' or 'email' fields cannot be left blank!")
            
        elif "@" in self.user_email:
            with sqlite3.connect("pomodoro_database.db") as db:
                im = db.cursor()
                im.execute("SELECT * FROM users")
                e_mail=[]
                for i in im.fetchall():
                    e_mail.append(i[2])
                # print( e_mail)
                if self.user_email in e_mail:
                    self.errorTextSignUp.setText(f"The user '{self.user_email}' is already exist.")
                else:
                    im.execute("INSERT INTO users(name,user_email) VALUES(?,?)",(self.name,self.user_email))
                    db.commit()
                    self.errorTextSignUp.setText(f"The user '{self.user_email}' has been successfully registered.")
             
        else:
            self.errorTextSignUp.setText("Sorry, your mail address must include '@' character")

    def login_button(self):
        
        with sqlite3.connect("pomodoro_database.db") as db:
            
            im = db.cursor()    
            im.execute("SELECT * FROM users")
            self.login = self.emailInputLogin.text()
            
            for i in im.fetchall():
                im.execute("SELECT * FROM users")
                # print(i)
                if self.login == "" or "@" not in self.login:
                    self.errorTextLogin.setText("For login please enter a valid email address!")
                
                elif self.login in i:
                    self.go_main_menu()
                    break
                                  
                else:
                    self.errorTextLogin.setText("Sorry, your email address is not registered!")

class MainMenuUI(QDialog):
    def __init__(self, login):
        super(MainMenuUI, self).__init__()
        loadUi("UI//mainMenu.ui", self)
        self.login = login
        self.addProjectButton.clicked.connect(self.add_new_Project)
        self.db = None
        
        self.selectProjectCombo = QComboBox(self)
        data = ['Project 11', 'Project 22', 'Project 33']    
        self.selectProjectCombo.addItems(data)  
        
        self.get_projects()
        
        # self.add_data_to_combobox()
        
    # def add_data_to_combobox(self):
    #     data = ['Project 11', 'Project 22', 'Project 33']

    #     self.selectProjectCombo.addItems(data)  
             
        
        # self.setWindowTitle("Projects")
        
        # self.connection = sqlite3.connect("pomodoro_database.db")
        # self.cursor = self.connection.cursor()
        
        # widget = QWidget()
        # layout = QVBoxLayout()
        # widget.setLayout(layout)
        
        # projects = self.get_projects("project_name")
        # combobox = self.selectProjectCombo()
        # # combobox.addItems(projects)
        # layout.addWidget(combobox)
        
        # self.setCentralWidget(widget)
    
    
 
    def add_new_Project(self):
        project_name = self.addProjectInput.text()
        # print(LoginUI.user_name)
        with sqlite3.connect("pomodoro_database.db") as db:
            cursor = db.cursor()
            cursor.execute("SELECT user_id FROM users WHERE user_email = ?",(self.login,))
            user_id = cursor.fetchone()[0]
            im = db.cursor()
            im.execute("INSERT INTO projects(project_name, user_id) VALUES (?, ?)", (project_name, user_id))
            db.commit()
        
        print(f"The Project named {project_name} has been successfully added.")
    
    
    
    def get_projects(self):
        with sqlite3.connect("pomodoro_database.db") as db:
            cursor = db.cursor()
            cursor.execute(f"SELECT * FROM projects")
            
            all_projects = self.cursor.fetchall()
            # my_projects = [veri[0] for veri in all_projects]
            # db.commit()
            print(all_projects)
    
    # def add_new_subject(self):
    #     subject_name = self.addSubjectInput.text()
    #     with sqlite3.connect("pomodoro_database.db") as db:
    #         cursor = db.cursor()
    #         cursor.execute("SELECT user_id FROM users WHERE user_email = ?",(self.login,))
    #         user_id = cursor.fetchone()[0]
    #         cursor.execute("SELECT project_id FROM projects WHERE user_id = ?",(self.login,))
    #         project_id = cursor.fetchone()[0]
    #         im = db.cursor()
    #         im.execute(" INSERT INTO subjects (subject_name, user_id, project_id) VALUES (?,?,?)",(subject_name,user_id, project_id))
    #         db.commit()
    
        

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