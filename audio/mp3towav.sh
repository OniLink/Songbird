#!/bin/bash

for i in *.MP3; do ffmpeg -i "$i" -f segment -segment_time 3600 "${i%.*}_out_%03d.wav"; done
for i in *.mp3; do ffmpeg -i "$i" -f segment -segment_time 3600 "${i%.*}_out_%03d.wav"; done
