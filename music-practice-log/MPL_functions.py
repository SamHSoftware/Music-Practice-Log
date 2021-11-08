from tkinter import *
import os.path 
from datetime import date
import pandas as pd
import numpy as np
import re 
import matplotlib.pyplot as plt
from matplotlib import dates as mpl_dates
import math 
import datetime 
from sklearn import datasets, linear_model
import numpy as np
import os 
from twilio.rest import Client
from git import Repo
from datetime import date, datetime
import smtplib
import random
from email.message import EmailMessage
import imghdr
import seaborn as sns 
from PIL import Image 

## FUNCTION PURPOSE: Allows the user to record the quantity of music practice that has been achieved for the day (in minutes). 
# Function inputs arg 1: None. 
# Function output 1: Creates/updates the log containing practice information.
# Function output 2: df [pandas.DataFrame] --> The updated log as a pandas DataFrame. 

# Create a GUI to log the duration of today's music practice.  
def log_progress():
    
    #### (1) Make the GUI.
    
    # Make a class object for the GUI.
    class GUI(): 
        def __init__(self, prompt):
            self.prompt = prompt 
            self.response = ""

            def OK():
                self.response = entry.get()
                root.destroy()

            root = Tk()
            lbl = Label(root, text=self.prompt)
            lbl.pack()
            entry = Entry(root)
            entry.pack()

            b = Button(root, text="OK", width=10, command=OK)
            b.pack()
            root.mainloop()

    #### (2) Create and call a function to use the GUI, and catch any user errors. 
    def use_GUI(message = "Please enter the number of minutes practiced."):
        instance_GUI = GUI(message)
        minutes_practiced_today = instance_GUI.response
        
        # Looks for accidental text entries, or emtpy entries.
        letters_in_answer = bool(re.search('[^0-9^.]', minutes_practiced_today))
        no_answer_given = True if len(minutes_practiced_today) == 0 else False
        
        # If the answer is OK. 
        if letters_in_answer == False and no_answer_given == False:
            print('case 1')
            return instance_GUI.response
        # If the answer contains alphabetical letters. 
        elif letters_in_answer == True and no_answer_given == False:
            print('case 2')
            return use_GUI("Re-enter answer using only numbers 0-9 and one decimal point.")
        # If the answer contains to no characters. 
        elif letters_in_answer == False and no_answer_given == True:
            print('case 3')
            return use_GUI("Oops, you forgot to enter a number!\nPlease re-enter your value, then press 'OK'")
    
    minutes_practiced_today = use_GUI(message = "Please enter the number of minutes practiced.")
    hours_practiced_today = float(minutes_practiced_today)/60
    
    #### (4) Determine the full file path for our log data.  
    cwd = os.getcwd()  
    log_data_directory = cwd.replace('music-practice-log', 'log-data')
    log_data_path = os.path.join(log_data_directory, 'log.csv')
    
    #### (5) Consider the user input, and add it to our log file. 
    # Create a list to hold the data. 
    df = []
        
    # Create the log file if it does not already exist. 
    if os.path.isfile(log_data_path) is False: 
        
        # Record the new data within a list.
        today = date.today()
        the_date = today.strftime("%d/%m/%Y")
        d = [
            the_date,
            hours_practiced_today,
            hours_practiced_today]
        
        # Append all the information to our dataframe. 
        df.append(d)
        
        # Convert the array to a pandas dataframe. 
        df = pd.DataFrame(df, columns=['Date (DMY)','Practice time (hours)','Cumulative practice time (hours)'])
    
    elif os.path.isfile(log_data_path) is True: 
    
        # Load in the data. 
        previous_data = pd.read_csv(log_data_path)
            
        # Calculate the cumulative number of hours played. 
        previous_hours = previous_data.iloc[:,1]
        total_hours = sum(previous_hours) + float(hours_practiced_today)
        
        # Record the new data within a list. 
        today = date.today()
        the_date = today.strftime("%d/%m/%Y")
        d = [the_date,
             hours_practiced_today,
             total_hours]
        
        # Add the information to our dataframe. 
        previous_data.loc[len(previous_data)] = d
        df = previous_data
        
    # Save our data.
    df.to_csv(log_data_path, index=False)
    
    return df

## FUNCTION PURPOSE: A function to update the local graph.
# Function input arg 1: log_data [pandas.DataFrame] --> Contains the log data.
# Function input arg 2: your_goal_in_hours [int] --> Your cumulative practice goal, in hours. 
# Function output 1: Saves a copy of the graph to the log-data folder as 'log.png'.

