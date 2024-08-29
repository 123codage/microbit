from microbit import accelerometer, display, pin_logo, button_a, button_b , Image
import time
import math
import music

class Images(Image):

    ZERO = '09990:09090:09090:09090:09990'
    ONE = '00900:09900:00900:00900:09990'
    TWO = '00900:09090:00900:09000:09990'
    THREE = '09990:00090:09990:00090:09990'
    FOUR = '00090:00900:09090:09990:00090'
    FIVE = '09990:09000:09990:00090:09990'
    SIX = '00990:00090:09990:09090:09990'
    SEVEN = '09990:00090:00090:00900:09000'
    EIGHT = '09990:09090:09990:09090:09990'
    NINE = '09990:09090:09990:00090:09990'

    """
    Image.HEART
    Image.HEART_SMALL
    Image.HAPPY
    Image.SMILE
    Image.SAD
    Image.CONFUSED
    Image.ANGRY
    Image.ASLEEP
    Image.SURPRISED
    Image.SILLY
    Image.FABULOUS
    Image.MEH
    Image.YES
    Image.NO
    Image.CLOCK12
    Image.CLOCK1
    Image.CLOCK2
    Image.CLOCK3
    Image.CLOCK4
    Image.CLOCK5
    Image.CLOCK6
    Image.CLOCK7
    Image.CLOCK8
    Image.CLOCK9
    Image.CLOCK10
    Image.CLOCK11
    Image.ARROW_N
    Image.ARROW_NE
    Image.ARROW_E
    Image.ARROW_SE
    Image.ARROW_S
    Image.ARROW_SW
    Image.ARROW_W
    Image.ARROW_NW
    Image.TRIANGLE
    Image.TRIANGLE_LEFT
    Image.CHESSBOARD
    Image.DIAMOND
    Image.DIAMOND_SMALL
    Image.SQUARE
    Image.SQUARE_SMALL
    Image.RABBIT
    Image.COW
    Image.MUSIC_CROTCHET
    Image.MUSIC_QUAVER
    Image.MUSIC_QUAVERS
    Image.PITCHFORK
    Image.XMAS
    Image.PACMAN
    Image.TARGET
    Image.TSHIRT
    Image.ROLLERSKATE
    Image.DUCK
    Image.HOUSE
    Image.TORTOISE
    Image.BUTTERFLY
    Image.STICKFIGURE
    Image.GHOST
    Image.SWORD
    Image.GIRAFFE
    Image.SKULL
    Image.UMBRELLA
    Image.SNAKE
    """

class Screen():
    lastScreen = None
    start = time.ticks_ms()
    speed = 100
    delay = 1000

    def __init__(self):
        pass

    """"
    # Affichage des 25 LEDs de la carte micro:bit
    # Affichage de l'objet Image de la bibliothèque microbit
    # Affichage d'une chaîne de caratères représentant les LEDs
    # Animation d'un tableau de plusieurs affichages

      exemples

            screen1 = Screen()
            screen1.show(Images.HAPPY, delay=1000)


            screen2 = Screen()
            screen2.show(Images.ONE, speed=100, delay=1000)

            screen3 = Screen()
            clock = [Images.CLOCK12,
                     Images.CLOCK1,
                     Images.CLOCK2,
                     Images.CLOCK3,
                     Images.CLOCK4,
                     Images.CLOCK5,
                     Images.CLOCK6,
                     Images.CLOCK7,
                     Images.CLOCK8,
                     Images.CLOCK9,
                     Images.CLOCK10,
                     Images.CLOCK11]
            screen3.show(clock, delay=1000)

            while True:
                screen3.draw()

    """
    def show(self, images, speed=0, delay=1000, draw=True):
        # Controle des paramètres
        if images is None:
            raise ValueError("image  is none")

        self.delay = delay

        if isinstance(images, list) and self.delay == 0:
            self.delay = 1000

        # Initialisation des données
        # Délai entre deux affichage d'un écran
        self.start = time.ticks_ms() - self.delay - 1
        # Délai d'affichage entre chaque pixel
        self.startpixel = time.ticks_ms()
        # Index du tableau d'affichage des écrans
        self.ImageIndex = -1
        self.images = images
        self.speed = speed

        self.col = 0
        self.row = 0

        if draw :
            self.draw()

    def draw(self):

        if self.images and self.delay > 0 :

            image = None
            # Si délai entre chaque affichage d'écran est dépassé ?
            if (time.ticks_ms()-self.start) > self.delay:
                # Si tableau pour afficher plusieurs images
                if isinstance(self.images, list):
                    # Début d'un cycle d'images
                    if self.col == 0 and self.row == 0 :
                        self.ImageIndex += 1
                        self.startpixel = time.ticks_ms() - self.speed - 1
                        # Fin du cycle d'images
                        if self.ImageIndex >= len(self.images):
                            self.ImageIndex = 0
                            return False

                    image = self.images[self.ImageIndex]
                else:
                    # si un seul écran
                    image = self.images

                # Si objet Image de la bibliotèque microbit
                if isinstance(image, Image):
                    display.show(image)
                    self.start = time.ticks_ms()
                else:
                    # Affichage de la chaine de caractère de type Image
                    # Si pas d'animation
                    if self.speed == 0 :
                        display.show(Image(image))
                        self.start = time.ticks_ms()
                    # Si animation d'affichage entre chaque pixel
                    else:
                        if (time.ticks_ms()-self.startpixel) > self.speed :
                            if self.col == 0 and self.row == 0 :
                                display.clear()
                            display.set_pixel(self.col,
                                              self.row,
                                              int(image[(self.row*5)+self.row + self.col]))
                            if int(image[(self.row*5)+self.row + self.col]) > 0 :
                                self.startpixel = time.ticks_ms()
                            # colonne suivante
                            self.col += 1
                            if self.col > 4 :
                                # ligne suivante
                                self.col = 0
                                self.row += 1
                                if self.row > 4 :
                                    # fin de l'écran
                                    self.col = 0
                                    self.row = 0
                                    self.start = time.ticks_ms()

        return True

    def getImageIndex(self):
        if isinstance(self.images, list):
            return self.ImageIndex
        else:
            return 0


