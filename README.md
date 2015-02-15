# eveonescratch

This is an add on library for the scratch programming language
that makes it easy to integrate with the EveBoardOne (http://eveboardone.com)

# Installation

To install this package simply run

`curl -L https://raw.githubusercontent.com/bbl232/eveonescratch/master/setup.sh | bash`

# Use

The left side of the EveBoard pin out can be used as outputs.
To control output broadcast '<pin> <on|off>' from within scratch.

e.g. To turn on the pin labelled IC2_SDA you would broadcast
`sda on`
Likewise to turn it off you would broadcast
`sda off`