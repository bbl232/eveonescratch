from __future__ import division
import spidev
import time


def bitstring(n):
	s = bin(n)[2:]
	return '0'*(8-len(s)) + s

def read(adc_channel, spi_channel):
	conn = spidev.SpiDev()
	conn.mode = 0
	conn.open(0,spi_channel)
	cmd = 0xC0 			
	if adc_channel: 		#HEX - set the EVEN/SIGN bit to select channel number 0
		cmd = 0xE0 		#HEX - set the ODD/SIGN bit to select channel number 1
	try:
		reply_bytes = conn.xfer2([cmd, 0x00])
		#print reply_bytes
		reply_bitstring = ''.join(bitstring(n) for n in reply_bytes)
		reply = reply_bitstring[5:15]
		conn.close()
		return int(reply, 2)    # Reply = Number of Count * reference / full range of counts.
	except KeyboardInterrupt:
		conn.close()		#close the SPI Port to exit cleanly.
		print "Exiting..."

