from machine import Pin, PWM, I2C
from hcsr04 import HCSR04
from servo import Servo
from i2c_lcd import I2cLcd
import time

# =====================================
# INITIALISATION LCD
# =====================================

i2c = I2C(0, sda=Pin(21), scl=Pin(22), freq=400000)

LCD_ADDR = 0x27

lcd = I2cLcd(i2c, LCD_ADDR, 2, 16)

# =====================================
# INITIALISATION SERVO
# =====================================

servo = Servo(Pin(14))

# =====================================
# CAPTEURS ULTRASON
# =====================================

# Capteur extérieur
ultrason_ext = HCSR04(trigger_pin=26, echo_pin=25)

# Capteur intérieur
ultrason_int = HCSR04(trigger_pin=18, echo_pin=19)

# =====================================
# LEDs
# =====================================

led_verte = Pin(4, Pin.OUT)
led_jaune = Pin(15, Pin.OUT)
led_rouge = Pin(13, Pin.OUT)

# =====================================
# ETAT INITIAL
# =====================================

servo.write_angle(180)

couvercle_ferme = True

# =====================================
# FONCTION LEDs OFF
# =====================================

def eteindre_leds():
    led_verte.off()
    led_jaune.off()
    led_rouge.off()

# =====================================
# BOUCLE PRINCIPALE
# =====================================

while True:

    # ===============================
    # LECTURE DISTANCES
    # ===============================

    distance_ext = ultrason_ext.distance_cm()
    time.sleep_ms(25)
    distance_int = ultrason_int.distance_cm()

    print("Distance extérieure :", distance_ext)
    print("Distance intérieure :", distance_int)

    # ===============================
    # GESTION COUVERCLE
    # ===============================

    if 2 < distance_ext < 20 and couvercle_ferme:

        for angle in range(180, 0, -5):
            servo.write_angle(angle)
            time.sleep_ms(20)

        couvercle_ferme = False

    elif distance_ext >= 20 and not couvercle_ferme:

        for angle in range(0, 181, 5):
            servo.write_angle(angle)
            time.sleep_ms(20)

        couvercle_ferme = True

    # ===============================
    # GESTION NIVEAU POUBELLE
    # ===============================

    lcd.clear()

    eteindre_leds()

    # VIDE
    if distance_int >= 40:

        led_verte.on()

        lcd.putstr("Poubelle vide")

    # MOITIE PLEINE
    elif 20 < distance_int < 40:

        led_jaune.on()

        lcd.putstr("A moitie pleine")

    # PLEINE
    else:

        led_rouge.on()

        lcd.putstr("Poubelle pleine")

    # ===============================
    # PAUSE
    # ===============================

    time.sleep(1)