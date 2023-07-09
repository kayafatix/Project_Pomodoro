import sqlite3
from time import time
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication
from PyQt5.uic import loadUi
import sys

# from PyQt5 import QtWidgets
# from PyQt5.QtWidgets import QDialog, QApplication
# from PyQt5.uic import loadUi

from PyQt5.QtCore import QTime, QTimer, QDate, Qt
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout

po_session = 0

def sayac():
    global po_session 
    po_session += 1
    # print(po_session)

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
            with sqlite3.connect("pomodoro.db") as db:
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
                    self.nameInputSignUp.clear()
                    self.emailInputSignUp.clear()
        else:
            self.errorTextSignUp.setText("Sorry, your mail address must include '@' character")
        
    def login_button(self):
        
        with sqlite3.connect("pomodoro.db") as db:
            
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
    # =================================================================


class MainMenuUI(QDialog):
    # addSubjectOnProjectCombo 
    def __init__(self, login):
        super(MainMenuUI, self).__init__()
        loadUi("UI//mainMenu.ui", self)
        self.login = login
        
        # self.titleWorkspaceLabel.setText(f"[{name}]'s Workspace")
        
        self.addProjectButton.clicked.connect(self.add_new_Project)
        self.addSubjectButton.clicked.connect(self.add_new_subject)
        self.addRecipientButton.clicked.connect(self.add_new_Recipient)
        
        self.startPomodoroButton.clicked.connect(self.start_pomodoro)
        
        self.projectDeleteButton.clicked.connect(self.delete_project)
        self.subjectDeleteButton.clicked.connect(self.delete_subject)

        self.errorTextSubjectLabel.setText("Enter a Subject")
        self.errorTextRecipientsEmailLabel.setText("Enter an email to add Recipients")
        
        
        self.selectProjectCombo.currentTextChanged.connect(self.updateSubjectCombo)
        self.projectDeleteCombo.currentTextChanged.connect(self.updateDeleteSubjectCombo)
        
        # self.db = None
        
        # query = "SELECT name FROM users WHERE user_id = ?"
        # with sqlite3.connect("pomodoro.db") as db:
        #     cursor = db.cursor()
        #     cursor.execute(query, (self.login,))
        #     name = cursor.fetchall()[0]
        #     print(name)
        #     # for i in projects: 
        #     #     self.addSubjectOnProjectCombo.addItem(i[0])

    # ---------------------------------------------------------------- ProjectComboBox1 ----------------------------------------------------------------
        query = "SELECT project_name FROM projects WHERE user_id = (SELECT user_id FROM users WHERE user_email = ?)"
        with sqlite3.connect("pomodoro.db") as db:
            cursor = db.cursor()
            cursor.execute(query, (self.login,))
            projects = cursor.fetchall()
            for i in projects: 
                self.addSubjectOnProjectCombo.addItem(i[0])

    # ---------------------------------------------------------------- ProjectComboBox2 ----------------------------------------------------------------
        query = "SELECT project_name FROM projects WHERE user_id = (SELECT user_id FROM users WHERE user_email = ?)"
        with sqlite3.connect("pomodoro.db") as db:
            cursor = db.cursor()
            cursor.execute(query, (self.login,))
            projects1 = cursor.fetchall()
            for i in projects1:
                # print(i)
                self.selectProjectCombo.addItem(i[0])
                self.projectDeleteCombo.addItem(i[0])

    # ---------------------------------------------------------------- ProjectComboBox2 ----------------------------------------------------------------
        
        



    # ---------------------------------------------------------------- SubjectComboBox ----------------------------------------------------------------
    def updateSubjectCombo(self, selectedProject):

        with sqlite3.connect("pomodoro.db") as db:
            self.selectSubjectCombo.clear() 
            cursor = db.cursor()
            cursor.execute("SELECT subject_name FROM subjects WHERE project_id = (SELECT project_id FROM projects WHERE project_name = ?)", (selectedProject,))
            subjects = cursor.fetchall()

            for i in subjects:
                # print(i)
                self.selectSubjectCombo.addItem(i[0])

    # ---------------------------------------------------------------- SubjectComboBox ----------------------------------------------------------------
    def updateDeleteSubjectCombo(self, selected_Project):

        with sqlite3.connect("pomodoro.db") as db:            
            self.subjectDeleteCombo.clear()
            cursor1 = db.cursor()
            cursor1.execute("SELECT subject_name FROM subjects WHERE project_id = (SELECT project_id FROM projects WHERE project_name = ?)", (selected_Project,))
            subjects_delete = cursor1.fetchall()

            for i in subjects_delete:                                
                self.subjectDeleteCombo.addItem(i[0])





    def add_new_Project(self):
        # showProjectComboBox0()
        project_name = self.addProjectInput.text()
        # print(LoginUI.user_name)
        with sqlite3.connect("pomodoro.db") as db:
            cursor = db.cursor()
            cursor.execute("SELECT user_id FROM users WHERE user_email = ?",(self.login,))
            user_id = cursor.fetchone()[0]
            im = db.cursor()
            im.execute("INSERT INTO projects(project_name, user_id) VALUES (?, ?)", (project_name, user_id))
        UI.go_main_menu()


        print(f"The Project named {project_name} has been successfully added.")

    def add_new_subject(self):
        subject_name = self.addSubjectInput.text()
        with sqlite3.connect("pomodoro.db") as db:
            cursor = db.cursor()
            cursor.execute("SELECT user_id FROM users WHERE user_email = ?",(self.login,))
            user_id = cursor.fetchone()[0]


            combotext = self.addSubjectOnProjectCombo.currentText()
            cursor1 = db.cursor()
            cursor1.execute("SELECT project_id FROM projects WHERE project_name = ?",(combotext,))
            project_id = cursor1.fetchone()[0]

            
            im = db.cursor()
            im.execute("INSERT INTO subjects(subject_name,user_id,project_id) VALUES (?,?,?)",(subject_name,user_id,project_id,))
        

        print(f"The Subject named {combotext} has been successfully added.")

    def start_pomodoro(self):        


        pomodoro_menu = PomodoroUI(self.login)
        widget.addWidget(pomodoro_menu)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def delete_project(self):

        combotext = self.projectDeleteCombo.currentText()



        with sqlite3.connect("pomodoro.db") as db:

            cursor2 = db.cursor()
            cursor2.execute("DELETE FROM subjects WHERE project_id = (SELECT project_id FROM projects WHERE project_name = ?)", (combotext,))
            
            cursor = db.cursor()
            cursor.execute("DELETE FROM projects WHERE project_name = ?",(combotext,))
            
        # self.projectDeleteCombo.currentText.clear()
        UI.go_main_menu()

    def delete_subject(self):
        combotext1 = self.subjectDeleteCombo.currentText()
        print(combotext1)

        with sqlite3.connect("pomodoro.db") as db:

            cursor = db.cursor()
            cursor.execute("DELETE FROM subjects WHERE subject_name = ?", (combotext1,))
                   
        # self.projectDeleteCombo.currentText.clear()
        UI.go_main_menu()

    def add_new_Recipient(self):
        self.recipients_email = self.addRecipientInput.text()
        
        # is_valid_email = lambda email: True if re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email) else False
        
        if self.recipients_email == "":
            self.errorTextRecipientsEmailLabel.setText("email fields cannot be left blank!")
            
        elif "@" in self.recipients_email:
            with sqlite3.connect("pomodoro.db") as db:
                cursor = db.cursor()
                cursor.execute("SELECT * FROM recipients")
                recipients_e_mail=[]
                for i in cursor.fetchall():
                    recipients_e_mail.append(i[1])
                # print( e_mail)
                if self.recipients_email in recipients_e_mail:
                    self.errorTextRecipientsEmailLabel.setText(f"The user '{self.recipients_email}' is already exist.")
                else:
                    cursor.execute("INSERT INTO recipients(recipients_email) VALUES (?)", (self.recipients_email,))
                    # db.commit()
                    self.errorTextRecipientsEmailLabel.setText(f"The user '{self.recipients_email}' has been successfully added.")
                    self.addRecipientInput.clear()
                    
        else:
            self.errorTextRecipientsEmailLabel.setText("Sorry, your mail address must include '@' character")
        
        UI.go_main_menu()


