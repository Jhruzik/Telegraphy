# Telegraphy

This project will transform any String message into Morse code that will be played by a buzzer connected to a Raspberry Pi.

## Setup
In order to recreate my working setup you will need the following setup:
* 1x Raspberry Pi
* 1x Active Buzzer
* 4x Jumper Cables
* 1x 1K Ohm Resistor
* 1x 220 Ohm Resistor
* 1x NPN Transistor

The wiring should look like this:
![Sketch](https://raw.githubusercontent.com/Jhruzik/Telegraphy/main/Sketch.png)

Note that the 220 Ohm resistor between 5V and the active buzzer is optional. I included it to decrease the buzzer's volume.

Make sure to install RPi.GPIO to access your Raspberry Pi's GPIO pins from Python:
```
pip install RPi.GPIO
```

## CLI
After recreating the setup and installing GPi.GPIO, you can use the command line like so:
```
python telegraphy.py 11 "Hello World"
```

The first argument must always be the physical pin location you want to use to emit the electrical signal. In my case, I use GPIO17 which is equal to pin 11 in my setup. The second argument will be the message to morse in double quotes. Notice that your message must only contain letters that are also present in the Morse alphabet. I included Umlauts to also render German messages.

## Notice
I am by no means a professional electrician. Hence, I take no responsibility for any damage that may result. This is a hobby project done to learn about the Raspberry Pi and electricity.

## License
This project is licensed under the MIT license. RPi.GPIO was also licensed under MIT.
