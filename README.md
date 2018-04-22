# clueboard_eagle

Eagle device library used by Clueboard

## Upgrade Note

**Please read this if you are already using this library.**

As of commit 1497c7f I have broken Controller.lbr up into multiple files to make
it easier to find the part you need. I will not be updating Controller.lbr anymore,
you should replace your components with the same component from the new file. At
some point in the future I will be removing Controller.lbr.

## [Components.lbr](Components.lbr)

Basic electrical components such as Capacitors, Crystals, Diodes, Resistors, and other (mostly) passive components.

## [Hardware.lbr](Hardware.lbr)

Components for interfacing with the physical world.

## [Headers.lbr](Headers.lbr)

Headers for connecting I/O to various interfaces.

## [ICs.lbr](ICs.lbr)

Integrated circuits and other specialty chips.

## [Controller.lbr](Controller.lbr)

**DEPRECATED**: Please use the equivalent footprints in other files.

## [Keyboard.lbr](Keyboard.lbr)

Switch footprints that support various Cherry MX and/or Alps switches.

### Switch Devices

When putting together your schematic there are 5 basic types of switches to choose
from:

* KEYSWITCH-DIODE: Cherry MX and/or Alps switches with in-switch diode support.
* KEYSWITCH-LED: Cherry MX and/or Alps switches with throughhole single-color LED support
* KEYSWITCH-LEDHOLE: Cherry MX and/or Alps switches with a slot to allow LED's to shine through or for 4 wire LEDs to poke through to a daughter board.
* KEYSWITCH-LEDTHTHOLE: Cherry MX and/or Alps switches with in-switch LED support and shine-through LED support.
* KEYSWITCH-PLAIN: Cherry MX and/or Alps switches
* KEYSWITCH-RGBLED: Cherry MX switches with throughhole RGB LED support
* KEYSWITCH-RGBSMDLED: Cherry MX and/or Alps switches with SMD RGB LED support
* KEYSWITCH-SMDLED: Cherry MX and/or Alps switches with SMD single-color LED support
* KEYSWITCH-SMDTHTLED: Cherry MX and/or Alps switches with both throughhole and SMD single-color LED support

Each one may have one or more switch footprints available:

* ALPS: Alps switch
* ALPSMX: Combined footprint that supports both ALPS and MX
* CHOC: Kailh (Kaihua) Choc low-profile switches
* CHOCX: Combined footprint that supports both CHOC and X
* MX: Cherry MX Switches, both Plate and PCB mount
* MXHS: Footprint that supports the Kailh PCB Sockets for switch hot swapping, plate mount switches only
* MXHSPCB: Footprint that supports the Kailh PCB Sockets for switch hot swapping, pcb or plate mount switches
* X: Kailh (Kaihua) X low-profile switches

## [LCD.lbr](LCD.lbr)

Various LCD based displays.

## [LED.lbr](LED.lbr)

LED lighting controllers and emitters.

## [MCU.lbr](MCU.lbr)

Processors that can be used to scan a keyboard matrix.

## [USB.lbr](USB.lbr)

USB connectors and devices which interface directly with the USB signal wires.

# License

These files are released under a [Creative Commons Attribution-NonCommercial](LICENSE.md) license. You are free to include and distribute them in your project, but if you are selling a board please contact me for a more permissive license. Gratis (no-cost) licenses are available to community run group buys.
