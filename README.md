# README for project: Music-Practice-Log

## Author details: 
Name: Sam Huguet  
E-mail: samhuguet1@gmail.com

## Description: 
- The purpose of this collection of these functions and .bat files are to allow the user to quickly log the amount of time they have practiced their chosen skill. In my case, it's a 5 string banjo. 
- Once practice time (in minutes) is logged, the script will produce a graph which provides an overview of the cumulative amount of practice over time. 
- Finally, periodically run functions can check if you've recently practiced. If you haven't, Python will send you a an e-mail with the aforementioned graph attached, and a predicted ETA for the completion of your goal (e.g. 2500 total hours of practice). 
- I've also included code in case you want to recieve a WhatsApp message (via the Twilio service). This service requires a paid subscription, so it might not be for everybody. 

## Software requirements. 
(1) An anaconda installation with a preprepared virtual environment containing the packages listed in ```conda_env.txt```. 

## How to log your time spent honing your chosen skill: 

(1) First, we need to set up all the correct paths for you machine. Open your ```.bat``` file named ```RUNME_to_log_progress```. Within this file, modify the following variables: 
- Set ```CONDAPATH``` to your the path of your Anaconda installation. 
- Set ```ENVPATH``` to the path of your virtual anaconda environment. 
- Set ```PYFUNCTION``` to the 

(2) Double click on ```RUNME_to_log_progress```. A small GUI will appear, asking you to enter the number of minutes that you have practiced today (see image below):

<img src="https://github.com/SamHSoftware/Music-Practice-Log/blob/main/img/GUI.PNG?raw=true" alt="GUI to enter practice time" width="300"/> 

Enter the number of minutes with the characters '0-9'. You may also use decimal points, but may not use non-numerical characters. If you do, the script will ask you to re-enter the value correctly. Press ```OK``` to finish.  

(3) A graph similar to the following will appear: 

<img src="https://github.com/SamHSoftware/Music-Practice-Log/blob/main/img/Graph.PNG?raw=true" alt="A graph of the cumulative amount of practice done over time" width="500"/> 

You may notice that the graph is lacking a title, and might seem like it's been cropped. If this is the case, click on the 'Configure subplots' button, then select 'Tight layout'.

## How to automatically assess your progress with time. 

(1) ??? auto run the bat file. 

(2) When run, the ```RUNME_to_assess_progress``` file will check to see if you have logged any practice time in the last 2 days. If you haven't, then the aforementioned e-mail will be sent to you. It's as simple as that! 







