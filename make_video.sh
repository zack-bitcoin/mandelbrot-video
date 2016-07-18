#!/bin/bash


rm video.mp4
sh resize.sh

#ffmpeg -framerate 1/5 -start_number 4 -i image%02d.png -c:v libx264 -r 30 -pix_fmt yuv420p video.mp4
ffmpeg -framerate 1/7 -pattern_type glob -i 'exact*.jpg' -i audio.mp3 -c:v libx264 -r 1 -c:a copy -shortest video.mp4


