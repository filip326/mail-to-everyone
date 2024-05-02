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

def main():
    MAX_RECEIVERS = int(input("Chunk size: "))
    RECEIVERS: list[str] = []

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
    smtp_port = input("SMTP Port (default=587): ")
    if smtp_port == "":
        smtp_port = 587
    else:
        smtp_port = int(smtp_port)
    
    smtp_username = input("SMTP Username: ")
    smtp_password = getpass.getpass("SMTP Password: ")

    sender = input("Sender: ")
