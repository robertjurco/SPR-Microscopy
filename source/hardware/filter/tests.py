from pyThorlabsPM100x.driver import ThorlabsPM100x
import pyvisa as visa
rm = visa.ResourceManager()
list_all_devices = rm.list_resources()
print(list_all_devices)