# eveonescratch

This is an add on library for the scratch programming language
that makes it easy to integrate with the EveBoardOne (http://eveboardone.com)

# Installation

To install this package simply run

`curl -L https://raw.githubusercontent.com/bbl232/eveonescratch/master/setup.sh | bash`

**Note**: You must enable SPI in the advanced options in...

`sudo raspi-config`

# Output

The left side of the EveBoard pin out can be used as outputs.
To control output broadcast '&lt;pin&gt; &lt;on|off&gt;' from within scratch.

e.g. To turn on the pin labelled IC2_SDA you would broadcast
`sda on`
Likewise to turn it off you would broadcast
`sda off`

## Pulse Width Modulation (PWM)

To enable PWM on a pin, broadcast
`pwm 04 50`
This broadcast would enable PWM on pin 04 with a duty cycle of 50%.

# Input

You can use the right side of the EveBoard pin out as inputs. The values from these pins will show up in the sensor value block in scratch.

You can also use ADC0 and ADC1 in the sensor value block. The values for these inputs come from the analog to digital converter on the board.

## MPR121

You can make use of an MPR121 12 channel capacitive touch sensor hooked up to the IC2 (I2C) bus.
To enable the touch sensor, simply broadcast
`mpr121 on`

# Troubleshooting

If no input values are coming in to Scratch, and no output values are leaving Scratch, you may have to diable and enable remote sensors in scratch (by right clicking the sensor value block).

If you can not get inputs to work, ensure there is a jumper on the component of the board you are trying to use.

Ensure you are using the right pin names and numbers for the jumper cables you have hooked up to the board.

You may have to reboot your Pi if all else fails.
