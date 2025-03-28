from machine import Pin, PWM
from neopixel import NeoPixel
from utime import sleep_ms

# Configuración de pines de botones
s1 = Pin(33, Pin.IN, Pin.PULL_DOWN)  # Rojo
s2 = Pin(32, Pin.IN, Pin.PULL_DOWN)   # Verde
s3 = Pin(25, Pin.IN, Pin.PULL_DOWN)   # Amarillo
s4 = Pin(35, Pin.IN, Pin.PULL_DOWN)  # Azul

# LED integrado en ESP32 (opcional)
led = Pin(2, Pin.OUT)

# Configuración del NeoPixel Ring (16 LEDs)
num_pixels = 16
np = NeoPixel(Pin(15, Pin.OUT), num_pixels)

# Configuración del buzzer
buzzer = PWM(Pin(2))  # Buzzer en el pin 19
buzzer.duty_u16(0)  # Apagar buzzer al inicio

# Notas de la "muerte de Mario" (frecuencias en Hz)
mario_death_notes = [523, 554, 587, 494, 698, 698, 698, 659, 587, 659, 659, 330, 523]
# Duraciones en milisegundos para cada nota
mario_death_durations = [250, 250, 250, 250, 300, 300, 300, 250, 250, 250, 250, 500, 500]

while True:
    a = s1.value()
    b = s2.value()
    c = s3.value()
    d = s4.value()

    sleep_ms(100)  # Pequeña pausa para evitar spam en la consola

    # Encender NeoPixel Ring si se cumple la condición
    if (a and c) or (c and d) or (a and b):
        for i in range(num_pixels):
            np[i] = (255, 0, 0)  # Todos los LEDs en rojo
        np.write()
    else:
        for i in range(num_pixels):
            np[i] = (0, 0, 0)  # Apagar todos los LEDs
        np.write()

    # Verificar ecuación lógica para reproducir la melodía
    z = (not d and not c and b and a) or \
        (not d and c and not b and a) or \
        (not d and c and b and not a) or \
        (d and not c and b and a) or \
        (d and c and not b and a) or \
        (d and c and b and not a)

    if z:
        print("🎵 Reproduciendo la melodía de Mario...")
        for i in range(len(mario_death_notes)):
            buzzer.freq(mario_death_notes[i])  # Establecer la frecuencia de la nota
            buzzer.duty_u16(2000)  # Ajustar volumen
            sleep_ms(mario_death_durations[i])  # Duración de la nota
            buzzer.duty_u16(0)  # Pausa entre notas
            sleep_ms(50)  # Pequeña pausa para que no suene pegado

    # Imprimir estado de los sensores
    print(f"s1: {a} s2: {b} s3: {c} s4: {d}")

    dato = int(a) * 4 + int(b) * 2 + int(c)
    print(f"el dato es {dato}")

    sleep_ms(100)  # Pequeña pausa para evitar spam en la consola
