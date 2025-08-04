from exchangelib import Mailbox, Account, Credentials
def check_email(email_address,email_pass):
    credentials = Credentials(email_address, email_pass)
    account = Account(email_address, credentials=credentials, autodiscover=True)
    latest_email = account.inbox.all().order_by('-datetime_received')[0]
    return latest_email.subject,latest_email.body



