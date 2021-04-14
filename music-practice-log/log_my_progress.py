from MPL_functions import *

## FUNCTION PURPOSE: Allows the user to record the quantity of music practice that has been achieved for the day (in minutes). 
# Function inputs arg 1: None. 
# Function output 1: Creates/updates the log containing practice information.
# Function output 2: df [pandas.DataFrame] --> The updated log as a pandas DataFrame. 
log_data = log_progress()

## FUNCTION PURPOSE: A function to update the local graph, and push it to GitHub. 
# Function input arg 1: log_data [pandas.DataFrame] --> Contains the log data.
# Function output 1: Saves a copy of the graph to the log-data folder as 'log.png'.
plot_log_data(log_data,
              your_goal_in_hours = 2500)