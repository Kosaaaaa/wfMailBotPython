import smtplib
import ssl
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import logging

class MyMail():

    def __init__(self, reciver, subject, body):
        self.reciver = reciver
        creds = self.read_creds()
        self.login = creds[0]
        self.passwd = creds[1]
        self.msg = MIMEMultipart('alternative')
        self.msg['Subject'] = subject
        self.msg.attach(MIMEText(body))
        logging.basicConfig(filename='mails.log', level='DEBUG', format='%(levelname)s-%(asctime)s: %(message)s')
    def read_creds(self):
        try:
            with open('creds.txt') as f:
                file = list(map(str.rstrip, f.readlines()))
                creds = [file[0], file[1]]
                return creds
        except FileNotFoundError:
            logging.critical('Creds file not found')
            print('Creds file not found')
    
    def sendIt(self):
        context = ssl.create_default_context()
        try:
            with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as server:
                server.login(self.login, self.passwd)
                server.sendmail(self.login, self.reciver, self.msg.as_string().encode('ascii'))
            #return 'Email sent ;)))'
            logging.info(f'Email sent to {self.reciver} ;)))')
        except smtplib.SMTPAuthenticationError:
            #return 'Auth error'
            logging.error('Auth error')
        except smtplib.SMTPConnectError:
            #return 'Connection error'
            logging.error('Connection error')


# Create email message with given name, surname and school class
# Function adds current date and returns complete message.
def get_PE_msg(name, surname, class_):
    return f'Zrealizowałem lekcję wf w dniu {datetime.now().strftime("%d.%m.%Y")}r.\n{surname} {name} {class_}'

def send_mail(reciver, subject, msg):
    MyMail(reciver, subject, msg).sendIt()

# This function checks if today is tuesday or wednesday to sent mail to right person
def main():
    if datetime.now().strftime('%a') == 'Tue':
        wf1 = MyMail('test1@test.pl', 'Obecność WF', get_PE_msg('Oskar', 'Kosobucki', '2P'))
        wf1.sendIt()
    elif datetime.now().strftime('%a') == 'Wed':
        wf2 = MyMail('test2@test.pl', 'Obecność WF', get_PE_msg('Oskar', 'Kosobucki', '2P'))
        wf2.sendIt()

if __name__ == '__main__':
    main()