# https://www.st.com/resource/en/datasheet/vl53l0x.pdf
# https://www.st.com/resource/en/datasheet/vl53l1x.pdf

from __future__ import print_function
import time


def connect(route, **args):
    '''
    route can either be I.I2C , or a radioLink instance
    '''
    return SHT21(route, **args)


def rawToTemp(vals):
    if vals:
        if len(vals):
            v = (vals[0] << 8) | (vals[1] & 0xFC)  # make integer & remove status bits
            v *= 175.72
            v /= (1 << 16)
            v -= 46.85
            return [v]
    return False


def rawToRH(vals):
    if vals:
        if len(vals):
            v = (vals[0] << 8) | (vals[1] & 0xFC)  # make integer & remove status bits
            v *= 125.
            v /= (1 << 16)
            v -= 6
            return [v]
    return False


class SHT21():
    RESET = 0xFE
    WRITE_ADDRESS = 0x52
    READ_ADDRESS = 0x53
    # registers
    MODEL_ID = 0xEA
    MODULE_TYPE = 0xCC
    MASK_REV = 0x10
    NUMPLOTS = 1
    PLOTNAMES = ['Data']
    ADDRESS = 0x29
    name = 'Time-of-Flight'

    def __init__(self, I2C, **args):
        self.I2C = I2C
        self.ADDRESS = args.get('address', self.ADDRESS)
        self.name = 'Time-of-Flight'
        '''
        try:
            print ('switching baud to 400k')
            self.I2C.configI2C(400e3)
        except:
            print ('FAILED TO CHANGE BAUD RATE')
        '''
        self.init()

    def init(self):
        self.I2C.writeBulk(self.ADDRESS, [self.RESET])  # soft reset
        time.sleep(0.1)

    @staticmethod
    def _calculate_checksum(data, number_of_bytes):
        """5.7 CRC Checksum using the polynomial given in the datasheet
        Credits: https://github.com/jaques/sht21_python/blob/master/sht21.py
        """
        # CRC
        POLYNOMIAL = 0x131  # //P(x)=x^8+x^5+x^4+1 = 100110001
        crc = 0
        # calculates 8-Bit checksum with given polynomial
        for byteCtr in range(number_of_bytes):
            crc ^= (data[byteCtr])
            for _ in range(8, 0, -1):
                if crc & 0x80:
                    crc = (crc << 1) ^ POLYNOMIAL
                else:
                    crc = (crc << 1)
        return crc

    def getRaw(self):
        self.I2C.writeBulk(self.ADDRESS, [self.selected])
        if self.selected == self.TEMP_ADDRESS:
            time.sleep(0.1)
        elif self.selected == self.HUMIDITY_ADDRESS:
            time.sleep(0.05)

        vals = self.I2C.simpleRead(self.ADDRESS, 3)
        if vals:
            if self._calculate_checksum(vals, 2) != vals[2]:
                print(vals)
                return False
        if self.selected == self.TEMP_ADDRESS:
            return rawToTemp(vals)
        elif self.selected == self.HUMIDITY_ADDRESS:
            return rawToRH(vals)
