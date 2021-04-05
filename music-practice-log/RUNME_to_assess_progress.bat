@echo OFF

rem Define the path to your Anaconda installation activate.bat file.
set CONDAPATH=C:\ProgramData\Anaconda3\Scripts\activate.bat
rem Define here the path to your environment.
set ENVPATH="C:\Users\Samuel Huguet\.conda\envs\Python3.7Environment"
rem Define the path to log_my_progress.py.
set PYFUNCTION="C:\Users\Samuel Huguet\OneDrive\Documents\Personal\Music-Practice-Log\music-practice-log\assess_my_progress.py"

rem Activate the conda environment
call %CONDAPATH% %ENVPATH%

rem Run a python script in that environment
python %PYFUNCTION%

rem Deactivate the environment
call conda deactivate
