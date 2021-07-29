# README for project: Music-Practice-Log

## Author details: 
Name: Sam Huguet  
E-mail: samhuguet1@gmail.com

## Description: 
- The purpose of this collection of these functions and .bat files are to allow the user to quickly log the amount of time they have dedicated to their chosen skill. In my case, it's a 5 string banjo. 
- Once practice time (in minutes) is logged, the script will produce a graph which provides an overview of the cumulative amount of practice over time. 
- Finally, you can get your PC to periodically run functions which can check if you've recently practiced. If you haven't, Python will send you an e-mail with the aforementioned graph attached, and a predicted ETA for the completion of your goal (e.g. 2500 total hours of practice). 
- I've also included code in case you want to recieve a WhatsApp message (via the Twilio service). This service requires a paid subscription, so it might not be for everybody. 

## Requirements. 
(1) An anaconda installation with a preprepared virtual environment containing the packages listed in ```conda_env.txt```. 
(2) A phone which can use WhatsApp or a gmail account. 

## How to log your time spent honing your chosen skill: 

(1) First, we need to set up all the correct paths for you machine. Open your ```.bat``` file named ```RUNME_to_log_progress```. Within this file, edit the following variables: 
- Set ```CONDAPATH``` to your the path of your Anaconda installation. 
- Set ```ENVPATH``` to the path of your virtual anaconda environment. 
- Set ```PYFUNCTION``` to the path of ```log_my_progress.py```. 

(2) Open up (to edit) ```log_my_progress.py```. Here, you'll see the following code at the end: 

```
plot_log_data(log_data,
             your_goal_in_hours = 2500)
```
You need to change the value of the last variable, ```your_goal_in_hours```, to the total number of hours you want to cumulatively achieve when practicing your chosen skill. 

(3) Double click on ```RUNME_to_log_progress.bat``` to log your progress. A small GUI will appear, asking you to enter the number of minutes that you have practiced today (see image below):

<img src="https://github.com/SamHSoftware/Music-Practice-Log/blob/main/img/GUI.PNG?raw=true" alt="GUI to enter practice time" width="300"/> 

Enter the number of minutes with the characters '0-9'. You may also use decimal points, but may not use non-numerical characters. If you do, the script will ask you to re-enter the value correctly. Press ```OK``` to finish.  

(4) A graph similar to the following will appear: 

<img src="https://github.com/SamHSoftware/Music-Practice-Log/blob/main/img/Graph.PNG?raw=true" alt="A graph of the cumulative amount of practice done over time" width="500"/> 

You may notice that the graph is lacking a title, and might seem like it's been cropped. If this is the case, click on the 'Configure subplots' button, then select 'Tight layout'.

## How to automatically assess your progress with time. 

(1) First, we need to set up all the correct paths for you machine. Open your ```.bat``` file named ```RUNME_to_assess_progress```. Within this file, edit the following variables: 
- Set ```CONDAPATH``` to your the path of your Anaconda installation. 
- Set ```ENVPATH``` to the path of your virtual anaconda environment. 
- Set ```PYFUNCTION``` to the path of ```assess_my_progress.py```. 

(2) Open (but don't yet run) ```assess_my_progress.py```. You will see the following lines of code... 
```
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
               from_whatsapp_number = os.environ.get('from_whatsapp_number'),
               to_whatsapp_number = os.environ.get('to_whatsapp_number'))
```

As you can see, there are quite a few input arguments. Most of the variables are described in the code block above, but there are a couple of things to mention.
- Some of the arguaments can be directly and easily edited (such as 'method' and 'time_threshold'), but I'd recommend adding some of the other variables (such as the passwords) to your os environemnt, so that they can be easily accessed via ```os.environ.get()```.
- The ```method``` variable is the most important. As described above, it can be set to either 'email' or 'WhatsApp'. If you choose the 'email' option, you can leave the last four variables (those pertaining to thw WhatsApp twilio service) untouched. ```os.environ.get()``` will return an empty object, and that's fine. Alternatively, if you'd prefer to recieve a WhatsApp message, then the email variables can be left untouched. 
- If you want to use the Twilio service, go to their website and follow their instructions to set up the service on your phone. 
- If you want to recive emails, you need to use gmail, and set up a 16 digit app password. You can find out how to do that [here](https://www.youtube.com/embed/JRCJ6RtE3xUhttps://youtu.be/JRCJ6RtE3xU?t=45).

(3) ??? auto run the bat file. 

(4) When run, the ```RUNME_to_assess_progress``` file will check to see if you have logged any practice time in the last 2 days. If you haven't, then the aforementioned e-mail/WhatsApp message will be sent to you. It's as simple as that! 







