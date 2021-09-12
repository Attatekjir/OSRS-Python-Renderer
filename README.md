# OSRS-Python-Renderer

Renderer of OSRS terrains implemented in Python. Based on the Java implementation of VirtueOS: https://github.com/clienthax/VirtueOS

This project is not really meant for others to interact with so expect jank and code uglyness. You can raise an issue if something does work or is unclear and maybe ill be bothered enough to look at the issue/help but do not expect anything.
Purpose of this project: Render a scene with specified parameters.
NOT the purpose of this project: 'Playable' OSRS client.

Seperated lots of data from classes, which is present in the Java version: Pro's: No spaghetti interaction between classes; clearer start and end. Con's: Lots of boilerplate handing down data structures through functions.

SETUP:
1. obtain a cache195 (2021-05-05-rev195) and put it somewhere on your computer. 
2. Make the variable 'cache_folder' point towards the cache195 folder in Main.py file
3. Install the required packages
4. Run Main.py
5. Takes about two minutes to set everything up. zzz! (but rendering the scenes afterwards is done in miliseconds)
6. If succesfull a seperate window will appear with an interactable window where u can move the camera around with the keys: A, W, S, D, C, SPACEBAR, LEFT ARROW, RIGHT ARROW, UP ARROW, DOWN ARROW to look around. (You can resize the window aswell)
7. Change the region you wish to look at by altering the variables self.xregion and self.yregion in the code. You have to restart the entire code again to see the change.

Required packages: numpy, numba, jupyter notebook, pandas, matplotlib, PyQt5... and more if it still does not run :).

k

