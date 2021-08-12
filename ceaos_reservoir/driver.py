import time
import string
import zmq
import json
import io
import sys
import fcntl
import copy
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
     socket.connect("tcp://158.130.113.109:23267")	# Replace with your IP Address
     time.sleep(2)
     device_list = get_devices()

     while True:
        for dev in device_list:
             dev.write("R")
        time.sleep(300)
        for dev in device_list:
            if dev.address == 99:
                ph = dev.read()
                ph = float(ph[0:4])
            elif dev.address == 100:
                ec = dev.read()
                ec = float(ec[0:4])
            elif dev.address == 102:
                watertemp = dev.read()
                watertemp = float(watertemp[0:4])
                farenheit = (watertemp * 1.8) + 32

        payload = json.dumps(
             {
                "action": "recv_value",
                "cea-addr": "farm1.env1.bed1.resevoir1",
                "payload": {
                    "ph": ph,
                    "ec": ec,
                    "watertemp": farenheit
                },
             }
        )
        socket.send_string(payload)
        reply = socket.recv()
        reply = json.loads(reply)
        print(reply)

if __name__ == '__main__':
    main()
