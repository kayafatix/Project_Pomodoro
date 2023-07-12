import sqlite3
from smtplib import SMTP 

#import mail_password
#self.sendEmailSummaryButton.clicked.connect(self.resipient_email_send)

# def resipient_email_send(self):
#     recipientMailAdress = self.addRecipientInput.text()

with sqlite3.connect("pomodoro.db") as db:
    cursor = db.cursor()   # user_name, project_name date,start_time,end_time,success,failure  (self.login,)
    cursor.execute("SELECT date,start_time,end_time,success,failure FROM tracking_history WHERE user_id = (SELECT user_id FROM users WHERE user_email = 'c@')")
    message= [i for i in cursor.fetchall()]
    print(message)
    # try:
    #     message = # database den al
    #     subject = "Show Summery"
    #     message = msg
    #     content = (f"subject : {subject} \n\n {message}")

    #     mymail = "aaa.mail"#mail ve password baska bir py dosyasinda nickname ile import edilebilir.
    #     password = "aaa_password " # google oturum acma 2 adimda dogrulama acik olmali uygulama sifreleri bolumunden sifre al

    #     send_to = recipientMailAdress # kime gonderilecek
    #     mail = smtp("smtp.gmail.com",587)
    #     mail.ehlo()# maile baglan
    #     mail.starttls() #mail mesajini sifreler
    #     mail.login(mymail,password)
    #     mail.sendmail(mymail,send_to,content.encode("utf-8") # gonderen(mymail),kime (send-to),ne gidecek(content)
    #     print("mesaj gonderildi"))
    # except:
    #     print("Hata !!! Mesaj gonderilemedi....")    