
Use video.erl to generate a bunch of image.png files. First start "erl" interpreter, then use the command: "video:main()".

use make_video.sh to turn all the pngs into a video.mp4


README for the python portion below VVV

mandelbrotG5
============

A Python 2.7 script for creating arbitrarily hi resolution images of the Mandelbrot set. It works by spawning processes that create rows of escape time values in a big shared arary. The main process starts all the workers and then iterates through the shared array, generates colors from the escape time values, and then writes the data to a file.

Some benchmark info: on my laptop (Dell Precision M6600 with Core i7 2920XM) it takes 46 minutes to create a 30k x 20k image.

The code has two dependencies: pypng and numpy. 

This project is dedicated to my beautiful PowerMac G5 Quad (R.I.P.)


