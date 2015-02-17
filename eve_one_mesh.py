from array import array
import socket
import time
import sys
import scratch
import RPi.GPIO as GPIO
import spidev
import thread

GPIO.cleanup()

def parse_broadcast(msg,pin_map,out_pins):
  try:
    if msg[0] == "broadcast":
      args = msg[1].split(' ')
      pin = args[0].upper()
      try:
        state = args[1].lower()
        GPIO.output(pin_map[pin], (0 if state == "off" else 1))
      except IndexError:
        pass
  except Exception:
    pass


def listen(s,pin_map,out_pins):
  while True:
    try:
      msg = s.receive()
      parse_broadcast(msg,pin_map,out_pins)
    except scratch.ScratchError:
      while not s.connected:
        try:
          s.connect()
        except scratch.ScratchError:
          pass
        time.sleep(0.1)


def _eve_adc_bitstring(n):
	s = bin(n)[2:]
	return '0'*(8-len(s)) + s

def _eve_adc_read(adc_channel, spi_channel):     
	conn = spidev.SpiDev()		
        conn.lsbfirst = False
	conn.mode = 0			
	conn.open(0,spi_channel) 	
	
	cmd = 0xC0 			
	if adc_channel: 	
		cmd = 0xE0 	
	try:		
		reply_bytes = conn.xfer2([cmd, 0x00])
		reply_bitstring = ''.join(_eve_adc_bitstring(n) for n in reply_bytes)
		reply = reply_bitstring[5:15]
		conn.close()
		return int(reply, 2)  
	except KeyboardInterrupt:
		conn.close()		
		print "Exiting..."



PORT = 42001
HOST = "127.0.0.1"

s = lambda:0 
s.connected=False

while not s.connected:
  try:
    s = scratch.Scratch(host=HOST,port=PORT)
  except scratch.ScratchError:
    pass

pin_map = {
  'SDA':3,
  'SCL':5,
  '4':7,
  'TXD':8,
  'RXD':10,
  '17':11,
  '18':12,
  '21':13,
  '22':15,
  '23':16,
  '24':18,
  'MOSI':19,
  'MISO':21,
  '25':22,
  'SCLK':23,
  'CE0':24,
  'CE1':26
}

GPIO.setmode(GPIO.BOARD)

out_pins=['SDA','SCL','4','TXD','RXD','17','18','21']
in_pins= ['22','23','24','25','CE1']

for p in out_pins:
  GPIO.setup(pin_map[p],GPIO.OUT)

for p in in_pins:
  GPIO.setup(pin_map[p],GPIO.IN,pull_up_down=GPIO.PUD_DOWN)

t = thread.start_new_thread(listen,(s,pin_map,out_pins))

while True:
  sensors = {};
  for p in in_pins:
    sensors[p] = (0 if GPIO.input(pin_map[p]) == GPIO.LOW else 1)
  sensors['adc0'] = _eve_adc_read(0,0)
  sensors['adc1'] = _eve_adc_read(1,0)

  try:
    s.sensorupdate(sensors)
  except scratch.ScratchError:
    pass

  time.sleep(0.1)
