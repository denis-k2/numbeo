import smtplib
from email.message import EmailMessage

# email = os.getenv("email")
# email_password = os.getenv("email_pw")

EMAIL = 'noreply@relohelper.space'
EMAIL_PASSWORD = 'CH#uC655sksC@#T'


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
            <a href="http://localhost:8000/verify/{token}">
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
    msg["From"] = f'Relohelper <{EMAIL}>'
    msg["To"] = to

    # Send the message via our own SMTP server.
    server = smtplib.SMTP_SSL("smtp.zoho.com", 465)
    server.login(EMAIL, EMAIL_PASSWORD)
    server.send_message(msg)
    server.quit()

# http://relohelper.space:8000/verify/eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJkZW4iLCJlbWFpbCI6ImR4eHg5OTlAZ21haWwuY29tIiwicm9sZSI6InVzZXIiLCJhY3RpdmUiOmZhbHNlLCJleHAiOjE2ODk1NzkxMTd9.LEvyf_iYZqVogpPjk6LwifqtxPfOfIzQ07_mg5h6BaY
