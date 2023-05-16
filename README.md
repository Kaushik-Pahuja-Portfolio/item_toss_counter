# item_toss_counter
 recognizes and counts the number of each type of item tossed in guilty gear strive

**Setup:**

you need python for this

install opencv (image recognition): `pip install opencv-python`

install pillow (screenshots): `pip install pillow`

**Collecting Data**
if not generating your own templates to recognize images, use the following settings in training mode:

stage: Lars Canyon

p1: faust color 2 (other colors may work, but I have not tested them)

In `keybinds.py`, set your keybinds following the comment instructions

in `collect_data.py`, set the toss_order list. all items are one word, lowercase. this program will only record "normal" item tosses.

if generating your own templates (see below) simply keep the same settings you used when creating those

Now run collect_data.py :

`python collect_data.py`

swap to strive, hit the chosen start button. toss as many items as you want and press the quit button when you're ready to store the data. Your data should now be in  `item_counts.csv`.

if that doesn't work, you may need to generate your own templates.

choose a stage with little to no random variation. Lars canyon is pretty good for this.
skins don't matter, nor does the side. just keep it the same when you collect data.

set item to bomb.

In your terminal run `screenshotter.py` (`python screenshoter.py`). follow the instructions in your terminal. You will need to take a second screenshot to get the peel (once again, follow the instructions in the terminal). If you got peel when you first chose banana, toss until you hit a banana, then swap the file names manually. After any item toss you may press the quit button to stop if you think you got a bad screenshot. 

delete the old template images, and replace them with your screenshots. Crop to minimize the size of the templates, while still being recognizable. Try to avoid including the stage and faust's fingers. Faust's finger positioning is literally rng. Now run `collect_data.py` as described above.
