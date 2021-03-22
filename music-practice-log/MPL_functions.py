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

    #### (2) Use the GUI.
    instance_GUI = GUI("Please enter the number of minutes practiced.")
    minutes_practiced_today = instance_GUI.response
    
    # If there was an accidental text entry, notify the user, and ask for a numerical input. 
    while bool(re.search('[^0-9^.]', minutes_practiced_today)) is True or minutes_practiced_today.count('.') > 1: 
        instance_GUI = GUI("Re-enter answer using only numbers 0-9 and one decimal point.")
        minutes_practiced_today = instance_GUI.response
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

## FUNCTION PURPOSE: A function to update the local graph, and push it to GitHub. 
# Function input arg 1: log_data [pandas.DataFrame] --> Contains the log data.
# Function output 1: Saves a copy of the graph to the log-data folder as 'log.png'.

# Create the graph. 
def plot_log_data(log_data):
    
    #### (1) Prepare the data for plotting.
    # Convert the date column to a datetime object. 
    log_data['Date (datetime object)'] = log_data['Date (DMY)'].astype('datetime64[ns]')
    
    # Get the start and end dates. 
    t_start = log_data['Date (datetime object)'][0]
    t_end = log_data['Date (datetime object)'][len(log_data)-1] 
    
    # Add a column the the number of days seperating each data-point from the first log-entry. 
    log_data['Days from start'] = [(abs(log_data['Date (datetime object)'][0] - row)).days for row in log_data['Date (datetime object)']]

    ### (2) Perform linear regression.
    regr = linear_model.LinearRegression(fit_intercept=False)
    days_from_start = log_data['Days from start'].to_numpy().reshape(-1, 1)
    cumulative_practice = log_data['Cumulative practice time (hours)'].to_numpy().reshape(-1, 1)
    regr.fit(days_from_start, cumulative_practice)
    
    x_prediction_values = log_data['Days from start'].iloc[[0, -1]].to_numpy().reshape(-1, 1)
    predictions = regr.predict(x_prediction_values)
    
    # Predict how long it'll take to get to our cumulative practice target. 
    days_till_completion = 2500/float(regr.coef_[0])
    years_till_completion = days_till_completion/365
    
    # Collect the results of the linear regression model so that we can plot them. 
    regr_date = pd.DataFrame()
    regr_date['First and last dates'] = log_data['Date (datetime object)'].iloc[[0,-1]]
    regr_date['Practice time (hours)'] = predictions
    
    #### (3) Prepare path names so that we can save the graph.
    cwd = os.getcwd()  
    log_data_directory = cwd.replace('music-practice-log', 'log-data')
    file_directory = os.path.join(log_data_directory, 'log.png')
    
    #### (4) Plot the graph.
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    date_data = log_data['Date (datetime object)']
    practice_data = log_data['Cumulative practice time (hours)']
    plt.plot_date(date_data, practice_data, linestyle='solid')
    plt.plot_date(regr_date['First and last dates'],regr_date['Practice time (hours)'],'r--')
    plt.gcf().autofmt_xdate()
    date_format = mpl_dates.DateFormatter('%d-%m-%Y')
    plt.gca().xaxis.set_major_formatter(date_format)
    plt.tight_layout()
    plt.xlabel('Date', labelpad=15)
    plt.ylabel('Cumulative practice \ntime (hours)', labelpad=10)
    plt.rcParams.update({'font.size': 15})
    ax.set_ylim([0, math.ceil(max(log_data['Cumulative practice time (hours)']))])
    #ax.set_xlim([datetime.date(t_start.year, t_start.month, t_start.day), datetime.date(t_end.year, t_end.month, t_end.day)])
    ax.xaxis.set_major_locator(plt.LinearLocator(4))
    years_string = '%.1f' % years_till_completion
    plt.title('Hi Sam.\n Given your current progress, you are\n predicted to reach your goal in ' + years_string + ' years.\n Keep up the good work!\n')
    #plt.savefig(file_directory, dpi=200, bbox_inches = "tight")
    plt.show()
    