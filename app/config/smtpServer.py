import smtplib, ssl

class Mail:
    def __init__(self):
        self.port = 465 # Gmail com SSL
        self.smtpServerDomain = "smtp.gmail.com" # Gmail com SSL
        self.senderMail = "onglinkdev@gmail.com"
        self.password = "Developer123"

    def send(self, emails, subject, content):
        sslContext = ssl.create_default_context()
        service = smtplib.SMTP_SSL(self.smtpServerDomain, self.port, context=sslContext)
        service.login(self.senderMail, self.password)

        for email in emails:
            result = service.sendmail(self.senderMail, email, f"Subject: {subject}\n{content}")

        service.quit()