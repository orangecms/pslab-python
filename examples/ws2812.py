from PSL import sciencelab
from time import sleep

pslab = sciencelab.connect(port = "/dev/ttyUSB0")

r = [255,0,0] # red
g = [0,255,0] # green
b = [0,0,255] # blue

y = [255,255,0] # yellow
m = [255,0,255] # magenta
c = [0,255,255] # cyan

w = [200,200,200] # white

lights = [r, g, b, y, m, c, w, r,
          g, b, y, m, c, w, r, g,
         ]
#          b, y, m, c, w, r, g, b,
#          y, m, c, w, r, g]

while True:
    pslab.WS2812B(lights,'SQR1')
    lights = lights[1:] + lights [:1]
    sleep(0.5)
