This is just a draft tool. 

make sure create .venv folder and activate the virtual environment. 

I didn't prepare requirement.txt, so just install missing packages according to the error message.

Just to run main_window.py and you will get 3 windows on the desktop: playback control, video, radar visualization. 

To change dataset files, sensor sync time, sensor position, edit config.json. 

if you want to have differnt config.json files for different dataset, search : with open('config.json', 'r') as file. then replace config.json to the exact file name.  There are two lines of code you need to change, we shall update the code to only change once. 

In the control window, just start and stop buttons are correctly implemented right now. Sadly the other functions worked before, just after some changes they didn't work anymore but should be easy fixes. 

TO DO:

to easily visualize specifc frame, we need to fix the slider bar function. the slider method is there, just not showing up in the window. Then we can fix the step forward and backward fucntion if needed.
