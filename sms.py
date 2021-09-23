# TODO: Initialize Africa's Talking
import africastalking
africastalking.initialize(
username='farah',
api_key='1abcb49ee5cc13055a41e5838ce48b2f4d685d0853a1f38a27203901aae1a4c6'
)
sms = africastalking.SMS
def sending(phone, password,fname):
    # TODO: Send message
    recipients = [phone]
    message = "Hi {}, Welcome to Erealtors, Your login Info is {}".format(fname, password)
    sender = 'AFRICASTKNG' # Place your SenderID here
    try:
        response = sms.send(message, recipients)
        print(response)
    except Exception as e:
        print(f'Houston, something went wrong: ${e}')
def sending1(phone, password,fname,company_name):
    # TODO: Send message
    recipients = [phone]
    message = "Hi {}, Welcome to Erealtors, Your login Info is {}, YOu are now an Agent of {} ".format(fname, password,company_name)
    sender = 'AFRICASTKNG' # Place your SenderID here
    try:
        response = sms.send(message, recipients)
        print(response)
    except Exception as e:
        print(f'Houston, something went wrong: ${e}')

def sending2(phone, password,fname,company_name):
    # TODO: Send message
    recipients = [phone]
    message = "Hi {}, Welcome to Erealtors, Your login Info is {}, YOu are now an Tenant of {} ".format(fname, password,company_name)
    sender = 'AFRICASTKNG' # Place your SenderID here
    try:
        response = sms.send(message, recipients)
        print(response)
    except Exception as e:
        print(f'Houston, something went wrong: ${e}')

def sending3(phone, password,fname,company_name):
    # TODO: Send message
    recipients = [phone]
    message = "Hi {}, Welcome to Erealtors, Your login Info is {}, YOu are now a Landlord of {} ".format(fname, password,company_name)
    sender = 'AFRICASTKNG' # Place your SenderID here
    try:
        response = sms.send(message, recipients)
        print(response)
    except Exception as e:
        print(f'Houston, something went wrong: ${e}')