import smtplib, ssl, argparse, os


def send_email(filename):
    port = 587  # For starttls
    smtp_server = "smtp.gmail.com"
    sender_email = "loic.hovon@gmail.com"
    receiver_email = "loic.hovon@gmail.com"
    password = os.environ.get("TMXSCRAPE_EMAILPASS")
    message = open(filename, "r", encoding="utf8").read()

    print(message)

    context = ssl.create_default_context()
    with smtplib.SMTP(smtp_server, port) as server:
        server.ehlo()  # Can be omitted
        server.starttls(context=context)
        server.ehlo()  # Can be omitted
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help="Name of the log file to send.")
    args = parser.parse_args()

    send_email(args.filename)