# Create the graph. 
def plot_log_data(log_data, 
                  your_goal_in_hours = 2500):
    
    #### (1) Prepare the data for plotting.
    # Convert the date column to a datetime object. 
    log_data['Date (datetime object)'] = pd.to_datetime(log_data['Date (DMY)'], format='%d/%m/%Y')
    
    # Get the start and end dates. 
    t_start = log_data['Date (datetime object)'][0]
    t_end = log_data['Date (datetime object)'][len(log_data)-1] 
    
    # Add a column with the number of days seperating each data-point from the first log-entry. 
    log_data['Days from start'] = [(abs(log_data['Date (datetime object)'][0] - row)).days for row in log_data['Date (datetime object)']]

    ### (2) Perform linear regression.
    regr = linear_model.LinearRegression(fit_intercept=False)
    days_from_start = log_data['Days from start'].to_numpy().reshape(-1, 1)
    cumulative_practice = log_data['Cumulative practice time (hours)'].to_numpy().reshape(-1, 1)
    regr.fit(days_from_start, cumulative_practice)
    
    x_prediction_values = log_data['Days from start'].iloc[[0, -1]].to_numpy().reshape(-1, 1)
    predictions = regr.predict(x_prediction_values)
    
    # Predict how long it'll take to get to our cumulative practice target. 
    days_till_completion = (your_goal_in_hours/float(regr.coef_[0]))-days_from_start[-1][0]
    years_till_completion = days_till_completion/365
    
    # Collect the results of the linear regression model so that we can plot them. 
    regr_date = pd.DataFrame()
    regr_date['First and last dates'] = log_data['Date (datetime object)'].iloc[[0,-1]]
    regr_date['Practice time (hours)'] = predictions
    
    #### (3) Prepare path names so that we can save the graph.
    cwd = os.getcwd()  
    log_data_directory = cwd.replace('music-practice-log', 'log-data')
    file_directory = os.path.join(log_data_directory, 'log.png')
    
    #### (4a) Plot the panel of graphs... if you've practiced for a month (31 days) or less.
    if log_data['Days from start'][len(log_data)-1] <= 31:
        
        # Plot the practice over time graph.
        ax = plt.subplot2grid((1, 5), (0, 0), colspan=3)
        date_data = log_data['Date (datetime object)']
        practice_data = log_data['Cumulative practice time (hours)']
        plt.plot_date(date_data, practice_data, linestyle='solid', markersize=2, linewidth=1)
        plt.plot_date(regr_date['First and last dates'],regr_date['Practice time (hours)'],'r--')
        plt.setp(plt.xticks()[1], rotation=30, ha='right')
        plt.xlabel('Date', labelpad=15)
        plt.ylabel('Cumulative practice \ntime (hours)', labelpad=10)
        plt.rcParams.update({'font.size': 12})
        ax.set_ylim([0, math.ceil(max(log_data['Cumulative practice time (hours)']))])
        #ax.set_xlim([datetime.date(t_start.year, t_start.month, t_start.day), datetime.date(t_end.year, t_end.month, t_end.day)])
        ax.xaxis.set_major_locator(plt.LinearLocator(4))
        years_string = '%.1f' % years_till_completion
        plt.title(f"Hi Sam.\nYour goal is {str(your_goal_in_hours)} hours of practice.\nYou've practiced for {round(cumulative_practice[-1][0], 1)} hours.\nYou're predicted to reach your goal\nin {years_string} years.\nKeep up the good work!\n", loc='left')

        # Create a KDE plot to represent the distribution of practice durations.
        plt.subplot2grid((1, 5), (0, 3), colspan=2)
        plt.rcParams.update({'font.size': 12})
        plt.xlabel('Practice time (hours)', labelpad=15)
        plt.ylabel('Density', labelpad=10)
        g = sns.kdeplot(log_data['Practice time (hours)'], bw_adjust=0.2, color="blue", shade=True)
        plt.title("Kernel density estimate (KDE)\nplot of practice durations\n")
        plt.axvline(log_data['Practice time (hours)'].mean(), color='k', linestyle='dashed', linewidth=1)
        mean_time = log_data['Practice time (hours)'].mean()*60
        plt.text(log_data['Practice time (hours)'].mean()*1.1, 0.8, f'Mean: {mean_time:.1f} min')

        # Show and save the figure. 
        plt.tight_layout()    
        figure = plt.gcf()
        figure.set_size_inches(10,10)
        plt.savefig(file_directory, dpi=200, bbox_inches = "tight")
        img = Image.open(file_directory)
        img.show()
        
    #### (4b) Plot the panel of graphs... if you've practiced for more than a month (31 days).
    if log_data['Days from start'][len(log_data)-1] > 31:

        # Get the row index representing the threshold after which we should include data. 
        minimum = min(i for i in (days_from_start - 31) if i >= 0)[0]
        idx = np.where((days_from_start - 31) == minimum)[0][0]
         
        # NOTE: The following variables are similar to those which were previously created.
        # To differentiate some of them, I will add '_31'.

        # Perform linear regression for the last month.
        log_data_31 = log_data[idx:len(log_data)]
        regr_31 = linear_model.LinearRegression(fit_intercept=True)
        days_within_last_month = log_data_31['Days from start'].to_numpy().reshape(-1, 1)
        cumulative_practice_last_month = log_data_31['Cumulative practice time (hours)'].to_numpy().reshape(-1, 1)
        regr_31.fit(days_within_last_month, cumulative_practice_last_month)
        x_prediction_values_last_month = log_data_31['Days from start'].iloc[[0, -1]].to_numpy().reshape(-1, 1)
        predictions_last_month = regr_31.predict(x_prediction_values_last_month)

        # Predict how long it'll take to get to our cumulative practice target given the last month of data.
        days_till_completion_31 = (your_goal_in_hours/float(regr_31.coef_[0]))-days_from_start[-1][0]        
        years_till_completion_31 = days_till_completion_31/365

        # Collect the results of the linear regression model so that we can plot them. 
        regr_31_date_1 = pd.DataFrame()
        regr_31_date_1['First and last dates'] = log_data['Date (datetime object)'].iloc[[0,-1]]
        regr_31_date_1['Practice time (hours)'] = regr_31.predict(log_data['Days from start'].iloc[[0,-1]].to_numpy().reshape(-1, 1))
        
        regr_31_date_2 = pd.DataFrame()
        regr_31_date_2['First and last dates'] = log_data_31['Date (datetime object)'].iloc[[0,-1]]
        regr_31_date_2['Practice time (hours)'] = predictions_last_month
   
        # Plot the practice over time graph FOR ENTIRE DATA RANGE.
        ax = plt.subplot2grid((2, 5), (0, 0), colspan=3)
        date_data = log_data['Date (datetime object)']
        practice_data = log_data['Cumulative practice time (hours)']
        plt.plot_date(regr_date['First and last dates'],regr_date['Practice time (hours)'],'r--', linewidth=0.8, label ='LOBF: All data')
        plt.plot_date(regr_31_date_1['First and last dates'],regr_31_date_1['Practice time (hours)'],'b--', linewidth=0.8, label ="LOBF: Last month's data")
        plt.plot_date(date_data, practice_data, linestyle='solid', markersize=2, linewidth=1, label ='Cumulative practice')
        plt.legend(loc="upper left")
        plt.setp(plt.xticks()[1], rotation=30, ha='right')
        plt.xlabel('Date', labelpad=15)
        plt.ylabel('Cumulative practice \ntime (hours)', labelpad=10)
        plt.rcParams.update({'font.size': 12})
        ax.set_ylim([0, math.ceil(max(log_data['Cumulative practice time (hours)']))])
        #ax.set_xlim([datetime.date(t_start.year, t_start.month, t_start.day), datetime.date(t_end.year, t_end.month, t_end.day)])
        ax.xaxis.set_major_locator(plt.LinearLocator(4))
        years_string = '%.1f' % years_till_completion
        plt.title(f"Hi Sam.\nYour goal is {str(your_goal_in_hours)} hours of practice.\nYou've practiced for {round(cumulative_practice[-1][0], 1)} hours.\nYou're predicted to reach your goal\nin {years_string} years.\nKeep up the good work!\n", loc='left')
        
        # Create a KDE plot to represent the distribution of practice durations FOR ENTIRE DATA RANGE.
        plt.subplot2grid((2, 5), (0, 3), colspan=2)
        plt.rcParams.update({'font.size': 12})
        plt.xlabel('Practice time (hours)', labelpad=15)
        plt.ylabel('Density', labelpad=10)
        g = sns.kdeplot(log_data['Practice time (hours)'], bw_adjust=0.2, color="blue", shade=True)
        plt.title("Kernel density estimate (KDE)\nplot of practice durations\n")
        plt.axvline(log_data['Practice time (hours)'].mean(), color='k', linestyle='dashed', linewidth=1)
        mean_time = log_data['Practice time (hours)'].mean()*60
        plt.text(log_data['Practice time (hours)'].mean()*1.1, 0.8, f'Mean: {mean_time:.1f} min')
        
        # Plot the practice over time graph FOR LAST MONTH OF DATA.
        ax = plt.subplot2grid((2, 5), (1, 0), colspan=3)
        date_data_31 = log_data_31['Date (datetime object)']
        practice_data_31 = log_data_31['Cumulative practice time (hours)']
        plt.plot_date(regr_31_date_2['First and last dates'],regr_31_date_2['Practice time (hours)'],'b--', linewidth=0.8, label="LOBF: Last month's data")
        plt.plot_date(date_data_31, practice_data_31, linestyle='solid', markersize=2, linewidth=1, label='Last month of cumulative\npractice')
        plt.legend(loc="upper left")
        plt.setp(plt.xticks()[1], rotation=30, ha='right')
        plt.xlabel('Date', labelpad=15)
        plt.ylabel('Cumulative practice \ntime (hours)', labelpad=10)
        plt.rcParams.update({'font.size': 12})
        ax.set_ylim([math.floor(min(log_data_31['Cumulative practice time (hours)'])), math.ceil(max(log_data_31['Cumulative practice time (hours)']))])
        #ax.set_xlim([datetime.date(t_start.year, t_start.month, t_start.day), datetime.date(t_end.year, t_end.month, t_end.day)])
        ax.xaxis.set_major_locator(plt.LinearLocator(4))
        years_string = '%.1f' % years_till_completion_31
        plt.title(f"This graph shows your efforts\nover the last month. If you\nmaintain these efforts, you're\npredicted to reach your goal\nin {years_string} years.\n", loc='left')
        
        # Create a KDE plot to represent the distribution of practice durations FOR LAST MONTH OF DATA.
        plt.subplot2grid((2, 5), (1, 3), colspan=2)
        plt.rcParams.update({'font.size': 12})
        plt.xlabel('Practice time (hours)', labelpad=15)
        plt.ylabel('Density', labelpad=10)
        g = sns.kdeplot(log_data_31['Practice time (hours)'], bw_adjust=0.3, color="blue", shade=True)
        plt.title("KDE plot of practice\ndurations over the\nlast month\n")
        plt.axvline(log_data_31['Practice time (hours)'].mean(), color='k', linestyle='dashed', linewidth=1)
        mean_time = log_data_31['Practice time (hours)'].mean()*60
        plt.text(log_data_31['Practice time (hours)'].mean()*1.1, 0.8, f'Mean: {mean_time:.1f} min')

        # Show and save the figure. 
        #plt.tight_layout() 
        plt.subplots_adjust(hspace=1.2, wspace=1.0)
        figure = plt.gcf()
        figure.set_size_inches(10, 10) # width, height
        plt.savefig(file_directory, dpi=200, bbox_inches = "tight")
        img = Image.open(file_directory)
        img.show()
    
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

