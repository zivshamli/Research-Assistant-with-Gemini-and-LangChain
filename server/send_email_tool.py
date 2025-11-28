import os
import smtplib
from dotenv import load_dotenv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from langchain.tools import Tool, StructuredTool
from pydantic import BaseModel, Field
from tools import save_to_txt

load_dotenv() 
tomail = os.getenv("EMAIL_ADDRESS2")



def send_email_tool(file_path="research_output.txt",topic="", to_email=tomail):
    from_email = os.getenv("EMAIL_ADDRESS")
    password = os.getenv("EMAIL_PASSWORD")

    if not from_email or not password:
        return " Email credentials are missing. Check your .env file."

    subject = topic
    body = "Attached is the research output you requested."

 

    # יצירת ההודעה
    msg = MIMEMultipart()
    msg["From"] = from_email
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    try:
        with open(file_path, "rb") as attachment:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header("Content-Disposition", f"attachment; filename={file_path}")
        msg.attach(part)
    except FileNotFoundError:
        return f" File {file_path} not found."

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(from_email, password)
            server.sendmail(from_email, to_email, msg.as_string())
        return f" Email sent to {to_email} with file {file_path}"
    except Exception as e:
        return f" Failed to send email: {e}"

send_email_tools = StructuredTool.from_function(
    name="send_email",
    description="Send a text file via email. Provide filename and content.",
    func=send_email_tool
)
