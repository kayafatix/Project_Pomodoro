import sqlite3
from time import time
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QTableWidgetItem
from PyQt5.uic import loadUi
import sys 
import re
import threading
import time
import datetime
from PyQt5.QtCore import QTime, QTimer, QDate, Qt


po_session = 1

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
        
        def is_valid_email(email):
            if re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email):
                return True
            else:
                return False        

        if self.name == "" or self.user_email == "":
            self.errorTextSignUp.setText("'name' or 'email' fields cannot be left blank!")
        elif not is_valid_email(self.user_email):
            self.errorTextSignUp.setText("Sorry, your mail address is not valid.")
        else:
            with sqlite3.connect("pomodoro.db") as db:
                im = db.cursor()
                im.execute("SELECT * FROM users")
                e_mail = [i[2] for i in im.fetchall()]
                if self.user_email in e_mail:
                    self.errorTextSignUp.setText(f"The user '{self.user_email}' already exists.")
                else:
                    im.execute("INSERT INTO users(name, user_email) VALUES(?, ?)", (self.name, self.user_email))
                    db.commit()
                    self.errorTextSignUp.setText(f"The user '{self.user_email}' has been successfully registered.")
                    self.nameInputSignUp.clear()
                    self.emailInputSignUp.clear()     
        
    def login_button(self):
    
        with sqlite3.connect("pomodoro.db") as db:            
            im = db.cursor()    
            im.execute("SELECT * FROM users")
            self.login = self.emailInputLogin.text()
            
            for i in im.fetchall():
                im.execute("SELECT * FROM users")
                if self.login == "" or "@" not in self.login:
                    self.errorTextLogin.setText("For login please enter a valid email address!")                   
                
                elif self.login in i:
                    self.go_main_menu()
                    break                               

                else:
                    self.errorTextLogin.setText("Sorry, your email address is not registered!")

                    
    # =================================================================


class MainMenuUI(QDialog):
    
    def __init__(self, login):
        super(MainMenuUI, self).__init__()
        loadUi("UI//mainMenu.ui", self)
        self.login = login
        
        self.addProjectButton.clicked.connect(self.add_new_Project)
        self.addSubjectButton.clicked.connect(self.add_new_subject)
        self.addRecipientButton.clicked.connect(self.add_new_Recipient)
        
        self.startPomodoroButton.clicked.connect(self.go_pomodoro_menu)
        
        self.projectDeleteButton.clicked.connect(self.delete_project)
        self.subjectDeleteButton.clicked.connect(self.delete_subject)
        self.deleteRecipientButton.clicked.connect(self.delete_recipient_emails)

        # self.errorTextProjectLabel.setText("")
        self.errorTextSubjectLabel.setText("")
        self.errorTextRecipientsEmailLabel.setText("")
        self.selectProjectCombo.currentTextChanged.connect(self.updateSubjectCombo)
        self.projectDeleteCombo.currentTextChanged.connect(self.updateDeleteSubjectCombo)
        self.selectSubjectCombo.currentTextChanged.connect(self.updatecafercombo)
        self.showSummaryProjectCombo.currentTextChanged.connect(self.updateSummarySubjectCombo)
        self.showSummaryButton.clicked.connect(self.show_summary)
        

        query = "SELECT name FROM users WHERE user_email = ?"
        with sqlite3.connect("pomodoro.db") as db:
            cursor = db.cursor()
            cursor.execute(query, (self.login,))
            name = cursor.fetchone()[0]
        self.titleWorkspaceLabel.setText(f"{name}'s Workspace")

    # ---------------------------------------------------------------- ProjectComboBox1 ----------------------------------------------------------------
        query1 = "SELECT project_name FROM projects WHERE user_id = (SELECT user_id FROM users WHERE user_email = ?)"
        with sqlite3.connect("pomodoro.db") as db:
            cursor = db.cursor()
            cursor.execute(query1, (self.login,))
            projects = cursor.fetchall()
            for i in projects:                
                self.addSubjectOnProjectCombo.addItem(i[0])

    # ---------------------------------------------------------------- ProjectComboBox2 ----------------------------------------------------------------
        query2 = "SELECT project_name FROM projects WHERE user_id = (SELECT user_id FROM users WHERE user_email = ?)"
        with sqlite3.connect("pomodoro.db") as db:
            cursor = db.cursor()
            cursor.execute(query2, (self.login,))
            projects1 = cursor.fetchall()
            for i in projects1:
                # print(i)
                self.selectProjectCombo.addItem(i[0])
                self.projectDeleteCombo.addItem(i[0])

    # ---------------------------------------------------------------- Recipients Combobox ----------------------------------------------------------------

        query = "SELECT recipients_email FROM recipients"
        with sqlite3.connect("pomodoro.db") as db:
            cursor = db.cursor()
            cursor.execute(query)
            projects1 = cursor.fetchall()
            for i in projects1:
                # print(i)
                self.deleteRecipientCombo.addItem(i[0])

    # -------------------------------------------------------------Tracking History Filter (All / All / All)---------------------------------------------------------------------------------------
        with sqlite3.connect("pomodoro.db") as db:

            cursor = db.cursor()
            cursor.execute(f"SELECT date, start_time,end_time,success,failure FROM tracking_history WHERE user_id = (SELECT user_id FROM users WHERE user_email = '{self.login}')")
            rows = cursor.fetchall()
            row_count = len(rows)

            self.summaryTableValuesWidget.setRowCount(row_count)
            self.summaryTableValuesWidget.setColumnCount(5)

            for row in range(row_count):
                for col in range(5):
                    item = QTableWidgetItem(str(rows[row][col]))
                    self.summaryTableValuesWidget.setItem(row, col, item)    
    
    # -------------------------------------------------------------------Time Difference---------------------------------------------------------------
        with sqlite3.connect("pomodoro.db") as db:
            cursor = db.cursor()
            cursor.execute("SELECT start_time,end_time FROM tracking_history WHERE user_id = (SELECT user_id FROM users WHERE user_email = ?)",(self.login,))
            rows = cursor.fetchall()
            # print(rows)

        total_difference = datetime.timedelta()

        for i in rows:
            start_time = datetime.datetime.strptime(i[0], "%H:%M:%S")
            end_time = datetime.datetime.strptime(i[1], "%H:%M:%S")  
            time_difference = end_time - start_time  
            total_difference += time_difference

        # print(total_difference)
        self.totalTrackedTimeDurationLabel.setText(str(total_difference)) 
