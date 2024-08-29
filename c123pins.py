from microbit import *
import time
import music

class Devices:
    """
    Broches numériques/analogiques :
    P0, P1, P2, P8, P12, P13, P14, P15, P16

    devices = Devices()
    device = devices.getDevice(1) 0 à 2 puis 8 puis 12 à 16
    ou
    device = devices.getDevice(1, threshold=900) seuil d'alerte de 1 à 1023

    pour les broches analogiques
    device.setValue(1023) valeur de 0 à 10213

    device.getValue()
    devive.isDetected() détection True ou False
                en fonction de la valeur du seuil d'alerte

    pour les borches numériques
    device.on()
    device.off()
    device.alternate()

    Utiliser les broches 8 puis 12 à 16
    touchSensor = devices.getTouchSensor(0)
    if touchSensor.isPressed():
    logPress = touchSensor.waitReleased() # Temps d'appui en millisecondes
    touchSensor.waitPressed()

    led = getLed(0)
    led.on()
    led.off()
    led.alternate()

    Utiliser les broches 0 à 2
    lightSensor = devices.getLightSensor(0, 500)
    light = lightSensor.getValue()
    lightSensor.isDetected()

    IRPhotoreflector = devices.getIRPhotoreflector(0)
    IRPhotoreflector.learnTrackingLine()

    soundSensor = devices.getSoundSensor(0, 50)
    sound = soundSensor.getValue()
    soundSensor.isDetected()

    """

    PINS = [
        pin0,
        pin1,
        pin2,
        pin3,
        pin4,
        pin5,
        pin6,
        pin7,
        pin8,
        pin9,
        pin10,
        pin11,
        pin12,
        pin13,
        pin14,
        pin15,
        pin16,
    ]

    def __init__(self):
        pass

    class _Pin:
        def __init__(self, pin=0, threshold=900):
            self.pin = None
            if 2 < pin < 8:
                raise ValueError("pin : ", pin, " no supported ")
            elif 8 < pin < 12:
                raise ValueError("pin : ", pin, " no supported ")
            elif 0 < pin >= len(Devices.PINS):
                raise ValueError("pin : ", pin, " no supported ")
            else:
                self.pin = Devices.PINS[pin]
                self.threshold = threshold
                self.timeout = 20

                self.status = False

        def getValue(self) -> int:
            return self.pin.read_analog()

        def setValue(self, value, period=1000):
            value = value if value > 0 else 0
            value = value if value <= 1023 else 1023
            self.pin.write_analog(value)
            self.pin.set_analog_period(period)

        def isDetected(self) -> bool:
            return True if self.pin.read_analog() > self.threshold else False

        def on(self):
            self.status = True
            self.pin.write_digital(1)

        def off(self):
            self.status = False
            self.pin.write_digital(0)

        def alternate(self):
            if self.status:
                self.off()
            else:
                self.on()

    def getDevice(self, pin=0, threshold=900):
        return self._Pin(pin, threshold)

    # Gestion d'un bouton poussoir
    class _TouchSensor(_Pin):
        def __init__(self, pin=0, threshold=900):
            super().__init__(pin, threshold)

        def isPressed(self) -> bool:
            return False if self.pin.read_digital() == 0 else True

        def waitReleased(self) -> int:

            start = time.ticks_ms()
            while self.isPressed():
                time.sleep_ms(20)
            return time.ticks_ms() - start

        def waitPressed(self):
            while not self.isPressed():
                time.sleep_ms(20)

    def getTouchSensor(self, pin=0, threshold=900):
        return self._TouchSensor(pin, threshold)

    # Gestion d'une LED
    def getLed(self, pin=0):
        return self._Analog_Pin(pin)

    # Gestion d'un capteur de lumière
    class _LightSensor(_Pin):
        def __init__(self, pin=0, threshold=900):
            super().__init__(pin, threshold)

    def getLightSensor(self, pin=0, threshold=900):
        if pin > 2:
            raise ValueError("pin analog : ", pin, " no supported ")
            return None
        else:
            return self._LightSensor(pin, threshold)

    # Gestion d'un photoréflecteur
    class _IRPhotoreflector(_Pin):
        def __init__(self, pin=0, threshold=900):
            super().__init__(pin, threshold)

        def learnTrackingLine(self, led=None) -> bool:
            start = time.ticks_ms()
            max = 0
            min = 1000
            while (((min >= max) or ((max - min) < 200)) and
                   ((time.ticks_ms() - start) < self.timeout)):
                value = self.getValue()
                max = value if value > max else max
                min = value if value < min else min
                time.sleep(0.1)
                if led:
                    led.Alternate()
            if (((min >= max) or ((max - min) < 200))):
                return False
            else:
                self.threshold = min + int((max - min)/2)
                return True

    def getIRPhotoreflector(self, pin=0, threshold=200):
        if pin > 2:
            raise ValueError("pin analog : ", pin, " no supported ")
            return None
        else:
            return self._IRPhotoreflector(pin, threshold)

    # Gestion d'un microphone
    class _SoundSensor(_Pin):
        def __init__(self, pin=0, threshold=100):
            super().__init__(pin, threshold)
        """
        def isDetected(self) -> int:
            return True if self.pin.read_analog() > self.threshold else False
        """
    def getSoundSensor(self, pin=0, threshold=100):
        if pin > 2:
            raise ValueError("pin analog : ", pin, " no supported ")
            return None
        else:
            return self._SoundSensor(pin, threshold)

