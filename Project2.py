import smtplib
import zipfile
import os

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders


def send_email(subject, message, from_email, to_email, password, files):
    try:
        # Create email container
        msg = MIMEMultipart()
        msg["From"] = from_email
        msg["To"] = to_email
        msg["Subject"] = subject

        # Attach message body
        msg.attach(MIMEText(message, "plain"))

        # Attach files
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

        # Connect to SMTP server
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()

        # Login
        server.login(from_email, password)

        # Send email
        server.sendmail(from_email, to_email, msg.as_string())

        print("Email sent successfully!")

        server.quit()

    except Exception as e:
        print("Error:", e)


# -------- ZIP CREATION FUNCTION --------
def create_zip(files, zip_name="files.zip"):
    with zipfile.ZipFile(zip_name, "w") as z:
        for file in files:
            z.write(file)
    return zip_name


# -------- USER INPUT --------
from_email = input("Sender Email: ")
password = input("App Password: ")
to_email = input("Receiver Email: ")

subject = input("Subject: ")
message = input("Message: ")

print("\nAttachment Mode:")
print("1. Single file")
print("2. Multiple files")
print("3. Zip multiple files")

choice = input("Choose option (1/2/3): ")

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

else:
    print("Invalid choice")

send_email(subject, message, from_email, to_email, password, files)