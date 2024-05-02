"""
This is a simple program that will take a list of receivers and a message and send the message to all the receivers,
but in chunks, to avoid overloading the server and bypass rate or max recipients limits.

The program will take the following inputs:
- Chunk size: The number of receivers to send the message to at a time.
- Receivers: A list of receivers to send the message to (txt file)
- html message: The message to send to the receivers (html file)
- text message: The message to send to the receivers (txt file)
- Subject: The subject of the email
- Sender: The email address of the sender
- Password: The password of the sender
"""

import getpass
import smtplib as smtp
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def main():
    MAX_RECEIVERS = int(input("Chunk size: "))
    RECEIVERS: list[str] = []

    print("Please ensure the following:")
    print("1. the receivers.txt file is in the same directory as this program. It shall contain the list of receivers, seperated by line-breaks.")
    print("2. the content.html file is in the same directory as this program. It shall contain the html content of the email.")
    print("3. the content.txt file is in the same directory as this program. It shall contain the text content of the email.")
    print("4. the sender email address and password you will enter are correct.")

    print("Press enter to continue...")
    input()

    print("=== reading files ===")

    with open("receivers.txt", "r") as file:
        receivers = file.readlines()
        for receiver in receivers:
            RECEIVERS.append(receiver.strip())
        
    with open("content.html", "r") as file:
        html_message = file.read()

    with open("content.txt", "r") as file:
        text_message = file.read()

    subject = input("Subject: ")
    smtp_server = input("SMTP Server: ")
    smtp_port = input("SMTP Port (default=465): ")
    if smtp_port == "":
        smtp_port = 465
    else:
        smtp_port = int(smtp_port)
    
    smtp_username = input("SMTP Username: ")
    smtp_password = getpass.getpass("SMTP Password: ")

    sender_email = input("Sender: ")

    # create a secure SSL context
    ssl_context = ssl.create_default_context()



    with smtp.SMTP_SSL(smtp_server, smtp_port, context=ssl_context) as server:
        server.login(smtp_username, smtp_password)
        print("=== logged in ===")

        if input(f"Confirm sending email to {len(receiver)} receivers? (y for yes)") != "y":
            print("Exiting...")
            return
        
        print("=== sending emails ===")

        # send email to all receivers in chunks
        # first divide the receivers into chunks
        receiver_chunks: list[list[str]] = [RECEIVERS[i:i+MAX_RECEIVERS] for i in range(0, len(RECEIVERS), MAX_RECEIVERS)]

        for chunk in receiver_chunks:
            message = MIMEMultipart("alternative")
            message["Subject"] = subject
            message["From"] = sender_email
            message["To"] = sender_email # always send to self and use Bcc to send to receivers (data privacy)
            message["Bcc"] = ", ".join(chunk)
            message.attach(MIMEText(html_message, "html"))
            message.attach(MIMEText(text_message, "plain"))

            print(message.as_string())
            


if __name__ == "__main__":
    main()