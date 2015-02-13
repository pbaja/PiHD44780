import smbus
from time import sleep

En = 0b00000100 # Enable bit
Rw = 0b00000010 # Read/Write bit
Rs = 0b00000001 # Register select bit
BLon = 0x08     # Backlight on
BLoff = 0x00    # Backlight off

class HD44780:

#################################################################
#            LOW LEVEL FUNCTIONS, CAN'T TOUCH THIS!             #
#################################################################

	def __init__(self,addr=0x27,port=1,backlight=True):
		self.currentline = 0
		self.bus = smbus.SMBus(port)
		self.addr = addr;
		self.setBacklight(backlight)

		#Prepare LCD
		self._cmdWrite(0x03)
		self._cmdWrite(0x03)
		self._cmdWrite(0x03)
		self._cmdWrite(0x02)

		self._cmdWrite(0x33)
		self._cmdWrite(0x32)
		self._cmdWrite(0x28) # Send data in 4 bit, 2 lines, 5x7 pixels
		self._cmdWrite(0x0C) # Hide cursor
		self._cmdWrite(0x06) # Writing mode (From left to right)
		self._cmdWrite(0x01) # Clear screen

		# Custom chars
		self.setCustomChar(0,[0x00, 0x00, 0x04, 0x0E, 0x1F, 0x00, 0x00, 0x00]) # ARROW UP
		self.setCustomChar(1,[0x00, 0x00, 0x00, 0x1F, 0x0E, 0x04, 0x00, 0x00]) # ARROW DOWN
		self.setCustomChar(2,[0x1F, 0x1F, 0x1B, 0x15, 0x0E, 0x1F, 0x1F, 0x1F]) # ARROW UP NEG
		self.setCustomChar(3,[0x1F, 0x1F, 0x1F, 0x0E, 0x15, 0x1B, 0x1F, 0x1F]) # ARROW DOWN NEG

		sleep(0.2)	
	def _busWrite(self, data):
		#Set data pins
		self.bus.write_byte(self.addr,data | self.backlight)
		#Send data to lcd
		self.bus.write_byte(self.addr,data | En | self.backlight)
		sleep(.0005)
		self.bus.write_byte(self.addr,((data & ~En) | self.backlight))
		sleep(.0001)	
	def _cmdWrite(self, cmd, mode=0):
		#Send first 4 bytes
		self._busWrite(mode | (cmd & 0xF0))
		#Send last 4 bytes
		self._busWrite(mode | ((cmd << 4) & 0xF0))

#################################################################
#                    MEDIUM LEVEL FUNCTIONS                     #
#################################################################

	def setCustomChar(self,pos,char):
		positions = [0x40,0x48,0x50,0x58,0x60,0x68,0x70,0x78]
		self._cmdWrite(positions[pos])
		for i in char:
			self._cmdWrite(i,Rs)

	def customChar(self, charId):
		self._cmdWrite(charId,Rs)

#################################################################
#                 HIGH LEVEL FUNCTIONS FOR USER                 #
#################################################################

	def writeMsg(self, text, time=0,homing=True):
		if homing:
			self.currentline=0
			self.home()
		for char in text:
			if char == '\n': # NEW LINE
				self.nextLine()
			elif char == '\a': # ARROW UP
				sleep(time)
				self._cmdWrite(0,Rs)
			elif char == '\b': # ARROW DOWN
				sleep(time)
				self._cmdWrite(1,Rs)
			elif char == '\f': # ARROW UP NEG
				sleep(time)
				self._cmdWrite(2,Rs)
			elif char == '\t': # ARROW DOWN NEG
				sleep(time)
				self._cmdWrite(3,Rs)
			else:
				sleep(time)
				self._cmdWrite(ord(char),Rs)

	def clear(self):               # Clear display 
		self._cmdWrite(0x01)
	def scrollRight(self):         # Move all characters right
		self._cmdWrite(0x1E)
	def scrollLeft(self):          # Move all characters left
		self._cmdWrite(0x18)
	def blank(self):               # Hide all characters
		self._cmdWrite(0x08)
	def restore(self):             # Show all characters
		self._cmdWrite(0x0C)
	def setBacklight(self, value): # Power on/off backlight
		self.backlight = BLon if value else BLoff

	def home(self):         # Move cursor to left, top corner
		self._cmdWrite(0x02)
		self.currentline = 0
	def cursorRight(self):  # Move cursor one place right
		self._cmdWrite(0x02)
	def cursorLeft(self):   # Move cursor one place left
		self._cmdWrite(0x02)
	def nextLine(self):     # Move cursor to next line
		self.setLine(self.currentline+1)
	def setLine(self,line): # Move cursor to line
		if line == 0:
			self._cmdWrite(0x80)
		elif line == 1:
			self._cmdWrite(0xC0)
		elif line == 2:
			self._cmdWrite(0x94)
		elif line == 3:
			self._cmdWrite(0xD4)
		self.currentline = line