def message_me(method='email', 
               time_threshold = 1, 
               email_address = os.environ.get('gmail_address'),
               email_password = os.environ.get('MPL_gmail_password'), 
               account_sid = os.environ.get('account_sid'),
               authorisation_token  = os.environ.get('authorisation_token'), 
               from_whatsapp_number = os.environ.get('from_whatsapp_number'),
               to_whatsapp_number = os.environ.get('to_whatsapp_number')):
    
    #### (1) Determine whether the user has practiced their instrument recently. 
    # Determine the full file path for our log data.  
    cwd = os.getcwd()  
    log_data_directory = cwd.replace('music-practice-log', 'log-data')
    log_data_path = os.path.join(log_data_directory, 'log.csv')

    # Determine how long it's been since our last log entry. 
    previous_data = pd.read_csv(log_data_path) 
    previous_data['Date (datetime object)'] = pd.to_datetime(previous_data['Date (DMY)'], format='%d/%m/%Y')
    last_entry = previous_data['Date (datetime object)'][len(previous_data)-1].to_pydatetime().date()
    today = date.today()
    total_days_since_last_entry = (today.day + (today.month*30) + (today.year*365)) - (last_entry.day + (last_entry.month*30) + (last_entry.year*365))

    #### (2) Create a list of potential WhatsApp messages.
    messages = [
        "Ahoy there, Sam. You haven't been able to get some banjo in recently! Have a look at this video to get psyched: https://www.youtube.com/watch?v=-3Y7F5JJRcM",
        "Oh,\n What's occurin,\n Play the Banjo ya noooob.",
        "Mi amigo, this is a reminder to keep up the banjo playing and the banjo logging. The graph must grow!",
        "You should practice because Laura says: 'I think it's really hot when you play the banjo well'. Take from that what you will.",
        "Imagine how awesome it'll be when you can play along at folk nights on the banjo! Keep up the good work.",
        "Hello there, banjo enthusiast! Here's a good song to get you excited for frailing again: https://www.youtube.com/watch?v=X9Rfm3_kJhM",
        "From Laura: 'You can doeth the do Bebe! Grab that Banjo and get strumming.'",
        "Here's the song that started it all: https://www.youtube.com/watch?v=xzt8WxXtVmM",
        "If it's late, or you're tired, remember that clawhammer can be relaxing. Have a listen to this: https://www.youtube.com/watch?v=POZDdac7wHU&list=PLyiQRVof2bGsj2kt_irm6wMgQxoq7jmOK",
        "You are not machines! You are not cattle! You are men! You have the love of humanity in your hearts! You don’t hate! Only the unloved hate - the unloved and the unnatural! Soldiers! Don’t fight for slavery! Fight for liberty! And play the banjo!",
        "Keep calm and play the banjo.",
        "When was the last time you played the banjo?\nJust for the sake of it\nAnd have you ever played the banjo just because it was a banjo and you have two good hands?\nSome people will say\n'You need sheet music'\nBut there is nothing wrong with not knowing what you are playing\nLots of people going around these day\nNot playing their instruments\nGo on any train, bus, plane\nAnd you'll see people who have stopped playing their instruments\nDon't be one of them\nYou may say\n'I've practiced this piece before' and that's ok\nBut creativity is never gone\nPractice they say is without fun\nBut I have never seen your banjo playing itself \nOn any secret corner\nYou may find the tune of your life, the sound of your soul\nThe rhythm of your day, the chord of your smile\nOr maybe not\nBut you may find something you've not heard before\nOf course, not all these practices can be magic practices that stun and amaze\nBut possible you may find a lonely piece that sings and cures\nOr even better you might find peace\nThat world that's on your computer is not the world\nThe world is the one that lies in the sounds your strings make\nAnd the smiles that they create\nThe dances, the vibes, the joys they emulate\nTell the world you are playing and it replies\nYou see I'm not sure what the secret to happiness is\nBut I'm pretty sure it starts when you play your banjo"
    ]
    random_message_idx = random.randint(0,len(messages))
    
    #### (3) Send one of the messages to the user. 
    if total_days_since_last_entry > time_threshold:

        #### (3a) Send a WhatsApp message.
        if method == 'WhatsApp':
            
            # Push the graph to GitHub. 
            PATH_OF_GIT_REPO = r'C:\Users\Samuel Huguet\OneDrive\Documents\Personal\Music-Practice-Log'  # make sure .git folder is properly configured
            COMMIT_MESSAGE = 'Updated graph and log file'
            try:
                repo = Repo(PATH_OF_GIT_REPO)
                repo.git.add(update=True)
                repo.index.commit(COMMIT_MESSAGE)
                origin = repo.remote(name='origin')
                origin.push()
            except:
                print('Some error occured while pushing the code')    
        
            client = Client(account_sid, authorisation_token)

            from_whatsapp_number = 'whatsapp:'+from_whatsapp_number
            to_whatsapp_number = 'whatsapp:'+to_whatsapp_number

            client.messages.create(body = messages[random_message_idx],
                                  MediaUrl = 'https://github.com/SamHSoftware/Music-Practice-Log/blob/main/log-data/log.png?raw=true',
                                  from_= from_whatsapp_number,
                                  to = to_whatsapp_number)
            
        #### (3b) Send an email.
        elif method == 'email':
        
            # Write the e-mail. 
            message = EmailMessage()
            message['Subject'] = 'Practice update'
            message['From'] = email_address
            message['To'] = email_address
            main_content = f'{messages[random_message_idx]}\n\nHere is a the graph displaying your practice over time:'
            message.set_content(main_content)

            # Include the graph within the e-mail.
            cwd = os.getcwd()  
            log_data_directory = cwd.replace('music-practice-log', 'log-data')
            file_directory = os.path.join(log_data_directory, 'log.png')
            
            with open(file_directory, 'rb') as f: 
                file_data = f.read() 
                file_type = imghdr.what(f.name)
                file_name = f.name 
            message.add_attachment(file_data, maintype='image', subtype=file_type, filename=file_name)
            
            # Define an SMTP client session object that can be used to send an email.
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                smtp.login(email_address, email_password)
                smtp.send_message(message)