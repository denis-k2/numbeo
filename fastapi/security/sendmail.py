import smtplib
from email.message import EmailMessage

from config import settings

DOMAIN_NAME = settings.domain_name
DOMAIN_PORT = settings.domain_port
SMTP_HOST = settings.smtp_host
SMTP_PORT = settings.smtp_port
EMAIL = settings.email
EMAIL_PASSWORD = settings.email_password


def send_mail(to, token, username):
    msg = EmailMessage()
    msg.add_alternative(
        f"""\
<html>
  <head>

    <title>Document</title>
  </head>
  <body>
    <div id="box">
      <h2>Hello {username},</h2> 
        <p> Before you can use the API, click 
            <a href="http://{DOMAIN_NAME}:{DOMAIN_PORT}/verify/{token}">
                here
            </a> to confirm your registration.
        </p>
      </form>
    </div>
  </body>
</html>

<style>
  #box {{
    margin: 0 auto;
    max-width: 500px;
    border: 1px solid black;
    height: 200px;
    text-align: center;
    background: lightgray;
  }}

  p {{
    padding: 10px 10px;
    font-size: 18px;
  }}

  .inline {{
    display: inline;
  }}

  .link-button {{
    background: none;
    border: none;
    color: blue;
    font-size: 22px;
    text-decoration: underline;
    cursor: pointer;
    font-family: serif;
  }}
  .link-button:focus {{
    outline: none;
  }}
  .link-button:active {{
    color: red;
  }}
</style>
    """,
        subtype="html",
    )

    msg["Subject"] = "Confirmation of your registration"
    msg["From"] = f"Relohelper <{EMAIL}>"
    msg["To"] = to

    # Send the message via our own SMTP server.
    server = smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT)
    server.login(EMAIL, EMAIL_PASSWORD)
    server.send_message(msg)
    server.quit()
