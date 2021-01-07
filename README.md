# Telegraphy

This project will transform any String message into Morse code that will be played by a buzzer connected to a Raspberry Pi. Also, the Message will be played to a small LCD.

## Setup
In order to recreate my working setup you will need the following setup:
* 1x Raspberry Pi
* 1x Active Buzzer
* 8x Jumper Cables
* 1x 1K Ohm Resistor
* 1x 220 Ohm Resistor
* 1x NPN Transistor
* 1x I2C LCD1602

The wiring should look like this:
![Sketch](https://raw.githubusercontent.com/Jhruzik/Telegraphy/main/Sketch.png)

Note that the 220 Ohm resistor between 5V and the active buzzer is optional. I included it to decrease the buzzer's volume. 

In this sketch you don't actually see an LCD. Instead an Adafruit Char LCD is connected to an I2C pcf8574 adapter which is hooked up to the Raspberry Pi.

Make sure to install RPi.GPIO to access your Raspberry Pi's GPIO pins from Python:
```
pip install RPi.GPIO
```

Also, you need the drivers for the LCD in the same folder where this script is located at. You can download the drivers from [Freenove's Github Repo](https://github.com/Freenove/Freenove_Ultimate_Starter_Kit_for_Raspberry_Pi/tree/master/Code/Python_Code/20.1.1_I2CLCD1602). Make sure to download the driver for [PCF8574](https://raw.githubusercontent.com/Freenove/Freenove_Ultimate_Starter_Kit_for_Raspberry_Pi/master/Code/Python_Code/20.1.1_I2CLCD1602/PCF8574.py) and the [Adafruit Char LCD](https://raw.githubusercontent.com/Freenove/Freenove_Ultimate_Starter_Kit_for_Raspberry_Pi/master/Code/Python_Code/20.1.1_I2CLCD1602/Adafruit_LCD1602.py). Download and place these files wherever this script is located at.

## CLI
After recreating the setup and installing GPi.GPIO, you can use the command line like so:
```
python telegraphy.py 11 3 "Hello World"
```

The first argument must always be the physical pin location you want to use to emit the electrical signal for the buzzer for. In my case, I use GPIO17 which is equal to pin 11 in my setup. The second argument is the SDA pin for the pcf adapter. In my setup it is pin 3. Finally, the third argument will be the message to morse in double quotes. Notice that your message must only contain letters that are also present in the Morse alphabet. You can also use Umlauts since they will be translated into the English counter part.

## Notice
I am by no means a professional electrician. Hence, I take no responsibility for any damage that may result. This is a hobby project done to learn about the Raspberry Pi and electricity.

## License
This project is licensed under the MIT license. RPi.GPIO was also licensed under MIT.
