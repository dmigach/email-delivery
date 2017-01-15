import smtplib
import pandas
import random
import argparse
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

mail_text_template = "Hi, {}!\nHow are you?\n"
mail_html_template = """\
    <html>
      <head></head>
      <body>
        <p>Hi, {}!<br>
           How are you?<br>
        </p>
      </body>
    </html>
    """


def parse_arguments():
    parser = argparse.ArgumentParser(description='send e-mails to list'
                                                 ' of addresses')
    parser.add_argument('path_to_names',
                        type=str, help='path to names csv')
    parser.add_argument('path_to_smtp', type=str,
                        help='path to smtps')
    arguments = parser.parse_args()
    return arguments.path_to_names, arguments.path_to_smtp


def get_names(path):
    if not os.path.exists(path):
        print('Wrong names csv path')
        return None
    return pandas.read_csv(path)


def get_dataframe(path):
    if not os.path.exists(path):
        print('Wrong smtps csv path')
        return None
    return pandas.read_csv(path)


def compose_mail(receiver_name, smtp_login):
    mail_text = mail_text_template.format(receiver_name)
    mail_html = mail_html_template.format(receiver_name)
    mail = MIMEMultipart('alternative')
    mail['Subject'] = "Hello, {}!".format(receiver_name)
    mail['From'] = smtp_login
    mail['To'] = email_address
    part1 = MIMEText(mail_text, 'plain')
    part2 = MIMEText(mail_html, 'html')
    mail.attach(part1)
    mail.attach(part2)
    return mail


def get_random_smtp():
    smtp_number_to_use = random.randint(0, smtp_qnt - 1)
    return smtp_dataframe.ix[smtp_number_to_use]


def send_mail(smtp_data, mail):
    smtp_server = smtp_data['smtp']
    smtp_port = int(smtp_data['port'])
    smtp_login = smtp_data['login']
    smtp_password = smtp_data['pass']
    if smtp_port == 587:
        mail_server = smtplib.SMTP(smtp_server, smtp_port)
        mail_server.starttls()
        mail_server.ehlo()
    elif smtp_port == 465:
        mail_server = smtplib.SMTP_SSL('{}:{}'.format(smtp_server, smtp_port))
        mail_server.ehlo()
    mail_server.login(smtp_login, smtp_password)
    mail_server.sendmail(smtp_login, email_address, mail.as_string())
    mail_server.quit()

if __name__ == '__main__':
    names_path, smtp_path = parse_arguments()
    names_dataframe = get_names(names_path)
    smtp_dataframe = get_dataframe(smtp_path)
    smtp_qnt = len(smtp_dataframe)
    for index, row in names_dataframe.iterrows():
        name, email_address = row['name'], row['mail']
        random_smtp = get_random_smtp()
        mail_from = random_smtp['login']
        message = compose_mail(name, mail_from)
        send_mail(random_smtp, message)


