# Hardware Challenge 1 - EarBot
## Goal
Sense the environment in some way of your choice (light, temperature, sound, water level in your plant, etc.) and respond somehow. 

## Description
In this project, I am familiarizing myself with interacting with the GoPiGo board as well as learning how to use attached sensors.

This project uses a Grove loudness sensor to determine how loud the ambient noise is. 

Every few seconds, the loudness sensor samples the sound level 10k times. After collecting the samples, it determines the average loudness.  The GoPiGo eyes are then used to indicate the relative "safety" of the volume level.

Volume Levels:
- Green - quiet
- Pink - noisy
- Orange - put in your ear plugs
- Red - danger, Will Robinson.

![Loudness Sensor](/ch1-img/loudnesssensor.png)

## Demo
[Demonstration Video](https://youtu.be/FjBthg8KJLI)

![Output Log](/ch1-img/log.png)
 
Resources:
- GoPiGo Loudness Sensor - https://gopigo3.readthedocs.io/en/master/api-basic/sensors.html#loudnesssensor
- GoPiGo Eye Color - https://gopigo3.readthedocs.io/en/master/api-basic/easygopigo3.html#easygopigo3.EasyGoPiGo3.set_eye_color
- GoPiGo Port Layout - https://gopigo3.readthedocs.io/en/master/api-basic/structure.html#hardware-ports
- RGB Color Lookup - https://www.colorhexa.com/ffa500

# Hardware Challenge 2 - WanderBot
## Goal
Affect the environment in some way of your choice (move an object, make a robot drive or fly in a controlled way, turn an appliance on/off, or even just blink an LED)

## Description
In this project, I am familiarizing myself with GoPiGo movement as well as a new sensor and capability. In my implementatioon, I will use a Dexter Industries distance sensor to measure the distance to a "wall" and the Dexter Industries servo to adjust the sensor angle.

Given the set of measurements, my robot will attempt to autonomously follow the walls of his sad, rectangular world.

![Distance Sensor](/ch2-img/distancesensor.png)

## Demo
[Demonstration Video - Square World](https://youtu.be/FjBthg8KJLI)
[Demonstration Video - Rectangle World](https://youtu.be/Kk-F6yqSJXA)


Resources:
- GoPiGo Distance Sensor - https://di-sensors.readthedocs.io/en/master/api-basic.html#di_sensors.easy_distance_sensor.EasyDistanceSensor
- GoPiGo Servo - https://gopigo3.readthedocs.io/en/master/api-basic/sensors.html#servo
- GoPiGo Movement - https://gopigo3.readthedocs.io/en/master/tutorials-basic/driving.html
