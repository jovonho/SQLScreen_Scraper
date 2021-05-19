import smtplib, ssl, argparse, os
from pathlib import Path
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import formatdate
from email import encoders


def send_email(filename):
    port = 587  # For starttls
    smtp_server = "smtp.gmail.com"
    sender_email = "loic.hovon@gmail.com"
    receiver_email = "loic.hovon@gmail.com"
    password = os.environ.get("TMXSCRAPE_EMAILPASS")
    # TODO: Validate results and say if successful or not
    body = "Here's today's scraping log."

    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg["Date"] = formatdate(localtime=True)
    msg["Subject"] = "TMX Scrape Result"

    msg.attach(MIMEText(body))

    part = MIMEBase("application", "octet-stream")

    with open(filename, "rb") as file:
        part.set_payload(file.read())
    encoders.encode_base64(part)
    part.add_header("Content-Disposition", 'attachment; filename="{}"'.format(Path(filename).name))
    msg.attach(part)

    context = ssl.create_default_context()
    with smtplib.SMTP(smtp_server, port) as server:
        server.starttls(context=context)
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, msg.as_string())


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help="Name of the log file to send.")
    args = parser.parse_args()

    send_email(args.filename)
