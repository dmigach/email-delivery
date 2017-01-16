import smtplib
import csv
import random
import argparse
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

SUBJECT = 'Hello'


def parse_arguments():
    parser = argparse.ArgumentParser(description='send e-mails to list'
                                                 ' of addresses')
    parser.add_argument('path_to_names',
                        type=str, help='path to names csv')
    parser.add_argument('path_to_smtp', type=str,
                        help='path to smtps')
    parser.add_argument('path_to_html_template', type=str, help='path to html'
                                                                'template')
    arguments = parser.parse_args()
    return (arguments.path_to_names,
            arguments.path_to_smtp,
            arguments.path_to_html_template)


def get_names(path):
    if not os.path.exists(path):
        return None
    else:
        with open(path, 'r') as csvfile:
            names = csv.DictReader(csvfile, delimiter=',')
            names_mails_list = [x for x in names]
    return names_mails_list


def get_smtps(path):
    if not os.path.exists(path):
        return None
    else:
        with open(path, 'r') as csvfile:
            smtps = csv.DictReader(csvfile, delimiter=',')
            smtps_list = [x for x in smtps]
    return smtps_list


def get_html_template(path):
    if os.path.exists(path):
        with open(path, 'r') as file_handler:
            return file_handler.read()


def compose_mail(receiver_name, receiver_address, from_name,
                 html_template, subject):
    mail_html = html_template.format(subject=subject, name=receiver_name)
    mail = MIMEMultipart('alternative')
    mail['Subject'] = subject
    mail['From'] = from_name
    mail['To'] = receiver_address
    mail.attach(MIMEText(mail_html, 'html'))
    return mail


def get_random_smtp(smtps_list, smtp_number):
    smtp_number_to_use = random.randint(0, smtp_number - 1)
    return smtps_list[smtp_number_to_use]


def send_mail(smtp_data, mail, receiver_address):
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
    mail_server.sendmail(smtp_login, receiver_address, mail.as_string())
    mail_server.quit()

if __name__ == '__main__':
    names_path, smtp_path, html_template_path = parse_arguments()

    mail_html_template = get_html_template(html_template_path)
    names_list = get_names(names_path)
    smtp_list = get_smtps(smtp_path)

    if names_list and smtp_list and mail_html_template:
        smtp_qnt = len(smtp_list)
        for address in names_list:
            name, email_address = address['name'], address['mail']
            random_smtp = get_random_smtp(smtp_list, smtp_qnt)
            mail_from = random_smtp['login']
            message = compose_mail(name, email_address, mail_from,
                                   mail_html_template, SUBJECT)
            send_mail(random_smtp, message, email_address)
        print('Successful')
    else:
        print('Check files paths')
