from LimeLCD import HD44780
from time import sleep, time, localtime, strftime

# HD44780(ADDRESS,PORT)
# Default: 0x27,1
lcd = HD44780()

#
# AVAILABLE FUNCTIONS
#
#clear()           # Clear display
#scrollRight()     # Move all characters right
#scrollLeft()      # Move all characters left
#blank()           # Hide all characters
#restore()         # Show all characters
#home()            # Move cursor to left, top corner
#cursorRight()     # Move cursor one place right
#cursorLeft()      # Move cursor one place left
#nextLine()        # Move cursor to next line
#setLine(line)     # Move cursor to line (Starting with 0)

lcd.writeMsg("1234567890ABCDEF\nTEST TEST TEST\n!@#$%^&*()_+{}:<\"\nOh god 3rd line!")
sleep(3)
lcd.clear()
lcd.writeMsg("Clearing in 3")
sleep(1)
lcd.writeMsg("2",0,False)
sleep(1)
lcd.writeMsg("1",0,False)
sleep(1)
lcd.clear()
sleep(3)
lcd.writeMsg("Nice animation!",0.1)
lcd.writeMsg("\nKab",0.5,False)
lcd.writeMsg("oooo",0.1,False)
lcd.writeMsg("m",0,False)
sleep(1)

lcd.clear()
lcd.writeMsg("Current time is:")
while True:
	lcd.setLine(1)
	lcd.writeMsg("   "+strftime("%H:%M:%S", localtime()),0,False)
	sleep(1)