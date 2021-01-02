# Make Imports
import RPi.GPIO as GPIO
import re
import argparse
from time import sleep


# Define Morse Alphabet
morse_code_dict = { 'A':'.-', 'B':'-...',
                    'C':'-.-.', 'D':'-..', 'E':'.',
                    'F':'..-.', 'G':'--.', 'H':'....',
                    'I':'..', 'J':'.---', 'K':'-.-',
                    'L':'.-..', 'M':'--', 'N':'-.',
                    'O':'---', 'P':'.--.', 'Q':'--.-',
                    'R':'.-.', 'S':'...', 'T':'-',
                    'U':'..-', 'V':'...-', 'W':'.--',
                    'X':'-..-', 'Y':'-.--', 'Z':'--..',
                    '1':'.----', '2':'..---', '3':'...--',
                    '4':'....-', '5':'.....', '6':'-....',
                    '7':'--...', '8':'---..', '9':'----.',
                    '0':'-----', ', ':'--..--', '.':'.-.-.-',
                    '?':'..--..', '/':'-..-.', '-':'-....-',
                    '(':'-.--.', ')':'-.--.-', ' ': ' ',
                    'Ä':'.-.', 'Ö':'---.', 'Ü':'..-.'}


# Translate Message to Morse Alphabet
def translate(msg: str) -> str:

    # Normalize Message
    msg_clean = re.sub("\s+", " ", msg)
    msg_clean = msg_clean.upper()

    # Check for Non-Existing Characters
    msg_dict = set(msg_clean)
    unkown_chars = msg_dict - set(morse_code_dict.keys())
    if len(unkown_chars) > 0:
        raise ValueError("The following characters don't exist in the Morse Alphabet: ['{}']".format("', '".join(unkown_chars)))

    # Code Message
    msg_coded = []
    for letter in msg_clean:
        msg_coded.append(morse_code_dict[letter])
    msg_coded = "".join(msg_coded)

    # Return Coded Message
    return msg_coded


# Play Message
def play(pin: int, msg: str):

    # Function to Play Tone
    def _beep(pin: int, t: float):
        GPIO.output(pin, GPIO.HIGH)
        sleep(t)
        GPIO.output(pin, GPIO.LOW)

    # Play Short Tone
    def _short(pin: int):
        _beep(pin, 0.1)

    # Play Long Tone
    def _long(pin: int):
        _beep(pin, 0.3)

    # Play Message
    pause = 0.3
    for tone in msg:
        if tone == '.':
            _short(pin)
            sleep(pause)
        elif tone == "-":
            _long(pin)
            sleep(pause)
        elif tone == " ":
            sleep(0.7)


# Setup RaspberryPi
def setup(pin: int):
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(pin, GPIO.OUT)


# Clean Up RaspberryPi
def destroy():
    GPIO.cleanup()


# Start Program
if __name__ == "__main__":

    # Parse User Arguments
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('pin', type=int, help='Physical number of GIPO pin')
    parser.add_argument('message', type=str, help='Message to morse')
    args = parser.parse_args()
    pin = int(args.pin)
    msg = args.message

    # Translate Message into Morse Code
    msg_coded = translate(msg)

    # Configure RPi
    setup(pin)

    # Morse Message
    try:
        play(pin, msg_coded)
    except Exception as e:
        raise e
    finally:
        destroy()
