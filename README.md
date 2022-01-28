# mvc-cab
Tools and Scripts for interracting with the Arcade 1UP Cabinets to supplement the following blog posts:
1. https://voidstarsec.com/blog//2022/01/27/uart-uboot-and-usb
# Contents
- ```mvc-cab.py```
  - This script can be used to extract the firmware via UBoot using the depthcharge library
# Dependencies
- [depthcharge](https://depthcharge.readthedocs.io/en/latest/)
- Serial adapter of some sort (the blog post uses a Raspberry Pi but an FTDI will also work)
# Wiring
Connect the cabinet to your raspberry pi as follows:
![Wiring Diagram](https://voidstarsec.com/blog/assets/images/pi-cab_bb.png)
