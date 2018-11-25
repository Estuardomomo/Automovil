import sys
import time
import Adafruit_DHT
from subprocess import call #la necesitamos para la interrupcion de teclado
import RPi.GPIO as GPIO
#------------------------------------CODIGO DE LOS MOTORES, MOVERSE A LA POSICION ------------------------------------
#---------------------------------CODIGO DE LOS SENSORES (HUMEDAD,TEMPERATURA Y LUZ)----------------------------------
GPIO.setmode(GPIO.BOARD) #Queremos usar la numeracion de la placa
#Definimos los dos pines del sensor que hemos conectado: Trigger y Echo
Trig = 11
Echo = 13
#Hay que configurar ambos pines del HC-SR04
GPIO.setup(Trig, GPIO.OUT)
GPIO.setup(Echo, GPIO.IN)
#Para leer la distancia del sensor al objeto, creamos una funcion
def detectarObstaculo():
    GPIO.output(Trig, False) #apagamos el pin Trig
    time.sleep(2*10**-6) #esperamos dos microsegundos
    GPIO.output(Trig, True) #encendemos el pin Trig
    time.sleep(10*10**-6) #esperamos diez microsegundos
    GPIO.output(Trig, False) #y lo volvemos a apagar
    #empezaremos a contar el tiempo cuando el pin Echo se encienda
    while GPIO.input(Echo) == 0:
        start = time.time()
    while GPIO.input(Echo) == 1:
        end = time.time()
    #La duracion del pulso del pin Echo sera la diferencia entre
    #el tiempo de inicio y el final
    duracion = end-start
    #Este tiempo viene dado en segundos. Si lo pasamos
    #a microsegundos, podemos aplicar directamente las formulas
    #de la documentacion
    duracion = duracion*10**6
    medida = duracion/58 #hay que dividir por la constante que pone en la documentacion, nos dara la distancia en cm
    print ("%.2f" %medida) #por ultimo, vamos a mostrar el resultado por pantalla
sensor = Adafruit_DHT.DHT11 #Configuracion del tipo de sensor DHT
pin = 23                    #Configuracion del puerto GPIO al cual esta conectado (GPIO 23)
try:                        
	contador = 0
    while True:     #Debemos medir datos 2 minutos, y tardamos 2 seg por medición.
	    humedad, temperatura = Adafruit_DHT.read_retry(sensor, pin)
        #Imprime en la consola las variables temperatura y humedad con un decimal
        print('Temperatura={0:0.1f}*  Humedad={1:0.1f}%'.format(temperatura, humedad))
        #Proximidad
        detectarObstaculo()
        #Duerme 2 segundos
        time.sleep(2)
        contador = contador + 1
except KeyboardInterrupt: 
	print("Ha ocurrido un error inesperado al utilizar los sensores") # Imprime en pantalla el error e
#por ultimo hay que restablecer los pines GPIO
print ("Limpiando...")
GPIO.cleanup()
print ("Acabado.")
 #----------------------------------CODIGO DE LOS MOTORES, REGRESAR AL ORIGEN (0,0)-------------------------------------