# -------------------------------------------------------------------------------------------------------------------------------------------------------
    
    def updateSubjectCombo(self, selectedProject):
            
            self.pomodoro_project = selectedProject

            # print(self.pomodoro_project)
            # self.pomodoro_project_method()
            with sqlite3.connect("pomodoro.db") as db:
                self.selectSubjectCombo.clear() 
                cursor = db.cursor()
                cursor.execute("SELECT subject_name FROM subjects WHERE project_id = (SELECT project_id FROM projects WHERE project_name = ?)", (selectedProject,))
                subjects = cursor.fetchall()

                for i in subjects:
                    # print(i)
                    self.selectSubjectCombo.addItem(i[0])

    def updatecafercombo(self,selectedSubject):

        self.currentsubject = selectedSubject

    # def pomodoro_project_method(self):
    #     print(self.pomodoro_project)
    # ---------------------------------------------------------------- SubjectDeleteComboBox ----------------------------------------------------------------
    def updateDeleteSubjectCombo(self, selected_Project):

        with sqlite3.connect("pomodoro.db") as db:            
            self.subjectDeleteCombo.clear()
            cursor1 = db.cursor()
            cursor1.execute("SELECT subject_name FROM subjects WHERE project_id = (SELECT project_id FROM projects WHERE project_name = ?)", (selected_Project,))
            subjects_delete = cursor1.fetchall()

            for i in subjects_delete:                                
                self.subjectDeleteCombo.addItem(i[0])

    # ---------------------------------------------------------------- SummaryProjectCombo ----------------------------------------------------------------
        query3 = "SELECT project_name FROM projects WHERE user_id = (SELECT user_id FROM users WHERE user_email = ?)"
        with sqlite3.connect("pomodoro.db") as db:
            cursor = db.cursor()
            cursor.execute(query3, (self.login,))
            self.project_summary = cursor.fetchall()
            self.showSummaryProjectCombo.addItem("All")
            for i in self.project_summary:
                # print(i)
                self.showSummaryProjectCombo.addItem(i[0])
    
    # ---------------------------------------------------------------- SummarySubjecttCombo ----------------------------------------------------------------

    def updateSummarySubjectCombo(self, selectedSummaryProject):
            # print(selectedSummaryProject)
            
            if selectedSummaryProject == "All":

                with sqlite3.connect("pomodoro.db") as db:
                    self.showSummarySubjectCombo.clear() 
                    cursor = db.cursor()
                    cursor.execute("SELECT subject_name FROM subjects WHERE user_id = (SELECT user_id FROM users WHERE user_email = ?)", (self.login,))
                    subjects = cursor.fetchall()
                    self.showSummarySubjectCombo.addItem("All")
                    # print(selectedSummaryProject)
                    for i in subjects:
                        # print(i)
                        self.showSummarySubjectCombo.addItem(i[0])

            else:
            
                with sqlite3.connect("pomodoro.db") as db:
                    self.showSummarySubjectCombo.clear() 
                    cursor = db.cursor()
                    cursor.execute("SELECT subject_name FROM subjects WHERE project_id = (SELECT project_id FROM projects WHERE project_name = ?)", (selectedSummaryProject,))
                    subjects = cursor.fetchall()
                    self.showSummarySubjectCombo.addItem("All")
                    # print(selectedSummaryProject)
                    for i in subjects:
                        # print(i)
                        self.showSummarySubjectCombo.addItem(i[0])
    
    # -----------------------------------------------------------------------------------------------------------------------------------------------------

    def add_new_Project(self):
        
        project_name = self.addProjectInput.text()
        with sqlite3.connect("pomodoro.db") as db:
            cursor_1 = db.cursor()
            cursor_1.execute("SELECT project_name FROM projects WHERE user_id = (SELECT user_id FROM users WHERE user_email = ?)",(self.login,))
            all_projects = [i[0] for i in cursor_1.fetchall()]
            # print(all_projects)
        
        if project_name == "":
            self.errorTextProjectLabel.setText("Enter a project name")
            QTimer.singleShot(1500, UI.go_main_menu)
        
        elif project_name in all_projects:
            self.errorTextProjectLabel.setText(f"{project_name} already exists")
            QTimer.singleShot(1500, UI.go_main_menu)
    
        else:
            
            with sqlite3.connect("pomodoro.db") as db:
                cursor = db.cursor()
                cursor.execute("SELECT user_id FROM users WHERE user_email = ?",(self.login,))
                user_id = cursor.fetchone()[0]
                im = db.cursor()
                im.execute("INSERT INTO projects(project_name, user_id) VALUES (?, ?)", (project_name, user_id))
            self.errorTextProjectLabel.setText(f"'{project_name}' successfully added.")
            QTimer.singleShot(1500, UI.go_main_menu)
            # UI.go_main_menu()
                   

    def add_new_subject(self):
        subject_name = self.addSubjectInput.text()
        
        with sqlite3.connect("pomodoro.db") as db:
            cursor_2 = db.cursor()
            cursor_2.execute("SELECT subject_name FROM subjects")
            all_subjects = [i[0] for i in cursor_2.fetchall()]
            print(subject_name)
            
            if subject_name == "":
                self.errorTextSubjectLabel.setText("enter a subject")
                QTimer.singleShot(1500, UI.go_main_menu)
            
            elif subject_name in all_subjects:
                self.errorTextSubjectLabel.setText("Subject already exists")
                QTimer.singleShot(1000, UI.go_main_menu)
            
            else:
                print("if worked")
                with sqlite3.connect("pomodoro.db") as db:
                    cursor = db.cursor()
                    cursor.execute("SELECT user_id FROM users WHERE user_email = ?",(self.login,))
                    user_id = cursor.fetchone()[0]

                    combotext = self.addSubjectOnProjectCombo.currentText()
                    cursor1 = db.cursor()
                    cursor1.execute("SELECT project_id FROM projects WHERE project_name = ?",(combotext,))
                    project_id = cursor1.fetchone()[0]
                    
                    print(subject_name, project_id, user_id)
                        
                    cursor2 = db.cursor()
                    cursor2.execute("INSERT INTO subjects(subject_name,user_id,project_id) VALUES (?,?,?)",(subject_name,user_id,project_id,))
                    self.errorTextSubjectLabel.setText("Subject added.")
                    QTimer.singleShot(1500, UI.go_main_menu)                    
                    

    def go_pomodoro_menu(self): #Start Pomodoro Button       

        pomodoro_menu = PomodoroUI(self.login,self.pomodoro_project,self.currentsubject)
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
        # print(combotext1)

        with sqlite3.connect("pomodoro.db") as db:

            cursor = db.cursor()
            cursor.execute("DELETE FROM subjects WHERE subject_name = ?", (combotext1,))

        # self.projectDeleteCombo.currentText.clear()
        UI.go_main_menu()


    def add_new_Recipient(self):
        recipient_email = self.addRecipientInput.text()
        is_valid_email = lambda recipient_email: True if re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', recipient_email) else False
           
        with sqlite3.connect("pomodoro.db") as db:
                cursor = db.cursor()
                cursor.execute("SELECT * FROM recipients")
                recipients_e_mail=[]
                for i in cursor.fetchall():
                    recipients_e_mail.append(i[1])
        
        if recipient_email == "":
            self.errorTextRecipientsEmailLabel.setText("Please enter an email")
            QTimer.singleShot(1500, UI.go_main_menu)
            
        else:
            if not is_valid_email(recipient_email):
                self.errorTextRecipientsEmailLabel.setText("Enter a valid email")
                QTimer.singleShot(1500, UI.go_main_menu)
        
            else:
                if recipient_email in recipients_e_mail:          
                    self.errorTextRecipientsEmailLabel.setText(f"{recipient_email} already exists")
                    QTimer.singleShot(1500, UI.go_main_menu)
        
                else:
                    with sqlite3.connect("pomodoro.db") as db:
                        cursor1 = db.cursor()                
                        cursor1.execute("INSERT INTO recipients(recipients_email) VALUES (?)", (recipient_email,))
                        # db.commit()
                        self.errorTextRecipientsEmailLabel.setText(f"The user '{recipient_email}' has been successfully added.")
                        QTimer.singleShot(1500, UI.go_main_menu)

        
    def delete_recipient_emails(self):
        combotext = self.deleteRecipientCombo.currentText()
         
        
        with sqlite3.connect("pomodoro.db") as db: 
            cursor = db.cursor()
            cursor.execute("DELETE FROM recipients WHERE recipients_email = ?", (combotext,))                  
            self.errorTextRecipientsEmailLabel.setText(f"{combotext} deleted successfully.")
            QTimer.singleShot(1500, UI.go_main_menu)

    def show_summary(self):

        project_combotext = self.showSummaryProjectCombo.currentText()
        subject_combotext = self.showSummarySubjectCombo.currentText()
        period = self.showSummaryPeriodCombo.currentText()

        Qtoday = QDate.currentDate()
        today = Qtoday.addDays(0)
        before1week = Qtoday.addDays(-7)
        before1month = Qtoday.addMonths(-1)



        if project_combotext == "All" and subject_combotext != "All":

            if period == "All":
                with sqlite3.connect("pomodoro.db") as db:

                    cursor = db.cursor()
                    cursor.execute(f"SELECT date, start_time,end_time,success,failure FROM tracking_history WHERE (subject_id = (SELECT subject_id FROM subjects WHERE subject_name = '{subject_combotext}'))")
                    rows = cursor.fetchall()
                    row_count = len(rows)

                    self.summaryTableValuesWidget.setRowCount(row_count)
                    self.summaryTableValuesWidget.setColumnCount(5)

                    for row in range(row_count):
                        for col in range(5):
                            item = QTableWidgetItem(str(rows[row][col]))
                            self.summaryTableValuesWidget.setItem(row, col, item)

            if period == "Today":
                with sqlite3.connect("pomodoro.db") as db:

                    cursor = db.cursor()
                    cursor.execute(f"SELECT date, start_time,end_time,success,failure FROM tracking_history WHERE (subject_id = (SELECT subject_id FROM subjects WHERE subject_name = '{subject_combotext}')) AND date = '{today.toString('dd-MM-yyyy')}'")
                    rows = cursor.fetchall()
                    row_count = len(rows)

                    self.summaryTableValuesWidget.setRowCount(row_count)
                    self.summaryTableValuesWidget.setColumnCount(5)

                    for row in range(row_count):
                        for col in range(5):
                            item = QTableWidgetItem(str(rows[row][col]))
                            self.summaryTableValuesWidget.setItem(row, col, item)
                    
            if period == "This week":
                with sqlite3.connect("pomodoro.db") as db:

                    cursor = db.cursor()
                    cursor.execute(f"SELECT date, start_time,end_time,success,failure FROM tracking_history WHERE (subject_id = (SELECT subject_id FROM subjects WHERE subject_name = '{subject_combotext}')) AND date BETWEEN '{before1week.toString('dd-MM-yyyy')}' AND '{today.toString('dd-MM-yyyy')}'")
                    rows = cursor.fetchall()
                    row_count = len(rows)

                    self.summaryTableValuesWidget.setRowCount(row_count)
                    self.summaryTableValuesWidget.setColumnCount(5)

                    for row in range(row_count):
                        for col in range(5):
                            item = QTableWidgetItem(str(rows[row][col]))
                            self.summaryTableValuesWidget.setItem(row, col, item)

            if period == "This month":
                with sqlite3.connect("pomodoro.db") as db:

                    cursor = db.cursor()
                    cursor.execute(f"SELECT date, start_time,end_time,success,failure FROM tracking_history WHERE (subject_id = (SELECT subject_id FROM subjects WHERE subject_name = '{subject_combotext}')) AND date BETWEEN '{before1month.toString('dd-MM-yyyy')}' AND '{today.toString('dd-MM-yyyy')}'")
                    rows = cursor.fetchall()
                    row_count = len(rows)

                    self.summaryTableValuesWidget.setRowCount(row_count)
                    self.summaryTableValuesWidget.setColumnCount(5)

                    for row in range(row_count):
                        for col in range(5):
                            item = QTableWidgetItem(str(rows[row][col]))
                            self.summaryTableValuesWidget.setItem(row, col, item)
        
        elif project_combotext == "All" and subject_combotext == "All":

            if period == "All":

                with sqlite3.connect("pomodoro.db") as db:

                    cursor = db.cursor()
                    cursor.execute(f"SELECT date, start_time,end_time,success,failure FROM tracking_history WHERE user_id = (SELECT user_id FROM users WHERE user_email = '{self.login}')")
                    rows = cursor.fetchall()
                    row_count = len(rows)

                    self.summaryTableValuesWidget.setRowCount(row_count)
                    self.summaryTableValuesWidget.setColumnCount(5)

                    for row in range(row_count):
                        for col in range(5):
                            item = QTableWidgetItem(str(rows[row][col]))
                            self.summaryTableValuesWidget.setItem(row, col, item)

            elif period == "Today":

                with sqlite3.connect("pomodoro.db") as db:

                    cursor = db.cursor()
                    cursor.execute(f"SELECT date, start_time,end_time,success,failure FROM tracking_history WHERE (user_id = (SELECT user_id FROM users WHERE user_email = '{self.login}')) AND date = '{today.toString('dd-MM-yyyy')}' ")
                    rows = cursor.fetchall()
                    row_count = len(rows)

                    self.summaryTableValuesWidget.setRowCount(row_count)
                    self.summaryTableValuesWidget.setColumnCount(5)

                    for row in range(row_count):
                        for col in range(5):
                            item = QTableWidgetItem(str(rows[row][col]))
                            self.summaryTableValuesWidget.setItem(row, col, item)

            elif period == "This week":


                with sqlite3.connect("pomodoro.db") as db:

                    cursor = db.cursor()
                    cursor.execute(f"SELECT date, start_time,end_time,success,failure FROM tracking_history WHERE (user_id = (SELECT user_id FROM users WHERE user_email = '{self.login}')) AND date BETWEEN '{before1week.toString('dd-MM-yyyy')}' AND '{today.toString('dd-MM-yyyy')}' ")
                    rows = cursor.fetchall()
                    row_count = len(rows)

                    self.summaryTableValuesWidget.setRowCount(row_count)
                    self.summaryTableValuesWidget.setColumnCount(5)

                    for row in range(row_count):
                        for col in range(5):
                            item = QTableWidgetItem(str(rows[row][col]))
                            self.summaryTableValuesWidget.setItem(row, col, item)

            elif period == "This month":

                with sqlite3.connect("pomodoro.db") as db:

                    cursor = db.cursor()
                    cursor.execute(f"SELECT date, start_time,end_time,success,failure FROM tracking_history WHERE (user_id = (SELECT user_id FROM users WHERE user_email = '{self.login}')) AND date BETWEEN '{before1month.toString('dd-MM-yyyy')}' AND '{today.toString('dd-MM-yyyy')}' ")
                    rows = cursor.fetchall()
                    row_count = len(rows)

                    self.summaryTableValuesWidget.setRowCount(row_count)
                    self.summaryTableValuesWidget.setColumnCount(5)

                    for row in range(row_count):
                        for col in range(5):
                            item = QTableWidgetItem(str(rows[row][col]))
                            self.summaryTableValuesWidget.setItem(row, col, item)


        elif project_combotext != "All" and subject_combotext == "All":


            if period == "All":

                with sqlite3.connect("pomodoro.db") as db:

                    cursor = db.cursor()
                    cursor.execute(f"SELECT date, start_time,end_time,success,failure FROM tracking_history WHERE (project_id = (SELECT project_id FROM projects WHERE project_name = '{project_combotext}'))")
                    rows = cursor.fetchall()
                    row_count = len(rows)

                    self.summaryTableValuesWidget.setRowCount(row_count)
                    self.summaryTableValuesWidget.setColumnCount(5)

                    for row in range(row_count):
                        for col in range(5):
                            item = QTableWidgetItem(str(rows[row][col]))
                            self.summaryTableValuesWidget.setItem(row, col, item)

            elif period == "Today":

                with sqlite3.connect("pomodoro.db") as db:

                    cursor = db.cursor()
                    cursor.execute(f"SELECT date, start_time,end_time,success,failure FROM tracking_history WHERE (project_id = (SELECT project_id FROM projects WHERE project_name = '{project_combotext}')) AND date = '{today.toString('dd-MM-yyyy')}'")
                    rows = cursor.fetchall()
                    row_count = len(rows)

                    self.summaryTableValuesWidget.setRowCount(row_count)
                    self.summaryTableValuesWidget.setColumnCount(5)

                    for row in range(row_count):
                        for col in range(5):
                            item = QTableWidgetItem(str(rows[row][col]))
                            self.summaryTableValuesWidget.setItem(row, col, item)

            elif period == "This week":

                with sqlite3.connect("pomodoro.db") as db:

                    cursor = db.cursor()
                    cursor.execute(f"SELECT date, start_time,end_time,success,failure FROM tracking_history WHERE (project_id = (SELECT project_id FROM projects WHERE project_name = '{project_combotext}')) AND date BETWEEN '{before1week.toString('dd-MM-yyyy')}' AND '{today.toString('dd-MM-yyyy')}'")
                    rows = cursor.fetchall()
                    row_count = len(rows)

                    self.summaryTableValuesWidget.setRowCount(row_count)
                    self.summaryTableValuesWidget.setColumnCount(5)

                    for row in range(row_count):
                        for col in range(5):
                            item = QTableWidgetItem(str(rows[row][col]))
                            self.summaryTableValuesWidget.setItem(row, col, item)

            elif period == "This month":

                with sqlite3.connect("pomodoro.db") as db:

                    cursor = db.cursor()
                    cursor.execute(f"SELECT date, start_time,end_time,success,failure FROM tracking_history WHERE (project_id = (SELECT project_id FROM projects WHERE project_name = '{project_combotext}')) AND date BETWEEN '{before1month.toString('dd-MM-yyyy')}' AND '{today.toString('dd-MM-yyyy')}'")
                    rows = cursor.fetchall()
                    row_count = len(rows)

                    self.summaryTableValuesWidget.setRowCount(row_count)
                    self.summaryTableValuesWidget.setColumnCount(5)

                    for row in range(row_count):
                        for col in range(5):
                            item = QTableWidgetItem(str(rows[row][col]))
                            self.summaryTableValuesWidget.setItem(row, col, item)

        else:

            if period == "All":

                with sqlite3.connect("pomodoro.db") as db:

                    cursor = db.cursor()
                    cursor.execute(f"SELECT date, start_time,end_time,success,failure FROM tracking_history WHERE (project_id = (SELECT project_id FROM projects WHERE project_name = '{project_combotext}')) AND (subject_id = (SELECT subject_id FROM subjects WHERE subject_name = '{subject_combotext}'))")
                    rows = cursor.fetchall()
                    row_count = len(rows)


                    self.summaryTableValuesWidget.setRowCount(row_count)
                    self.summaryTableValuesWidget.setColumnCount(5)

                    for row in range(row_count):
                        for col in range(5):
                            item = QTableWidgetItem(str(rows[row][col]))
                            self.summaryTableValuesWidget.setItem(row, col, item)


            elif period == "Today":

                with sqlite3.connect("pomodoro.db") as db:

                    cursor = db.cursor()
                    cursor.execute(f"SELECT date, start_time,end_time,success,failure FROM tracking_history WHERE (project_id = (SELECT project_id FROM projects WHERE project_name = '{project_combotext}')) AND (subject_id = (SELECT subject_id FROM subjects WHERE subject_name = '{subject_combotext}')) AND date = '{today.toString('dd-MM-yyyy')}'")
                    rows = cursor.fetchall()
                    row_count = len(rows)

                    self.summaryTableValuesWidget.setRowCount(row_count)
                    self.summaryTableValuesWidget.setColumnCount(5)

                    for row in range(row_count):
                        for col in range(5):
                            item = QTableWidgetItem(str(rows[row][col]))
                            self.summaryTableValuesWidget.setItem(row, col, item)

            elif period == "This week":

                with sqlite3.connect("pomodoro.db") as db:

                    cursor = db.cursor()
                    cursor.execute(f"SELECT date, start_time,end_time,success,failure FROM tracking_history WHERE (project_id = (SELECT project_id FROM projects WHERE project_name = '{project_combotext}')) AND (subject_id = (SELECT subject_id FROM subjects WHERE subject_name = '{subject_combotext}')) AND (date BETWEEN '{before1week.toString('dd-MM-yyyy')}' AND '{today.toString('dd-MM-yyyy')}')")
                    rows = cursor.fetchall()
                    row_count = len(rows)

                    self.summaryTableValuesWidget.setRowCount(row_count)
                    self.summaryTableValuesWidget.setColumnCount(5)

                    for row in range(row_count):
                        for col in range(5):
                            item = QTableWidgetItem(str(rows[row][col]))
                            self.summaryTableValuesWidget.setItem(row, col, item)

            elif period == "This month":

                with sqlite3.connect("pomodoro.db") as db:

                    cursor = db.cursor()
                    cursor.execute(f"SELECT date, start_time,end_time,success,failure FROM tracking_history WHERE (project_id = (SELECT project_id FROM projects WHERE project_name = '{project_combotext}')) AND (subject_id = (SELECT subject_id FROM subjects WHERE subject_name = '{subject_combotext}')) AND (date BETWEEN '{before1month.toString('dd-MM-yyyy')}' AND '{today.toString('dd-MM-yyyy')}')")
                    rows = cursor.fetchall()
                    row_count = len(rows)

                    self.summaryTableValuesWidget.setRowCount(row_count)
                    self.summaryTableValuesWidget.setColumnCount(5)

                    for row in range(row_count):
                        for col in range(5):
                            item = QTableWidgetItem(str(rows[row][col]))
                            self.summaryTableValuesWidget.setItem(row, col, item)

        