"""
Gestion des boutons A et B et de la zone sensitive
Détection de l'appui du bouton A Bouton B et zone sensitive
Attente si appui long sur un des trois dispositifs
    # création de l'objet pour gérer les boutons
    # appui des boutons sonorisé ou pas
    buttons = Buttons(True)
    # Attente de l'appui sur le bouton A ou B ou sur la zone sensible
    buttons.waitPressed()
    # Attente des boutons relachés
    buttons.waitReleased(longPressDelay=0)

    while True:
        # Text si un appui sur A ou B ou zone sensible
        boutonA, boutonB, sensitif = buttons.isPressed()
        if boutonA :
            ...
        if boutonB :
            ...
            # attente des boutons relachés et de la zone sensible
            # temps en millisecondes du temps appuyé
            longPress = buttons.waitReleased()
        if sensitif :
            ...



"""
class Buttons:

    def __init__(self, sounded=False):
        self.sounded = sounded

    def isPressed(self) -> (bool, bool, bool):
        return (True if button_a.is_pressed() else False,
                True if button_b.is_pressed() else False,
                True if pin_logo.is_touched() else False)

    def waitReleased(self, longPressDelay=500) -> int:
        startDelay = time.ticks_ms()
        if button_a.is_pressed() or button_b.is_pressed() or pin_logo.is_touched():
            if self.sounded:
                music.pitch(400, 1)
            while (button_a.is_pressed() or
                   button_b.is_pressed() or
                   pin_logo.is_touched()):
                if self.sounded:
                    if ((longPressDelay > 0) and
                       ((time.ticks_ms()-startDelay) > longPressDelay)):
                        music.pitch(800, 1)

        return time.ticks_ms()-startDelay

    def waitPressed(self) -> (bool, bool, bool):
        while (not button_a.is_pressed() and
               not button_b.is_pressed() and
               not pin_logo.is_touched()):
            pass
        return (True if button_a.is_pressed() else False,
                True if button_b.is_pressed() else False,
                True if pin_logo.is_touched() else False)

"""
Déclenchement du buzzer sur une fréquence et un temps
on déclenchement du buzzer fréquence et temps
"""
class Buzzer():
    frequency = 800

    def __init__(self, frequency=800):
        self.frequency = frequency

    def on(self, frequency=800, delay=1):
        music.pitch(frequency, delay)
"""
Détection de la lumière du jour sur un seuil
-seuil de détection
-délai de détection
"""
class LihgtSensor():
    start = time.ticks_ms()
    threshold = 100
    delay = 1000

    def __init__(self, threshold=100, delay=1000):
        self.threshold = threshold
        self.delay = delay

    def init(self, threshold=100, delay=1000):
        self.threshold = threshold
        self.delay = delay
        self.start = time.ticks_ms()

    def isLight(self, delay=0):
        if delay == 0:
            delay = self.delay
        if display.read_light_level() < self.threshold:
            self.start = time.ticks_ms()
        if (time.ticks_ms() - self.start > (delay)):
            self.start = time.ticks_ms()
            return True
        else:
            return False

    def getValue(self):
        return display.read_light_level()

"""
Détection d'un mouvement par l'accéléromètre
"""
class Accelerometer():
    def __init__(self, power=5, delay=50):
        self.p, self.t = self.getSway()
        self.r = self.getPitch()

        self.start = time.ticks_ms()
        self.delay = delay
        self.power = power

    def getSway(self):
        p = self.getPitch()
        t = self.getRool()
        return (p, t)

    def getPitch(self):
        p = int(math.atan2(accelerometer.get_y(),
                           -accelerometer.get_z()) * 180.0/math.pi)
        return p

    def getRool(self):
        t = int(math.atan2(accelerometer.get_x(),
                           math.sqrt(accelerometer.get_y()**2 +
                           accelerometer.get_z()**2)) * 180.0/math.pi)
        return t

    def isShake(self):

        if (time.ticks_ms() - self.start) > self.delay:
            p, t = self.getSway()

            self.start = time.ticks_ms()
            if abs(self.p - p) > 5 or abs(self.t - t) > self.power :
                self.p = p
                self.t = t
                return True

        return False

    def isPitch(self):

        if (time.ticks_ms() - self.start) > self.delay:
            p = self.getPitch()
            self.start = time.ticks_ms()
            if abs(self.p - p) > self.power :
                self.p = p
                return True

        return False

    def isRoll(self):

        if (time.ticks_ms() - self.start) > self.delay:
            r = self.getPitch()

            self.start = time.ticks_ms()
            if abs(self.r - r) > self.power :
                self.r = r
                return True

        return False
