from MPL_functions import *

## FUNCTION PURPOSE: A function to WhatsApp or email the user to remind them to practice their instrument. 
# Function input arg 1: method [string] --> 'email' or 'WhatsApp'. Determins the type of message you recieve. 
# Function input arg 2: time_threshold [int] --> The number of days (discrete value) without practice, after which the user will be sent an e-mail. 
# Function input arg 3: email_address [string] --> The gmail address you wish to use. 
# Function input arg 3: email_password [string] --> The 16-digit google app password which you can create online. 
# Function input arg 4: account_sid [string] --> The application SID if using the Twilio service. 
# Function input arg 5: authorisation_token [string] --> The authorisation token if using the Twilio service. 
# Function input arg 6: from_whatsapp_number [string] --> The WhatsApp number you wish to send messages from. 
# Function input arg 7: to_whatsapp_number [string] --> The WhatsApp number you wish to send messages to. 
# Function output 1: Log data is added to GitHub, and a message is sent to the user. 
message_me(method='email', 
               time_threshold = 2, 
               email_address = os.environ.get('gmail_address'),
               email_password = os.environ.get('MPL_gmail_password'), 
               account_sid = os.environ.get('account_sid'),
               authorisation_token  = os.environ.get('authorisation_token'), 
               from_whatsapp_number = os.environ.get('from_whatsapp_number')
               to_whatsapp_number = os.environ.get('to_whatsapp_number'))