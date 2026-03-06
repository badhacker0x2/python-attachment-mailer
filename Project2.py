import smtplib
import os
import zipfile
import logging

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders


# -------- LOGGING SETUP --------
logging.basicConfig(
    filename="mail_log.txt",
    level=logging.INFO,
    format="%(asctime)s - %(message)s"
)


# -------- CREATE ZIP FILE --------
def create_zip(files, zip_name="attachments.zip"):
    with zipfile.ZipFile(zip_name, "w") as z:
        for file in files:
            z.write(file, os.path.basename(file))
    return zip_name


# -------- ATTACH FILE FUNCTION --------
def attach_files(msg, files):
    for file in files:
        with open(file, "rb") as attachment:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())

        encoders.encode_base64(part)

        part.add_header(
            "Content-Disposition",
            f"attachment; filename={os.path.basename(file)}"
        )

        msg.attach(part)


# -------- SEND EMAIL FUNCTION --------
def send_email(subject, message, sender, receiver, password, files=None):

    try:
        msg = MIMEMultipart()
        msg["From"] = sender
        msg["To"] = receiver
        msg["Subject"] = subject

        msg.attach(MIMEText(message, "plain"))

        if files:
            attach_files(msg, files)

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()

        server.login(sender, password)

        server.sendmail(sender, receiver, msg.as_string())

        server.quit()

        print("Email sent successfully!")
        logging.info(f"Email sent to {receiver}")

    except Exception as e:
        print("Error:", e)
        logging.error(f"Failed to send email: {e}")


# -------- USER INPUT --------
sender = input("Sender Email: ")
password = input("App Password: ")
receiver = input("Receiver Email: ")

subject = input("Subject: ")
message = input("Message: ")

print("\nAttachment Mode")
print("1 - Single File")
print("2 - Multiple Files")
print("3 - Zip Multiple Files")

choice = input("Choose option: ")

files = []

if choice == "1":
    file = input("Enter file path: ")
    files.append(file)

elif choice == "2":
    file_list = input("Enter file paths separated by comma: ")
    files = [f.strip() for f in file_list.split(",")]

elif choice == "3":
    file_list = input("Enter file paths separated by comma: ")
    file_paths = [f.strip() for f in file_list.split(",")]

    zip_file = create_zip(file_paths)
    files.append(zip_file)

send_email(subject, message, sender, receiver, password, files)