# =================================================================



class PomodoroUI(QDialog):

    def __init__(self,login):
        super(PomodoroUI,self).__init__()
        loadUi("UI//pomodoro.ui",self)

        
        self.login = login
        self.goToMainMenuButton.clicked.connect(UI.go_main_menu)
        self.startStopButton.clicked.connect(self.start_button)
        self.doneButton.clicked.connect(self.done_button)
        self.addTask.clicked.connect(self.add_task_button)

        self.count_minutes = 0  
        self.count_seconds = 5
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_count)



        # self.pomodoro_session = 0
        self.sayac = 0

    # ---------------------------------------------------------------- TasksComboBox ----------------------------------------------------------------

        query = "SELECT task_name FROM tasks WHERE user_id = (SELECT user_id FROM users WHERE user_email = ?)"
        with sqlite3.connect("pomodoro.db") as db:
            cursor = db.cursor()
            cursor.execute(query, (self.login,))
            projects = cursor.fetchall()
            for i in projects:
                self.tasksCombo.addItem(i[0])
    # ---------------------------------------------------------------- TasksComboBox ----------------------------------------------------------------







    def start_button(self):
        self.startStopButton.setEnabled(False)

        # sayac()
        # self.pomodoro_session += 1
        # print(self.pomodoro_session)

        self.timer.start(1000)
        

        with sqlite3.connect("pomodoro.db") as db:
            cursor = db.cursor()
            cursor.execute("SELECT user_id FROM users WHERE user_email = ?", (self.login,))
            user_id = cursor.fetchone()[0]

            cursor = db.cursor()
            cursor.execute("SELECT project_id FROM projects WHERE user_id = (SELECT user_id FROM users WHERE user_email = ?)", (self.login,))
            project_id = cursor.fetchone()[0]

            cursor = db.cursor()
            cursor.execute("SELECT subject_id FROM subjects WHERE user_id = (SELECT user_id FROM users WHERE user_email = ?)", (self.login,))
            subject_id = cursor.fetchone()[0]


            if self.sayac % 2 == 0:
                self.im = db.cursor()
                
                self.im.execute("INSERT INTO tracking_history(user_id, start_time, project_id, subject_id, date) VALUES (?, ?, ?, ?, ?)", (user_id, PomodoroUI.show_time(self), project_id,subject_id,PomodoroUI.show_date(self),))
                
            else:
                PomodoroUI.done_button(self)
                self.sayac += 1
            

    def done_button(self):
        # print("heyt")
        # self.timer.stop()
        # self.accept()
        with sqlite3.connect("pomodoro.db") as db:

            curss = db.cursor()
            curss.execute("UPDATE tracking_history SET success = ?, end_time = ? WHERE tracking_history_id = (SELECT tracking_history_id FROM tracking_history ORDER BY tracking_history_id DESC LIMIT 1)", ("+",PomodoroUI.show_time(self),))
            self.timer.stop()
            self.accept()
        

        if po_session == 4:
                longbreak = LongBreakUI(self.login)
                widget.addWidget(longbreak)
                widget.setCurrentIndex(widget.currentIndex()+1)
        else:
            shortbreak = ShortBreakUI(self.login)
            widget.addWidget(shortbreak)
            widget.setCurrentIndex(widget.currentIndex()+1)
            sayac()


    def show_time(self):

        self.current_time = QTime.currentTime()
        self.time_text = self.current_time.toString("hh:mm:ss")
        return self.time_text
    
    
    def update_count(self):
        if self.count_minutes == 0 and self.count_seconds == 0:
            self.timer.stop()
            self.accept()
            if po_session == 4:
                longBreak = LongBreakUI(self.login)
                widget.addWidget(longBreak)
                widget.setCurrentIndex(widget.currentIndex()+1)
            else:
                shortbreak = ShortBreakUI(self.login)
                widget.addWidget(shortbreak)
                widget.setCurrentIndex(widget.currentIndex()+1)
                sayac()
                PomodoroUI.done_button(self)
        else:
            if self.count_seconds == 0:
                self.count_minutes -= 1
                self.count_seconds = 59
            else:
                self.count_seconds -= 1
            self.timeLabel.setText(f"{self.count_minutes:01d}:{self.count_seconds:02d}")
        
    
    def show_date(self):
        self.current_date = QDate.currentDate()
        self.date_text = self.current_date.toString("dd-MM-yyyy")
        return self.date_text
    
    def add_task_button(self):
        combo = MainMenuUI(self.login)
        combotext = combo.selectProjectCombo.currentText()
        combotext1 = combo.selectSubjectCombo.currentText()
        add_task = self.taskInput.text()


        print(combotext,combotext1)

        with sqlite3.connect("pomodoro.db") as db:

            cursor = db.cursor()
            cursor.execute("SELECT user_id FROM users WHERE user_email = ?",(self.login,))
            user_id = cursor.fetchone()[0]            
            
            cursor1 = db.cursor()
            cursor1.execute("SELECT project_id FROM projects WHERE project_name = ?",(combotext,))
            project_id = cursor1.fetchone()[0]

            cursor1 = db.cursor()
            cursor1.execute("SELECT subject_id FROM subjects WHERE subject_name = ?",(combotext1,))
            subject_id = cursor1.fetchone()[0]

            im = db.cursor()
            im.execute("INSERT INTO tasks(user_id,project_id,subject_id,task_name) VALUES (?,?,?,?)",(user_id,project_id,subject_id,add_task,))
            
        




