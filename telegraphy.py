# Make Imports
import RPi.GPIO as GPIO
import re
import argparse
from time import sleep
from PCF8574 import PCF8574_GPIO
from Adafruit_LCD1602 import Adafruit_CharLCD


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
                    '0':'-----', ',':'--..--', '.':'.-.-.-',
                    '?':'..--..', '/':'-..-.', '-':'-....-',
                    '(':'-.--.', ')':'-.--.-', ' ': ' '} 


# Check Message
def check_message(msg:str, alphabet: set) -> bool:
    letters = set(msg.upper())
    return len(letters-alphabet) == 0


# Play Tone
def play(pin: int, tone: str):

    # Check User Input
    if tone not in [".", "-"]:
        raise ValueError("Tone must be either '.' or '-'")

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

    # Play Tone
    pause = 0.1
    if tone == '.':
        _short(pin)
        sleep(pause)
    elif tone == "-":
        _long(pin)
        sleep(pause)

# Show Letter
def show(lcd, letter: str, line: int, column: int):
    lcd.setCursor(column, line)
    lcd.message(letter)


# Setup RaspberryPi
def setup(pin: int):
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(pin, GPIO.OUT)


# Create LCD
def create_lcd(pin):

    # Setup Display
    PCF8574_address = 0x27
    PCF8574A_address = 0x3F

    # Create MCP
    try:
        mcp = PCF8574_GPIO(PCF8574_address)
    except Exception:
        try:
            mcp = PCF8574_GPIO(PCF8574A_address)
        except Exception as e:
            raise e
    lcd = Adafruit_CharLCD(pin_rs=0, pin_e=2, pins_db=[4,5,6,7], GPIO=mcp)

    # Turn on LCD
    mcp.output(pin,1)
    lcd.begin(16, 2)

    # Return LCD
    return lcd


# Clean Up RaspberryPi
def destroy():
    GPIO.cleanup()


# Start Program
if __name__ == "__main__":

    # Parse User Arguments
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('pin_buzzer', type=int, help='Physical number of GPIO pin for buzzer')
    parser.add_argument("pin_lcd", type=int, help="Physical number og GPIO pin for LCD")
    parser.add_argument('message', type=str, help='Message to morse')
    args = parser.parse_args()
    pin_buzzer = int(args.pin_buzzer)
    pin_lcd = int(args.pin_lcd)
    msg = args.message

    # Replace Umlauts in Message
    msg = msg.replace("Ä", "Ae")
    msg = msg.replace("ä", "ae")
    msg = msg.replace("Ö", "Oe")
    msg = msg.replace("ö", "oe")
    msg = msg.replace("Ü", "Ue")
    msg = msg.replace("ü", "ue")

    # Check if Message is valid
    morse_alphabet = set(morse_code_dict.keys()) 
    if check_message(msg, morse_alphabet) is False:
        raise ValueError("There are letters in your message not present in the Morse alphabet")

    # Configure RPi
    setup(pin_buzzer)

    # Create LCD
    lcd = create_lcd(pin_lcd)

    # Morse Message
    try:

        # Set Initial Cursor Position
        lcd.clear()
        index = 0
        lcd.setCursor(index, 0)
       
        # Split Message into Words
        msg_split = re.split(r"\s+", msg)
        
        # Iterate through Message
        for word in msg_split:

            # Calculate Space Left
            space_left = 32-index
            if len(word) > space_left and len(word) < 32:
                lcd.clear()
                index = 0

            # Play and Show Letter
            for letter in word:

                # Show Letter
                if index >= 16:
                    lcd.setCursor(index - 16,1)
                if index > 31:
                    lcd.clear()
                    index = 0
                    lcd.setCursor(index, 0)
                lcd.message(letter)
                index += 1

                # Play Tone
                morse_code = morse_code_dict[letter.upper()]
                for tone in morse_code:
                    play(pin_buzzer, tone)
                sleep(0.3) # Pause between Sounds
            
            # Pause between Word
            sleep(0.7)

            # Print Space
            if index != 16:
                lcd.message(" ")
                index += 1

    except Exception as e:
        raise e
    finally:
        destroy()
        lcd.clear()
