import smtplib
import os
from email.mime.text import MIMEText


def enviar_email(destinatario, codigo):
    # Configuração do servidor SMTP (use suas próprias credenciais)
    server = str(os.getenv('SMTP_SERVER'))
    port = str(os.getenv('SMTP_PORT'))
    user = str(os.getenv('SMTP_USER'))
    password = str(os.getenv('SMTP_PASS'))
    sender = str(os.getenv('SMTP_SENDER'))
    recipients = destinatario

    # Cria a mensagem
    msg = MIMEText(f'Seu código OTP é: {codigo}')
    msg['Subject'] = 'OTP Avantti'
    msg['From'] = sender
    msg['To'] = recipients

    # Envia o e-mail
    smtp = smtplib.SMTP(server, port)
    smtp.starttls()
    smtp.login(user, password)
    smtp.sendmail(sender, recipients, msg.as_string())
    smtp.quit()
