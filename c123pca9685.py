from microbit import sleep, i2c
import math, ustruct
import time

"""
https://www.dfrobot.com/product-1738.html
https://wiki.dfrobot.com/Micro_bit_Driver_Expansion_Board_SKU_DFR0548

Documentation composant PCA9685 : https://cdn-shop.adafruit.com/datasheets/PCA9685.pdf
Dépôt sources github : https://github.com/DFRobot/pxt-motor

"""

# Registers/etc:
PCA9685_ADDRESS    = 0x40 # 64
MODE1              = 0x00
MODE2              = 0x01
SUBADR1            = 0x02
SUBADR2            = 0x03
SUBADR3            = 0x04
PRESCALE           = 0xFE
LED0_ON_L          = 0x06
LED0_ON_H          = 0x07
LED0_OFF_L         = 0x08
LED0_OFF_H         = 0x09
ALL_LED_ON_L       = 0xFA
ALL_LED_ON_H       = 0xFB
ALL_LED_OFF_L      = 0xFC
ALL_LED_OFF_H      = 0xFD

# Bits:
RESTART            = 0x80
SLEEP              = 0x10
ALLCALL            = 0x01
INVRT              = 0x10
OUTDRV             = 0x04
RESET              = 0x00

# Enum for DC Motors
class Motors:
    M1 = 0x01
    M2 = 0x02
    M3 = 0x03
    M4 = 0x04

# Enum for Motor Direction
class Dir:
    cw = 1
    ccw = -1

class Servos:
    S1 = 0x08
    S2 = 0x07
    S3 = 0x06
    S4 = 0x05
    S5 = 0x04
    S6 = 0x03
    S7 = 0x02
    S8 = 0x01

class PCA9685(object):
    """PCA9685 PWM LED/servo controller."""

    def __init__(self, address=PCA9685_ADDRESS, freq_hz = 50):
        """Initialize the PCA9685."""
        self._search_PCA9686()
        self.address = address
        i2c.write(self.address, bytearray([MODE1, RESET])) # reset not sure if needed but other libraries do it
        self._set_pwm_freq(freq_hz)

    def _search_PCA9686(self):
        address_i2c = i2c.scan()
        for address in address_i2c:
            if address==PCA9685_ADDRESS:
                return True
        raise ValueError("I2C scan : ", PCA9685_ADDRESS, " no supported ")
        return False

    def _set_pwm_freq(self, freq_hz):
        """Set the PWM frequency to the provided value in hertz."""
        prescaleval = 25000000.0    # 25MHz
        prescaleval /= 4096.0       # 12-bit
        prescaleval /= float(freq_hz)
        prescaleval -= 1.0
        # print('Setting PWM frequency to {0} Hz'.format(freq_hz))
        # print('Estimated pre-scale: {0}'.format(prescaleval))
        prescale = int(math.floor(prescaleval + 0.5))
        # print('Final pre-scale: {0}'.format(prescale))
        i2c.write(self.address, bytearray([MODE1])) # write register we want to read from first
        oldmode = i2c.read(self.address, 1)
        if len(oldmode) == 1:
            oldmode = ustruct.unpack('<H', oldmode + b'\x00')[0]  # Ajouter un octet nul pour compléter les 2 octets
        else:
            oldmode = ustruct.unpack('<H', oldmode)[0]
        newmode = (oldmode & 0x7F) | 0x10    # sleep
        i2c.write(self.address, bytearray([MODE1, newmode]))  # go to sleep
        i2c.write(self.address, bytearray([PRESCALE, prescale]))
        i2c.write(self.address, bytearray([MODE1, oldmode]))
        time.sleep_ms(5)
        # i2c.write(self.address, bytearray([MODE1, oldmode | 0x80]))
        i2c.write(self.address, bytearray([MODE1, oldmode | 0xa1]))

    def _set_pwm(self, channel, on, off):
        """Sets a single PWM channel."""
        if channel < 0 or channel > 15:
            return

        buf = bytearray(5)
        buf[0] = LED0_ON_L + 4 * channel
        buf[1] = on & 0xff
        buf[2] = (on >> 8) & 0xff
        buf[3] = off & 0xff
        buf[4] = (off >> 8) & 0xff
        i2c.write(PCA9685_ADDRESS, buf)

    def motorRun(self, index, direction, speed):
        speed = speed * 16 * direction
        if speed >= 4096:
            speed = 4095
        elif speed <= -4096:
            speed = -4095

        if index > 4 or index <= 0:
            return

        pn = (4 - index) * 2
        pp = (4 - index) * 2 + 1
        if speed >= 0:
            self._set_pwm(pp, 0, speed)
            self._set_pwm(pn, 0, 0)
        else:
            self._set_pwm(pp, 0, 0)
            self._set_pwm(pn, 0, -speed)

    def motorStop(self, index):
        self._set_pwm((4 - index) * 2, 0, 0)
        self._set_pwm((4 - index) * 2 + 1, 0, 0)

    def motorStopAll(self):
        for idx in range(1, 5, 1):
            self.motorStop(idx)

    def servo(self, index, degree):
        v_us = (degree * 1800 / 180 + 600)
        value = v_us * 4096 / 20000
        self._set_pwm(index + 7, 0, int(value))

i2c.init()

pca9685 = PCA9685()

"""
pca9685.servo(Servos.S8, 20)

pca9685.motorRun(Motors.M1, Dir.cw, 255)

time.sleep(2)
pca9685.motorStopAll()
pca9685.servo(Servos.S8, 160)
pca9685.motorRun(Motors.M2, Dir.cw, 255)
time.sleep(2)
pca9685.motorStopAll()
pca9685.servo(Servos.S8, 90)
pca9685.motorRun(Motors.M3, Dir.cw, 255)
time.sleep(2)
pca9685.motorStopAll()
pca9685.motorRun(Motors.M4, Dir.cw, 255)
time.sleep(2)
pca9685.motorStopAll()
"""
