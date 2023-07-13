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
from email_sender import send_email

class LoginUI(QDialog):
    def __init__(self):
        super(LoginUI,self).__init__()
        loadUi("./UI/login.ui",self)
        self.signUpButton.clicked.connect(self.createuserfunc)
        # This is example of changing screen
        self.loginButton.clicked.connect(self.go_main_menu)
        
        
    def createuserfunc(self):
        name = self.nameInputSignUp.text()
        email = self.emailInputSignUp.text()
        
        if '@' not in email:
            self.errorTextSignUp.setText('Lütfen geçerli bir email adresi giriniz.')            
        else:
            print('Başarılı bir şekilde  isim:', name, ' ve email:',email, ' ile kayıt olundu')
        
    def go_main_menu(self):
        user = self.emailInputLogin.text()
        if len(user)==0 or '@' not in user :
            self.errorTextLogin.setText('Lütfen geçerli bir email adresi giriniz.')
        else:
            #conn= sqlite3.connect('data.db')
            #curr= conn.cursor()
            #query = 'SELECT email from ....'
            #curr.execute(query)
            #result_email= curr.fetchone()[0]
            #if result_email == email:
            if user=='ozcankursun@gmail.com':
                print('Başarılı bir şekilde giriş yapıldı.')
                main_menu = MainMenuUI()
                widget.addWidget(main_menu)
                widget.setCurrentIndex(widget.currentIndex()+1)
                
            else:
               self.errorTextLogin.setText('Bir hesabınız yoksa kayıt olunuz.')
            
           
                
        

class MainMenuUI(QDialog):
    #Bunu yapacagiz
    def __init__(self):
        super(MainMenuUI,self).__init__()
        loadUi("./UI/mainMenu.ui",self)
        self.addProjectButton.clicked.connect(self.send_email)
        # self.sendEmailThisSummaryButton.connect(self.send_email)
        
        
        
    def send_email(self):
        print("email sent")
        with sqlite3.connect("pomodoro.db") as db:
                cursor = db.cursor()
                cursor.execute("SELECT * FROM recipients")
                recipients_e_mail=[]
                
                for i in cursor.fetchall():
                    recipients_e_mail.append(i[1])
                
                cursor1 = db.cursor()
                cursor1.execute("SELECT * FROM users")
                users=cursor1.fetchall()
                
        send_email(recipient=recipients_e_mail[0], email=f"{users} merhaba")    
        
    

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