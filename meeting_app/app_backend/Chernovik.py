import smtplib

def send():
    smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
    smtpObj.starttls()
    smtpObj.login('denisburkovfortest@gmail.com','Denisfortest2022')
    msg = "test"
    smtpObj.sendmail("denisburkovfortest@gmail.com","wow-denis@mail.ru","test")
    smtpObj.quit()