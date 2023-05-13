# item_toss_counter
 recognizes and counts the number of each type of item tossed in guilty gear strive

Setup:
you need python for this

install opencv (image recognition): pip install opencv-python
install pillow (screenshots): pip install pillow

to run: 
set dummy to faust, set it to toss item after position reset.
if not generating your own templates to recognize images, use the following settings in training mode:
dummy: faust color 2
stage: Lars Canyon
dummy on p1 side (idk why i did that, but that's how it is.)

Now run collect_data.py (make sure you set the buttons you want to use at the top of the file)
python collect_data.py
swap to strive, hit the chosen start button. toss as many items as you want and hold the quit button when you're ready to store the data. Your data should now be in a new file called item_counts.csv.

if that doesn't work, you may need to generate your own templates.
to do that:
choose a stage with little to no random variation. Lars canyon is pretty good for this.
dummy colors don't matter, neither does the side. just keep it constant when you collect data.
set dummy to toss item on position reset
set item to bomb.
In your terminal run screenshotter.py (python screenshoter.py). follow the instructions in your terminal. Once again, set the buttons that you want at the top of the file. You will need to take a second screenshot to get the peel (once again, follow the instructions in the terminal). If you got peel when you first chose banana, toss until you hit a banana, then swap the file names manually. After any item toss you may press the quit button to stop if you think you got a bad screenshot. 

delete the old template images, and replace them with your screenshots. Crop to minimize the size of the templates, while still being recognizable. Now run collect_data.py as described above.