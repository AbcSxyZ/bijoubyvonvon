from django.conf import settings
from django.core.mail import send_mail
import re
import os

def description_loader():
    """
    Retrieve the description file, and format it
    with html tags to get an appropriate paragraph format.
    """
    #Retrieve file content
    src_file  = os.path.join(settings.BASE_DIR, settings.DESCRIPTION_FILE)
    description_text = open(src_file, 'r', encoding="utf8").read()

    #Strip empty lines
    text = re.sub("^\s*$", "", description_text, flags=re.MULTILINE)

    #Split by paragraph
    paragraph_list = re.split("\n{2,}", text)
    description_render = ""
    for paragraph in paragraph_list:
        description_render += """
        <p class="content has-text-justified is-size-5">
            {}
        </p>
        """.format(paragraph)
    return description_render

def mailing(post_data):
    """
    Send an email to the website owner with data inside
    the contact form.
    """
    mail_subject = "Website - Nouveau message"
    mail_body = """
    De : {email}
    Sujet : {subject}

    {msg}
    """.format(**post_data.dict())
    email_from = settings.EMAIL_HOST_USER
    email_to = ["bijoubyvonvon@gmail.com"]
    send_mail(mail_subject, mail_body, email_from, email_to)
