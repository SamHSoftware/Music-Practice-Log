@echo OFF

rem Define the path to your Anaconda installation.
set CONDAPATH=C:\ProgramData\Anaconda3
rem Define here the path to your environment.
set ENVPATH="C:\Users\Samuel Huguet\.conda\envs\Python3.7Environment"

rem Activate the conda environment
call C:\ProgramData\Anaconda3\Scripts\activate.bat

rem Run a python script in that environment
python "C:\Users\Samuel Huguet\OneDrive\Documents\Personal\Music-Practice-Log\music-practice-log\log_my_progress.py"

rem Deactivate the environment
call conda deactivate
