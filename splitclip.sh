#!/bin/bash

fileName=$1
segmentSize=$2
ffmpeg -i $fileName -f segment -segment_time $segmentSize  -c copy out%03d.mp3
