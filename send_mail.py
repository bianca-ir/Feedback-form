import smtplib 
from email.mime.text import MIMEText 

def send_mail(customer, location, rating, comments): 
    port = 2525 
    smtp_server = 'smtp.mailtrap.io'
    login = 'bb5c1ae0faa184'
    password = 'b7e54ad5b99323' 
    message = f"<h3> New feedback submission </h3><ul><li> Customer:{customer}</li><li> Location:{location}</li><li> Rating:{rating}</li><li> Comments:{comments}</li></ul>"

    sender_email = 'bot@cafehouse.com'
    receiver_email = 'yourmail@example.com'
    msg = MIMEText(message, 'html') 
    msg['Subject'] = 'Cafe House Feedback'
    msg['From'] = sender_email
    msg['To'] = receiver_email

    # Send mail 
    with smtplib.SMTP(smtp_server, port) as server: 
        server.login(login, password) 
        server.sendmail(sender_email, receiver_email, msg.as_string()) 
