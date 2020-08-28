import PSL
from PSL.packet_handler import Handler
from PSL.Peripherals import I2C
from PSL.SENSORS.SHT21 import SHT21

conn = Handler()
i2c = PSL.Peripherals.I2C(conn)

data = i2c.scan()
print(data)

sensor = SHT21(i2c)
sensor.selectParameter('humidity')
humi = sensor.getRaw()
sensor.selectParameter('temperature')
temp = sensor.getRaw()
print("humidity:    ", humi)
print("temperature: ", temp)
