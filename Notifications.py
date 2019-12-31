import smtplib



class Notification:
    def __init__ (self, message):
         self.type = type
         self.receiver = "delchi1199@gmail.com"
         self.subject = "3D printing console"
         self.message = message
         self.sender = "mainlinuxcomputer@gmail.com"
         self.senderPasswd = "Atolloverde777"

    def send(self):
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.login(self.sender, self.senderPasswd)
        BODY = '\r\n'.join(['To: %s' % self.receiver,
                            'From: %s' % self.sender,
                            'Subject: %s' % self.subject,
                            '', self.message])


        server.sendmail(self.sender, [self.receiver], BODY)
        print ('email sent')

        server.quit()

def test():
    alert = Notification("SAS")
    alert.send()
