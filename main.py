import click
import smtplib
import os
import time
import mimetypes
from tqdm import tqdm
from email import encoders
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase


@click.group()
def mycommands():
    pass


@click.command()
@click.option("--sender", prompt="Введіть пошту відправника", help="Пошта користувача.")
@click.option("--receiver", prompt="Введіть пошту одержувача", help="Пошта одержувача.")
@click.option("--password", prompt="Введіть пароль додатка", help="Пароль додатка.")
@click.option("--attachments", prompt="Папка з файлами", help="Папка з файлами для одержувача.", default="attachments",
              show_default=True)
@click.option("--title", prompt="Заголовок", help="Заголовок вiдправки пошти.", default="Заголовок")
@click.option("--text", prompt="Введіть текст для одержувача", help="Повiдомлення у виглядi тексту.", default="",
              show_default=False)
def send_email(sender, receiver, password, attachments, title, text=None):
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()

    try:
        server.login(sender, password)
        msg = MIMEMultipart()
        msg["From"] = sender
        msg["To"] = receiver
        msg["Subject"] = title

        if text:
            msg.attach(MIMEText(text))

        click.echo("Збір інформації...")
        for file in tqdm(os.listdir(attachments)):
            time.sleep(0.4)
            filename = os.path.basename(file)
            ftype, encoding = mimetypes.guess_type(file)
            file_type, subtype = ftype.split("/")

            with open(f"{attachments}/{file}", "rb") as f:
                file = MIMEBase(file_type, subtype)
                file.set_payload(f.read())
                encoders.encode_base64(file)

            file.add_header('content-disposition', 'attachment', filename=filename)
            msg.attach(file)

        click.echo("Вiдправка...")
        server.sendmail(sender, sender, msg.as_string())

        click.echo("Повідомлення успішно надіслано!")
    except Exception as err:
        click.echo(f"{err} \nМожливо, ви помилилися в якомусь ряду!")


mycommands.add_command(send_email)

if __name__ == "__main__":
    mycommands()
