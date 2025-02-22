This program has only been compiled and tested on MacOS X for both Intel and M1/M2. (Both Mac versions work on an ARM chip.)
This program uses Python 3.11 and PyGame 2.5.1 (https://www.pygame.org/contribute.html)

**Before using the program:**
Download the zip file under the Code menu. 
Create text files for each session you want to save times for.
It is recommended that the file names be short. 
Files should be formatted similar to the example file (example.txt) and use the .txt extension.
Any average type can be recorded for PB purposes, on line 3 of the .txt file.
Place these files in the same folder as the download.
Change the configuration settings to your liking.
Run the executable file corresponding to your operating system.

**Configuration Settings:**
The averages or means displayed can be changed by listing up to 4 of them on the first line.
Note that averages start with "a" or "A" and means start with "m" or "M".
Font type and sizes can be changed on their respective lines.
The color of the background and text can be changed by typing in RGB values, only R,G,B is acceptable. 

**While running:**
To use the program, type in the session name to save the results to, then the puzzle type for the scramble.
Press the Enter key on the keyboard to generate new scrambles.
Scrambles are only generated for WCA puzzles!
Type in a time and press Enter while the cursor is on the time input to save the time.
Times should be formatted like HH:MM:SS.XX, XXXX.XX, or MMSSXX.
Averages are automatically calculated at the bottom of the screen. 
Note that all times displayed and saved are formatted like XXXX.XX

**To exit:**
Click on the exit button.

__For contributors:__
Bash scripts are provided to compile the program for MacOS only.
Please use PyInstaller >= 6.0.0 when compiling the program and name the resulting executable file appropriately.
If you are compiling for a new OS, please also add a new compiliation shell script to expedite future contibutions.
