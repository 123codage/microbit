# Bibliothèque c123common
from c123common import Images, Screen, Buttons

Création d’un objet Screen

Screen()

# Création d’un affichage

show(images, speed=0, delay=1000, draw=True)

images : soit une image ou un tableau d’images

•	'09990:09090:09090:09090:09990'

•	Images.GHOST

•	[Images.GHOST, Images.SWORD, Images.SNAKE …]

speed : temps d’affichage entre deux LEDs en millisecondes

delay : temps de l’affichage d’un écran de 25 LEDs

draw : affichage de l’écran dans la fonction show 

# Affichage et animation de la dernière définition de show

draw() -> bool

retourne : True ou False (True si encore dans un cycle d’affichage False en fin d’un cycle d’affichage)

# Index de l’affichage du tableau en cours d’animation

getImageIndex() -> int

retourne l’index en cours du tableau d’animation
 
# Création d’objet pour la gestion des deux boutons et de la zone sensible

Buttons(sounded=False)

sounded = sonorisation ou pas lors de l’appui des boutons et de la zone sensible

# Détection de l’appui sur un des boutons A ou B ou de la zone sensible

isPressed() -> (bool, bool, bool)

retourne : trois valeurs sur un état (True ou False) du bouton A, puis celui du bouton B et enfin celui de la zone sensible.

# Attente du relâchement du bouton ou zone sensible

waitReleased(self, longPressDelay=500) -> int

longPressDelay : temps en millisecondes avant un avertissement sonore d’un appui long

retourne le temps en millisecondes de l’appui sur le bouton

# Attente avant l’appui sur un des boutons A ou B ou l’appui sur la zone sensible

waitPressed(self) -> (bool, bool, bool)

retourne : trois valeurs sur un état (True ou False) du bouton A, puis celui du bouton B et enfin celui de la zone sensible.

# Bibliothèque c123pins

from c123pins import Devices

Devices()

# Gestion des broches

getDevice(pin=0, threshold=900)

	pin : numéro de la broche 0, 1,2 , 8, 12, 13, 14, 15, 16
 
	threshold : seuil de détection des valeurs retournées 

# Broche analogique

Les entrées analogiques sont reliées à un convertisseur analogique numérique (CAN) interne au microcontrôleur. Il s’agit d’un convertisseur 10 bits, c’est-à-dire qu’il retournera une valeur entière comprise entre 0, lorsque la tension en entrée est nulle, et 1024 lorsqu’elle est à 3,3 V.

getValue() -> int:

La méthode « getValue() » permet de lire la tension sur la broche spécifiée par le paramètre « pin » et retourne un entier compris entre à (0 V) et 1023 (3,3 V). 

setValue(value, period=1000)

La méthode » setValue()» permet de générer sur la broche spécifiée par le paramètre « pin », un signal PWM avec un rapport cyclique proportionnel à la valeur du paramètre « value ». Cette valeur doit être comprise entre 0 (0 %) et 1023 (100 %). 

isDetected() -> bool

# Broche numérique

on()

La méthode « on » place la broche spécifiée par le paramètre « pin » au niveau haut. 

off()

La méthode « off » place la broche spécifiée par le paramètre « pin » au niveau bas. 

alternate()

getTouchSensor(pin=0, threshold=900)

	isPressed() -> bool

	waitReleased() -> int

	waitPressed()

getLed(pin=0)

	on()

	off()

	alternate()

	setValue(value, period=1000)

getLightSensor(pin=0, threshold=900)

	getValue() -> int:
 
	setValue(value, period=1000)
 
	isDetected() -> bool

getIRPhotoreflector(pin=0, threshold=200)

	learnTrackingLine(led=None) -> bool:
 
	getValue() -> int:
 
	setValue(value, period=1000)
 
	isDetected() -> bool

getSoundSensor(self, pin=0, threshold=100)

	getValue() -> int:
 
	setValue(value, period=1000)
 
	isDetected() -> bool


# Exemple d'une programmation :

	from c123common import Images, Screen, Buttons	
	from c123pins import Devices	
	import time
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
	
	start123 = [Images.THREE,	
	            Images.TWO,		    
	            Images.ONE]
	"""
	Création gestionnaire
	bouton A et bouton B
	plus zone sensible
	"""	
	buttons = Buttons(True)	
	"""
	Gestionnaire des écrans d'actions
	et des animations
	"""	
	actions = Screen()	
	animations = Screen()	
	# Attente validation	
	actions.show(Images.YES)	
	buttons.waitPressed()	
	devices = Devices()	
	lightSensor = devices.getLightSensor(2, 200)	
	soundSensor = devices.getSoundSensor(1, 150)	
	led = devices.getDevice(8)	
	touchSensor = devices.getTouchSensor(16)	
	# Affichage de l'animation du démarrage 3,2,1	
	animations.show(start123, 100, 500)	
	while animations.draw():	
	    pass	
	# Affichage animation attente	
	animations.show(clock, 100, 1000)	
	while True:	
	    animations.draw()	    
	    # Test des boutons et zone sensible	    
	    buttonA, buttonB, sensitif = buttons.isPressed()	
     
	    if buttonA:	    
	        led.on()		
	        actions.show(Images.ARROW_W)		
	        buttons.waitReleased()	
	 
	    if buttonB:	    
	        led.off()		
	        actions.show(Images.ARROW_E)		
	        buttons.waitReleased()
	
	    if sensitif :	    
	        for intensite in range(0, 1024, 16):		
	            led.setValue(intensite)		    
	            time.sleep_ms(50)
	
	        for intensite in range(1024, 0, -16):		
	            led.setValue(intensite)		    
	            time.sleep_ms(50)
	
	    if touchSensor.isPressed():	
	        led.alternate()		
	        print(lightSensor.getValue())		
	        touchSensor.waitReleased()
	
	    if not lightSensor.isDetected():	    
	        led.on()		
	        print("plus de lumiere")
	
	    if soundSensor.isDetected():	    
	        led.on()
	        print("son")
