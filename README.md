# Hardware Challenge 1
## Goal
Sense the environment in some way of your choice (light, temperature, sound, water level in your plant, etc.) and respond somehow.  Go to @290 for posting your submission.

## Description
In this project, I am familiarizing myself with interacting with the GoPiGo board as well as learning how to use attached sensors.

This project uses a Grove loudness sensor to determine how loud the ambient noise is. 

Every few seconds, the loudness sensor samples the sound level 10k times. After collecting the samples, it determines the average loudness.  The GoPiGo eyes are used to indicate the relative "safety" of the volume level.

Volume Levels:
- Green - quiet
- Pink - noisy
- Red - put in your ear plugs.
 
