
CONTENT
        1. INTRODUCTION
        2. FILE MANIFEST
        3. INSTALLATION
        4. USAGE

1. INTRODUCTION

This is the README file for Booking.com scraper tool.

This package contains python scripts, python standalone modules(to avoid from installs), browser drivers for selenium.
Performance of this tool depends on selenium framework which is a little bit heavy engine.
From configs.txt you can increase the number of threads to run the browsers parallel, which will increase the speed.
Be careful with threads numbers, do not choose higher than 15 if you don't have a strong servers.
Start from 3, if the computer is not hanging increase the number.

2. FILE MANIFEST

modules/           : Python standard modules

drivers/           : drivers for phanthomjs, chrome and firefox needed by selenium framework

configs.txt/       : configuration file for the tool(i.e number of threads, what browser to use, output format, etc.)

extractor.py/      : main executable script

booking.py, hotel.py, utilities.py : other python files (not interesting)

output.xlsx/json   : output json or excel file

input.xlsx         : input file containing search parameters

3. INSTALLATION

Windows: 
	Install python :
	- Download and install python3. When installing enable "Add python3 to PATH" checkbox.
	- Download and install a browser (firefox or chrome)
	Install python modules:
	- open windows command prompt
	> pip3 install lxml
        > pip3 intsall html5lib
	> pip3 install pandas

Linux (Ubuntu):
	Install python and modules from terminal:
	- open linux terminal
	> sudo apt-get install python3
	> sudo apt-get install python3-pip
	> sudo apt-get install chromium-browser (or firefox)
        > sudo pip3 install lxml
	> sudo pip3 install html5lib
	> sudo pip3 install pandas
	> sudo pip3 install easyprocess
	> sudo pip3 install pyvirtualdisplay

4. USAGE 

Open terminal and run: 
	> python3 extractor.py