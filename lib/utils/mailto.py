import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

support_mail = "nadir.sm@gmail.com"
suport_mail_password = 'fdch1412!'
msg_from = "Medina from Hospytal Synergy"

texts = {
    0: """
          Bonjour {},

          Comme convenu, voici votre code pour valider votre inscription é la plateforme de collaboration médicale Hospital Synergy:

              code  : {}

          Je vous attends sur notre salon privée sur Discord pour me fournir cette info.

          Avec mes respectueux messages.

          Medina from Hospytal Synergy

        """
}


def mailto(dest, password, name, subject, purpose):
    msg = MIMEMultipart()
    msg['From'] = msg_from
    msg['To'] = dest
    msg['Subject'] = subject

    body = texts.get(purpose).format(name, password)

    msg.attach(MIMEText(body))
    mail = smtplib.SMTP('smtp.gmail.com', 587)
    mail.ehlo()
    mail.starttls()
    mail.login(support_mail, suport_mail_password)
    text = msg.as_string()
    mail.sendmail(support_mail, dest, text)
    mail.close()

    print(f"Mails envoyés à {name} avec le code suivant {password}!")
