import time
import string
import zmq
import json
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
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:23267")
    device_list = get_devices()

    while True:
        for dev in device_list:
             dev.write("R")
        for dev in device_list:
            if dev.address == 99:
                ph = dev.read()
            elif dev.address == 100:
                ec = dev.read()
            elif dev.address == 102:
                watertemp = dev.read()
                farenheit = (watertemp * 1.8) + 32

        payload = {
                "action": "recv_value",
                "cea-addr": "farm1.env1.bed1.resevoir",
                "payload": {
                    "ph": ph,
                    "ec": ec,
                    "watertemp": farenheit
                }
            }
        socket.send_json(payload)
        time.sleep(3.0) 

if __name__ == '__main__':
    main()
