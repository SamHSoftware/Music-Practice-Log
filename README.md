# README for project: Music-Practice-Log

## Author details: 
Name: Sam Huguet  
E-mail: samhuguet1@gmail.com

## Description: 
- The purpose of this collection of these functions and .bat files are to allow the user to quickly log the amount of time they have practiced their chosen skill. In my case, it's a 5 string banjo. 
- Once practice time (in minutes) is logged, the script will produce a graph which provides an overview of the cumulative amount of practice over time. 
- Finally, periodically run functions can check if you've recently practiced. If you haven't, Python will send you a WhatsApp message (via the Twilio service) with the aforementioned graph attached, and a predicted ETA for the completion of your goal (e.g. 2500 total hours of practice). 

## Software requirements. 
(1) An anaconda installation with a preprepared virtual environment containing the packages listed in ```conda_env.txt```. 

## How to log your time spent honing your chosen skill: 

(1) First, we need to set up all the correct paths for you machine. Open your ```.bat``` file named ```RUNME_to_log_progress```. Within this file, modify the following variables: 
- Set ```CONDAPATH``` to your the path of your Anaconda installation. 
- Set ```ENVPATH``` to the path of your virtual anaconda environment. 
- Set ```PYFUNCTION``` to the 

(2) Double click on ```RUNME_to_log_progress```. A small GUI will appear, asking you to enter the number of minutes that you have practiced today (see image below):

get the image ...........................

Enter the number of minutes with the characters '0-9'. You may also use decimal points, but may not use non-numerical characters. If you do, the script will ask you to re-enter the value correctly. Press ```OK``` to finish.  