# =================================================================





class ShortBreakUI(QDialog):
    def __init__(self,login):
        super(ShortBreakUI,self).__init__()
        loadUi("UI//shortBreak.ui",self)
        
        self.login = login
        self.goToMainMenuButton.clicked.connect(UI.go_main_menu)
        self.startButton.clicked.connect(self.short_break)
        self.skipButton.clicked.connect(self.skip_button)

        self.count_minutes = 0  
        self.count_seconds = 4
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_count)
        
    def short_break(self):
        self.timer.start(1000)

    def update_count(self):
        if self.count_minutes == 0 and self.count_seconds == 0:
            self.timer.stop()
            self.accept()
            pomodoro_menu = PomodoroUI(self.login)
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

        pomodoro_menu = PomodoroUI(self.login)
        widget.addWidget(pomodoro_menu)
        widget.setCurrentIndex(widget.currentIndex()+1)         





# =================================================================





class LongBreakUI(QDialog):
    def __init__(self,login):
        super(LongBreakUI,self).__init__()
        loadUi("UI//longBreak.ui",self)

        self.login = login
        self.goToMainMenuButton.clicked.connect(UI.go_main_menu)
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
UI = LoginUI()
# UI = MainMenuUI("c@")
# UI = PomodoroUI("c@")
# UI = ShortBreakUI()
# UI = LongBreakUI()

widget = QtWidgets.QStackedWidget()
widget.addWidget(UI)
widget.setFixedWidth(800)
widget.setFixedHeight(600)
widget.setWindowTitle("Time Tracking App")
widget.show()
sys.exit(app.exec_())

