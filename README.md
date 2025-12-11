# moneyclicker
Simple, cross-platform lightweight auto clicker made in Python, with support for some keypress spamming.

Made with stackoverflow and reorganized by ChatGPT at one point (not vibe coded)

## What is Moneyclicker?
Moneyclicker is a simple autoclicker utility for games. It's not incredibly feature rich or pretty looking, but it gets the job done. Because it's made in Python, it runs on anything from a Raspberry Pi to a Walmart special GT 1030 "Gaming PC" to a Mac Mini. The language limits the speed it can run at, but testing indicates that's the least of your worries compared to other programs like OP Auto Clicker that are made in more performant languages but still limit you to around 45CPS.

## What can I expect from Moneyclicker?
When the click rate is optimally tuned, you can expect anywhere from 1055CPS to 3600CPS. You can also expect similar from the keyboard spamming function, which can replay steps of a recorded "macro" at this speed. However, the speed decreases as the clicking rate decreases beyond what your system can handle. A good rule of thumb is to set the operation rate to the refresh rate of your monitor, for stable performance while still offering fast clicks. For example, if your monitor is 144hz, set the rate to 0.0069, etc. 

## Why is Moneyclicker so bare?

It's to keep it simple. Of course, it could have a more organized UI, which I plan to do at some point, but by introducing a bunch of APIs, failsafes, or tangential features, it vastly increases the risk of edge cases fucking something up or updates rendering Moneyclicker unusable if testing can't be done for all cases. It's also optimized for the absolute minimal security risk; querying the OS for certain things, trying to look for files, or storing extra data could be a large security risk in the wrong hands. So, of course, I kept it minimal and functional, two modules and nothing like an icon (that could also possibly display wrong on different operating systems or themes).

## What is planned for Moneyclicker in the future?

Not much, as I plan to keep it simple, as stated above. I will reorganize the UI to be more intuitive in the future, possibly offer different languages as their own scripts (to prevent bloat), and possibly add a feature that automatically optimizes your clicking rate or calculates CPS to sleep time rate, as it is currently very rudimentiary. The current rate system was chosen to prevent confusion over why the CPS is not what was requested of the program, and offer more precision.

## How do I set up Moneyclicker?

On Windows, install Python, and download the code as .zip, or clone the repo. Then navigate to the folder that you extracted Moneyclicker to, or the folder that you cloned the repo to. Open CMD and type:

```pip install -r requirements.txt```

Confirm that you want to install them, if prompted, by typing Y.

You can then double click money.pyw. It was named .pyw to prevent window clutter.

On Linux, Python is already installed, however Git can be difficult to write instructions for across distros, so download the code as .zip and extract it. Once you navigate to the folder containing money.pyw, install the requirements, which can be done on Ubuntu/Debian-based distros by typing ```sudo python3 -m venv moneyclicker```, ```source moneyclicker/bin/activate```, and then ```pip3 install tk pynput```. To run it, type ```python3 ./money.pyw```

On macOS, which I personally have not tested, Python should be installed if it is not already. You should then download the code as .zip and run money.pyw.
Support is needed here! macOS testers will be credited.

Moneyclicker is licensed under GPL 2.0 (as if that mattered, it's not all that serious). But that does mean that you can copy it and do whatever cursed shit you wanna do with it. It's not going to change licenses, at least in a way that would prevent open source code sharing and modification.
