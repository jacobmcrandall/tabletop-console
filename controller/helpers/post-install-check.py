#https://learn.adafruit.com/circuitpython-libraries-on-any-computer-with-mcp2221/post-install-checks
import hid
import os
hid.enumerate()
device = hid.device()
device.open(0x04D8, 0x00DD)
os.environ["BLINKA_MCP2221"]