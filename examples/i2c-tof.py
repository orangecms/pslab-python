import PSL
from PSL.packet_handler import Handler
from PSL.Peripherals import I2C
from PSL.SENSORS.VL531X import VL531X
from time import sleep

conn = Handler()
i2c = PSL.Peripherals.I2C(conn, 0x29)

data = i2c.scan()
print(data)

sensor = VL531X(i2c)

while True:
    res = sensor.getRaw()
    print("distance: ", res)

    sleep(0.05)
