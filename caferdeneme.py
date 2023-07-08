import sqlite3
from time import time
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QTableWidgetItem
from PyQt5.uic import loadUi
import sys


from PyQt5.QtCore import QTime, QTimer, QDate, Qt
# from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout

po_session = 1

def sayac():
    global po_session 
    po_session += 1
    print(po_session)

class LoginUI(QDialog):

    def __init__(self):
        super(LoginUI,self).__init__()
        loadUi("UI//login.ui",self)
        self.signUpButton.clicked.connect(self.sign_up_button)
        self.loginButton.clicked.connect(self.login_button)
        self.errorTextLogin.setText("")
        self.errorTextSignUp.setText("")
    
        
        self.db = None
        "merhaba saban abi"
        
    def go_main_menu(self):
        main_menu = MainMenuUI(self.login)
        widget.addWidget(main_menu)
        widget.setCurrentIndex(widget.currentIndex()+1)       

    # def sign_up_button(self):
    #     self.name = self.nameInputSignUp.text()
    #     self.user_email = self.emailInputSignUp.text()

    #     if "@" in self.user_email:
    #         with sqlite3.connect("Database//caferdatabase.db") as db:
    #             im = db.cursor()
    #             im.execute("INSERT INTO users(name,user_email) VALUES(?,?)",(self.name,self.user_email))
            
    #             print(f"The user named {self.name} has been successfully registered.")
    #     else:
    #         self.errorTextSignUp.setText("Sorry, your mail address must include '@' character")
    def sign_up_button(self):
        self.name = self.nameInputSignUp.text()
        self.user_email = self.emailInputSignUp.text()

        if self.name == "" or self.user_email == "":
            self.errorTextSignUp.setText("'name' or 'email' fields cannot be left blank!")
            
        elif "@" in self.user_email:
            with sqlite3.connect("Database//caferdatabase.db") as db:
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
        
        with sqlite3.connect("Database//caferdatabase.db") as db:
            
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
        self.addProjectButton.clicked.connect(self.add_new_Project)
        self.startPomodoroButton.clicked.connect(self.start_pomodoro)
        self.addSubjectButton.clicked.connect(self.add_new_subject)
        self.projectDeleteButton.clicked.connect(self.delete_project)

        self.errorTextSubjectLabel.setText("")
        self.selectProjectCombo.currentTextChanged.connect(self.updateSubjectCombo)

        self.showSummaryButton.clicked.connect(self.show_summary)
        
        # self.db = None

    # ---------------------------------------------------------------- ProjectComboBox1 ----------------------------------------------------------------
        query = "SELECT project_name FROM projects WHERE user_id = (SELECT user_id FROM users WHERE user_email = ?)"
        with sqlite3.connect("Database//caferdatabase.db") as db:
            cursor = db.cursor()
            cursor.execute(query, (self.login,))
            projects = cursor.fetchall()
            for i in projects: 
                self.addSubjectOnProjectCombo.addItem(i[0])

    # ---------------------------------------------------------------- ProjectComboBox1 ----------------------------------------------------------------






    # ---------------------------------------------------------------- ProjectComboBox2 ----------------------------------------------------------------
        query = "SELECT project_name FROM projects WHERE user_id = (SELECT user_id FROM users WHERE user_email = ?)"
        with sqlite3.connect("Database//caferdatabase.db") as db:
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

        with sqlite3.connect("Database//caferdatabase.db") as db:
            self.selectSubjectCombo.clear() 
            cursor = db.cursor()
            cursor.execute("SELECT subject_name FROM subjects WHERE project_id = (SELECT project_id FROM projects WHERE project_name = ?)", (selectedProject,))
            subjects = cursor.fetchall()

            for i in subjects:
                # print(i)
                self.selectSubjectCombo.addItem(i[0])

    # ---------------------------------------------------------------- SubjectComboBox ----------------------------------------------------------------






    def add_new_Project(self):
        # showProjectComboBox0()
        project_name = self.addProjectInput.text()
        # print(LoginUI.user_name)
        with sqlite3.connect("Database//caferdatabase.db") as db:
            cursor = db.cursor()
            cursor.execute("SELECT user_id FROM users WHERE user_email = ?",(self.login,))
            user_id = cursor.fetchone()[0]
            im = db.cursor()
            im.execute("INSERT INTO projects(project_name, user_id) VALUES (?, ?)", (project_name, user_id))
        UI.go_main_menu()


        print(f"The Project named {project_name} has been successfully added.")

    def add_new_subject(self):
        subject_name = self.addSubjectInput.text()
        with sqlite3.connect("Database//caferdatabase.db") as db:
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



        with sqlite3.connect("Database//caferdatabase.db") as db:

            cursor2 = db.cursor()
            cursor2.execute("DELETE FROM subjects WHERE project_id = (SELECT project_id FROM projects WHERE project_name = ?)", (combotext,))

            cursor = db.cursor()
            cursor.execute("DELETE FROM projects WHERE project_name = ?",(combotext,))
            
        # self.projectDeleteCombo.currentText.clear()
        UI.go_main_menu()




    def show_summary(self):
        # Veritabanı bağlantısını açın
        # connection = sqlite3.connect("veritabani.db")
        # cursor = connection.cursor()
        with sqlite3.connect("Database//caferdatabase.db") as db:
            cursor = db.cursor()

            # # Tablo adını ve sütun sayısını alın
            # table_name = "tracking_history"
            # cursor.execute(f"PRAGMA table_info({table_name})")
            # columns = cursor.fetchall()
            # column_count = len(columns)

            # Tablo içeriğini alın
            cursor.execute(f"SELECT date, start_time,end_time,success,failure FROM tracking_history")
            rows = cursor.fetchall()
            row_count = len(rows)

            # Tablo boyutunu ayarlayın
            self.summaryTableValuesWidget.setRowCount(row_count)
            self.summaryTableValuesWidget.setColumnCount(5)

            # Hücrelere verileri yerleştirin
            for row in range(row_count):
                for col in range(5):
                    item = QTableWidgetItem(str(rows[row][col]))
                    self.summaryTableValuesWidget.setItem(row, col, item)







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
        

    # ---------------------------------------------------------------- TasksComboBox ----------------------------------------------------------------

        query = "SELECT task_name FROM tasks WHERE user_id = (SELECT user_id FROM users WHERE user_email = ?)"
        with sqlite3.connect("Database//caferdatabase.db") as db:
            cursor = db.cursor()
            cursor.execute(query, (self.login,))
            projects = cursor.fetchall()
            for i in projects:
                self.tasksCombo.addItem(i[0])
    # ---------------------------------------------------------------- TasksComboBox ----------------------------------------------------------------






        self.sayac = 0
    def start_button(self):
        self.startStopButton.setEnabled(False)

        self.timer.start(1000)
        

        with sqlite3.connect("Database//caferdatabase.db") as db:
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
        with sqlite3.connect("Database//caferdatabase.db") as db:

            curss = db.cursor()
            curss.execute("UPDATE tracking_history SET success = ?, end_time = ? WHERE tracking_history_id = (SELECT tracking_history_id FROM tracking_history ORDER BY tracking_history_id DESC LIMIT 1)", ("+",PomodoroUI.show_time(self),))
            self.timer.stop()
            self.accept()
        

        if po_session % 4 == 0:
                longbreak = LongBreakUI(self.login)
                widget.addWidget(longbreak)
                widget.setCurrentIndex(widget.currentIndex()+1)
                sayac()
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
            if po_session % 4 == 0:
                    longBreak = LongBreakUI(self.login)
                    widget.addWidget(longBreak)
                    widget.setCurrentIndex(widget.currentIndex()+1)
                    sayac()
            else:
                shortbreak = ShortBreakUI(self.login)
                widget.addWidget(shortbreak)
                widget.setCurrentIndex(widget.currentIndex()+1)
                sayac()
                with sqlite3.connect("Database//caferdatabase.db") as db:

                    curss = db.cursor()
                    curss.execute("UPDATE tracking_history SET success = ?, end_time = ? WHERE tracking_history_id = (SELECT tracking_history_id FROM tracking_history ORDER BY tracking_history_id DESC LIMIT 1)", ("+",PomodoroUI.show_time(self),))
                    self.timer.stop()
                    self.accept()
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

        with sqlite3.connect("Database//caferdatabase.db") as db:

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

