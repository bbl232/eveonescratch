from array import array
import socket
import time
import sys
import scratch
import signal
import RPi.GPIO as GPIO
import spidev
import Adafruit_MPR121.MPR121 as MPR121
import thread
import os

pwm = {}
cap = MPR121.MPR121()
pin_map = {
  '04':7,
  'TXD':8,
  'RXD':10,
  '17':11,
  '18':12,
  '21':13,
  '22':15,
  '23':16,
  '24':18,
  '25':22,
  'SCLK':23,
  'CE0':24,
  'CE1':26
}

GPIO.setmode(GPIO.BOARD)

out_pins=['04','TXD','RXD','17','18','21']
in_pins= ['22','23','24','25','CE1']

if os.path.exists("/opt/eveonescratch/._eveOne_mpr_enabled"):
  os.remove("/opt/eveonescratch/._eveOne_mpr_enabled")

def mpr_enable():
  try:
    if not cap.begin(address=0x5A,busnum=1):
      print 'Error, could not initialize'
    else:
      os.mknod("/opt/eveonescratch/._eveOne_mpr_enabled")
      print 'Successfully enabled'
  except Exception:
    pass

def read_touch():
  values = []
  
  try:
    touched = cap.touched()
    for i in range(12):
      bit = 1 << i
      values.append(1 if touched & bit else 0)

    return values
  except Exception:
    pass

def parse_broadcast(msg):
  try:
    if msg[0] == "broadcast":
      args = msg[1].split(' ')
      if args[0].lower() == "pwm":
        pin = args[1].upper()
        if args[2].lower() == "off":
          pwm[pin].stop()
          del pwm[pin]
        elif pin in pwm and float(args[2])>=0.0 and float(args[2])<=100.0:
          pwm[pin].ChangeDutyCycle(float(args[2]))
        elif pin not in pwm and float(args[2])>=0.0 and float(args[2])<=100.0:
          pwm[pin] = GPIO.PWM(pin_map[pin], 50)
          pwm[pin].start(float(args[2]))
      elif args[0].lower() == "mpr121":
        if args[1].lower() == "on":
          mpr_enable()
      else:
        pin = args[0].upper()
        try:
          state = args[1].lower()
          GPIO.output(pin_map[pin], (0 if state == "off" else 1))
        except IndexError:
          pass
  except Exception:
    pass

def listen(s,g):
  while True:
    try:
      msg = s.receive()
      parse_broadcast(msg)
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
    print "Could not connect to scratch, waiting 2s..."
    time.sleep(2)
    pass

for p in out_pins:
  GPIO.setup(pin_map[p],GPIO.OUT)

for p in in_pins:
  GPIO.setup(pin_map[p],GPIO.IN,pull_up_down=GPIO.PUD_DOWN)

t = thread.start_new_thread(listen,(s,0))

def cleanup(signal,frame):
  os.remove("/opt/eveonescratch/._eveOne_mpr_enabled")
  s.disconnect()
  GPIO.cleanup()
  exit(0);

signal.signal(signal.SIGTERM, cleanup)
signal.signal(signal.SIGINT, cleanup)


while True:
  try:
    sensors = {};
    for p in in_pins:
      sensors[p] = (0 if GPIO.input(pin_map[p]) == GPIO.LOW else 1)
    sensors['adc0'] = _eve_adc_read(0,0)
    sensors['adc1'] = _eve_adc_read(1,0)

    if os.path.exists("/opt/eveonescratch/._eveOne_mpr_enabled"):
      channels = read_touch()
      for i in range(12):
        sensors['touch'+str(i)] = channels[i]

    try:
      s.sensorupdate(sensors)
    except scratch.ScratchError:
      pass

    time.sleep(0.1)
  except Exception:
    pass

