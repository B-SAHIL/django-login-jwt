from django.core.mail import EmailMessage

def send_email(subject, html_message, from_email, recipient_list):
    email = EmailMessage(subject, html_message, from_email, recipient_list)
    email.content_subtype = "html"  # Set the content type to HTML
    email.send()
    print("Email sent successfully.")