# =================================================================


class PomodoroUI(QDialog):

    def __init__(self,login,pomodoro_project,currentsubject):
        super(PomodoroUI,self).__init__()
        loadUi("UI//pomodoro.ui",self)

        self.login = login
        self.pomodoro_project = pomodoro_project
        self.currentsubject = currentsubject
        self.goToMainMenuButton.clicked.connect(UI.go_main_menu)
        self.startStopButton.clicked.connect(self.start_button)
        self.doneButton.clicked.connect(self.done_button)
        self.addTask.clicked.connect(self.add_task_button)
        # self.labelAsNotFinishedButton.connect(self.label_not_finished)
        self.sayac = 0
        self.numberOfSession.setText(f"{self.sayac+1}")

        self.count_minutes = 0  
        self.count_seconds = 5
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_count)

    # ---------------------------------------------------------------- TasksComboBox ----------------------------------------------------------------

        query = "SELECT task_name FROM tasks WHERE (subject_id = (SELECT subject_id FROM subjects WHERE subject_name = ?)) AND (user_id = (SELECT user_id FROM users WHERE user_email = ?))"
        with sqlite3.connect("pomodoro.db") as db:
            cursor = db.cursor()
            cursor.execute(query, (self.currentsubject,self.login,))
            projects = cursor.fetchall()
            for i in projects:
                self.tasksCombo.addItem(i[0])
                self.tasksCombo_2.addItem(i[0])
    # ---------------------------------------------------------------- TasksComboBox ----------------------------------------------------------------

        
    
        
    def start_button(self):
        self.startStopButton.setEnabled(False)
        self.timer.start(1000)

        with sqlite3.connect("pomodoro.db") as db:
            cursor = db.cursor()
            cursor.execute("SELECT user_id FROM users WHERE user_email = ?", (self.login,))
            user_id = cursor.fetchone()[0]

            cursor = db.cursor()
            cursor.execute("SELECT project_id FROM projects WHERE (project_name = ?) AND (user_id = (SELECT user_id FROM users WHERE user_email = ?))", (self.pomodoro_project,self.login,))
            project_id = cursor.fetchone()[0]
            

            cursor = db.cursor()
            cursor.execute("SELECT subject_id FROM subjects WHERE (subject_name = ?) AND (user_id = (SELECT user_id FROM users WHERE user_email = ?))", (self.currentsubject,self.login,))
            subject_id = cursor.fetchone()[0]


            if self.sayac % 2 == 0:
                self.im = db.cursor()
                
                self.im.execute("INSERT INTO tracking_history(user_id, start_time, project_id, subject_id, date) VALUES (?, ?, ?, ?, ?)", (user_id, PomodoroUI.show_time(self), project_id,subject_id,PomodoroUI.show_date(self),))
                
            else:
                PomodoroUI.done_button(self)
                self.sayac += 1
            

    def done_button(self):
        with sqlite3.connect("pomodoro.db") as db:

            curss = db.cursor()
            curss.execute("UPDATE tracking_history SET success = ?, end_time = ? WHERE tracking_history_id = (SELECT tracking_history_id FROM tracking_history ORDER BY tracking_history_id DESC LIMIT 1)", ("+",PomodoroUI.show_time(self),))
            self.timer.stop()
            self.accept()
        

        if po_session % 4 == 0:
                longbreak = LongBreakUI(self.login,self.pomodoro_project,self.currentsubject)
                widget.addWidget(longbreak)
                widget.setCurrentIndex(widget.currentIndex()+1)
                sayac()
        else:
            shortbreak = ShortBreakUI(self.login,self.pomodoro_project,self.currentsubject)
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
                with sqlite3.connect("pomodoro.db") as db:

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
        add_task = self.taskInput.text() 
        with sqlite3.connect("pomodoro.db") as db:

            cursor = db.cursor()
            cursor.execute("SELECT user_id FROM users WHERE user_email = ?",(self.login,))
            user_id = cursor.fetchone()[0]            
            
            cursor1 = db.cursor()
            cursor1.execute("SELECT project_id FROM projects WHERE project_name = ?",(self.pomodoro_project,))
            project_id = cursor1.fetchone()[0]

            cursor1 = db.cursor()
            cursor1.execute("SELECT subject_id FROM subjects WHERE subject_name = ?",(self.currentsubject,))
            subject_id = cursor1.fetchone()[0]

            im = db.cursor()
            im.execute("INSERT INTO tasks(user_id,project_id,subject_id,task_name) VALUES (?,?,?,?)",(user_id,project_id,subject_id,add_task,))

        QTimer.singleShot(500, lambda: MainMenuUI.go_pomodoro_menu(self))
    
    
    # def label_not_finished(self):
    #     with sqlite3.connect("pomodoro.db") as db:
    #         cursor = db.cursor()
    #         cursor.execute("UPDATE tracking_history SET failure = ?, end_time = ? WHERE tracking_history_id = (SELECT tracking_history_id FROM tracking_history ORDER BY tracking_history_id DESC LIMIT 1)", ("-",PomodoroUI.show_time(self),))
    #         self.timer.stop()
    #         self.accept()

        # print("not  finished")
        # MainMenuUI.go_pomodoro_menu(self)   

