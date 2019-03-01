import sys
import time
import Adafruit_DHT
from subprocess import call #la necesitamos para la interrupcion de teclado
import RPi.GPIO as GPIO
from pymongo import MongoClient
import datetime
GPIO.setmode(GPIO.BOARD) #Queremos usar la numeracion de la placa
Cinco = 29
Seis = 31
Doce = 32
Dieciseis =36
#-----------------------------------------CODIGO REFERENTE A LA BASE DE DATOS-----------------------------------------
client = MongoClient('mongodb://admin:1admin@ds263500.mlab.com:63500/arquitwo')
db = client['arquitwo']
#Metodo que todos lo grupos deben usar para insertar a la base de datos
def InsertarXplorer(dev_id,sen_id, posX, posY, value):
    collection = db['XPlorer']
    collection.insert_one({
        "Date": datetime.datetime.now(),
        "Device_ID": dev_id,
        "Sensor_ID": sen_id,
        "X": posX,
        "Y": posY,
        "Sensor_Value": value
    })
#Metodo que indica la posicion a la cual hay que dirigirse
def getPosToMove():
    collection = db["Pic"]
    listx = []
    listxpos = []
    listy = []
    listypos = []
    result = []
    for i in collection.find():
        if(i['X'] == 0):
            listy.append(i['Escala'])
            listypos.append(i['Y'])

        if (i['Y'] == 0):
            listx.append(i['Escala'])
            listxpos.append(i['X'])

    posX = listxpos[listx.index(max(listx))]
    posY = listypos[listy.index(max(listy))]
    result.append(posX)
    result.append(posY)
    return result
matriz = getPosToMove()
print(matriz[0]) #Posicion en X
print(matriz[1]) #Posicion en Y
#------------------------------------CODIGO DE LOS MOTORES, MOVERSE A LA POSICION ------------------------------------
GPIO.setwarnings(False)

GPIO.setup(Cinco, GPIO.OUT)
GPIO.setup(Seis, GPIO.OUT)
GPIO.setup(Doce, GPIO.OUT)
GPIO.setup(Dieciseis, GPIO.OUT)
def right(seconds):
    #high to front left motor
    GPIO.output(Cinco,GPIO.HIGH) #ADELANTE
    GPIO.output(Seis,GPIO.LOW)
    GPIO.output(Doce,GPIO.LOW) #ATRAS
    GPIO.output(Dieciseis,GPIO.HIGH)
    print('right')
    time.sleep(seconds)
def left(seconds):
    #high to front right motor
    GPIO.output(Cinco,GPIO.LOW) #ATRAS
    GPIO.output(Seis,GPIO.HIGH)
    GPIO.output(Doce,GPIO.HIGH) #ADELANTE
    GPIO.output(Dieciseis,GPIO.LOW)
    
    print('left')
    time.sleep(seconds)
def forward(seconds):
    GPIO.output(Cinco,GPIO.HIGH) #ADELANTEDerecha
    GPIO.output(Seis,GPIO.LOW)
    GPIO.output(Doce,GPIO.HIGH) #ADELANTEIzquierda
    GPIO.output(Dieciseis,GPIO.LOW)
    print('forward')
    time.sleep(seconds)
def backwards(seconds):
    GPIO.output(Cinco,GPIO.LOW) #ATRAS
    GPIO.output(Seis,GPIO.HIGH)
    GPIO.output(Doce,GPIO.LOW) #ATRAS
    GPIO.output(Dieciseis,GPIO.HIGH)
    print('atras')
    time.sleep(seconds)
def stop(seconds):
    GPIO.output(Cinco,GPIO.LOW) #ATRAS
    GPIO.output(Seis,GPIO.LOW)
    GPIO.output(Doce,GPIO.LOW) #ATRAS
    GPIO.output(Dieciseis,GPIO.LOW)
    print('stop')
    time.sleep(seconds)
def MovMeterFoward():
    for i in range(0,1):
        forward(2.5)
        stop(1)
MovX = 5
MovY = 5
while (MovX > matriz[1]):
    MovMeterFoward()
    MovX = MovX - 1
left(1.6)
stop(1)
while (MovY > matriz[0]):
    MovMeterFoward()
    MovY = MovY - 1
#---------------------------------CODIGO DE LOS SENSORES (HUMEDAD,TEMPERATURA Y PROXIMIDAD)----------------------------------

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
    return medida
sensor = Adafruit_DHT.DHT11 #Configuracion del tipo de sensor DHT
pin = 23                    #Configuracion del puerto GPIOIO al cual esta conectado (GPIOIO 23)
try:                        
    contador = 0
    while (contador < 60):#Debemos medir datos 2 minutos, y tardamos 2 seg por medicion
        humedad, temperatura = Adafruit_DHT.read_retry(sensor, pin)
        #Imprime en la consola las variables temperatura y humedad con un decimal
        print('Temperatura={0:0.1f}*  Humedad={1:0.1f}%'.format(temperatura, humedad))
        #Proximidad
        Proximidad = detectarObstaculo()
        print ("%.2f" %Proximidad) #por ultimo, vamos a mostrar el resultado por pantalla
        #Duerme 2 segundos
        time.sleep(2)
        contador = contador + 1
        InsertarXplorer(2,1, matriz[0], matriz[1], temperatura)
        InsertarXplorer(2,2, matriz[0], matriz[1], humedad)
        InsertarXplorer(2,4, matriz[0], matriz[1], Proximidad)
except KeyboardInterrupt: 
	print("Ha ocurrido un error inesperado al utilizar los sensores") # Imprime en pantalla el error e

 #----------------------------------CODIGO DE LOS MOTORES, REGRESAR AL ORIGEN (0,0)-------------------------------------
while (MovY <  5):
    backwards(2.5)
    MovY = MovY + 1
left(1.6)
stop(1)
while (MovX < 5):
    MovMeterFoward()
    MovX = MovX + 1
left(1.6)
left(1.6)
stop(1)
print ("Acabado.")
#por ultimo hay que restablecer los pines GPIO
print ("Limpiando...")
GPIO.cleanup()