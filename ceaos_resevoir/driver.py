import io
import sys
import fcntl
import time
import copy
import string
from .AtlasI2C import (
	 AtlasI2C
    )
def get_devices():
    device = AtlasI2C()
    device_address_list = device.list_i2c_devices()
    device_list = []

    for i in device_address_list:
        device.set_i2c_address(i)
        response = device.query("I")
        moduletype = response.split(",")[1]
        response = device.query("name,?").split(",")[1]
        device_list.append(AtlasI2C(address = i, moduletype = moduletype, name = response))
    return device_list

def main():

    device_list = get_devices()

    device = device_list[0]

    while True:
        for dev in device_list:
             dev.write("R")
        time.sleep(5.0)
        for dev in device_list:
            print(dev.read())

if __name__ == '__main__':
    main()