# =================================================================


class ShortBreakUI(QDialog):
    def __init__(self,login,pomodoro_project,currentsubject):
        super(ShortBreakUI,self).__init__()
        loadUi("UI//shortBreak.ui",self)
        
        self.login = login
        self.pomodoro_project = pomodoro_project
        self.currentsubject = currentsubject
        # self.currentsubject = currentsubject
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
            MainMenuUI.go_pomodoro_menu(self)
        else:
            if self.count_seconds == 0:
                self.count_minutes -= 1
                self.count_seconds = 59
            else:
                self.count_seconds -= 1
            self.timeLabel.setText(f"{self.count_minutes:01d}:{self.count_seconds:02d}")

    def skip_button(self):

        MainMenuUI.go_pomodoro_menu(self)

        # pomodoro_menu = PomodoroUI(self.login)
        # widget.addWidget(pomodoro_menu)
        # widget.setCurrentIndex(widget.currentIndex()+1)         


# =================================================================


class LongBreakUI(QDialog):
    def __init__(self,login,pomodoro_project,currentsubject):
        super(LongBreakUI,self).__init__()
        loadUi("UI//longBreak.ui",self)

        self.login = login
        self.pomodoro_project = pomodoro_project
        self.currentsubject = currentsubject
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
            MainMenuUI.go_pomodoro_menu(self)
        else:
            if self.count_seconds == 0:
                self.count_minutes -= 1
                self.count_seconds = 59
            else:
                self.count_seconds -= 1
            self.timeLabel.setText(f"{self.count_minutes:01d}:{self.count_seconds:02d}")

    def skip_button(self):

        MainMenuUI.go_pomodoro_menu(self)



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

