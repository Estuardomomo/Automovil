import sys
import time
import Adafruit_DHT

while True:
 #------------------------------------CÓDIGO DE LOS MOTORES, MOVERSE A LA POSICIÓN ------------------------------------
 
 #---------------------------------CÓDIGO DE LOS SENSORES (HUMEDAD,TEMPERATURA Y LUZ)----------------------------------
    sensor = Adafruit_DHT.DHT11 #Configuracion del tipo de sensor DHT
    pin = 23                    #Configuracion del puerto GPIO al cual esta conectado (GPIO 23)
    try:                        
	    contador = 0
        while contador < 24     #Debemos medir datos 2 minutos, y tardamos 5 seg por medición.
		humedad, temperatura = Adafruit_DHT.read_retry(sensor, pin)
		#Imprime en la consola las variables temperatura y humedad con un decimal
		print('Temperatura={0:0.1f}*  Humedad={1:0.1f}%'.format(temperatura, humedad))
        #Duerme 5 segundos
		time.sleep(5)
    except Exception,e: 
	print str(e) # Imprime en pantalla el error e
 #----------------------------------CÓDIGO DE LOS MOTORES, REGRESAR AL ORIGEN (0,0)-------------------------------------