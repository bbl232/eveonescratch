# eveonescratch

This is an add on library for the scratch programming language
that makes it easy to integrate with the EveBoardOne (http://eveboardone.com)

# Installation

To install this package simply run

`curl -L https://raw.githubusercontent.com/bbl232/eveonescratch/master/setup.sh | bash`

# Output

The left side of the EveBoard pin out can be used as outputs.
To control output broadcast '&lt;pin&gt; &lt;on|off&gt;' from within scratch.

e.g. To turn on the pin labelled IC2_SDA you would broadcast
`sda on`
Likewise to turn it off you would broadcast
`sda off`

# Input

You can use the right side of the EveBoard pin out as inputs. The values from these pins will show up in the sensor value block in scratch.

You can also use ADC0 and ADC1 in the sensor value block. The values for these inputs come from the analog to digital converter on the board.

# Troubleshooting

If no input values are coming in to Scratch, and no output values are leaving Scratch, you may have to diable and enable remote sensors in scratch (by right clicking the sensor value block).

If you can not get inputs to work, ensure there is a jumper on the component of the board you are trying to use.

Ensure you are using the right pin names and numbers for the jumper cables you have hooked up to the board.
