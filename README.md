# Raspberry Pi-Móvil
El objetivo de este proyecto es crear un “buscador de luz” el cual funcionará basado en un PIC 16F877 como unidad de control de direcciones y un Raspberry Pi 3b como controlador del dispositivo independiente y conexión a la base de datos NOSQL.
## Matriz de buscadores de luz
La matriz de buscadores de luz es una matriz compuesta por los dispositivos buscadores de luz que estan ubicados 5 en fila que representan el eje x y otros 5 en fila que representan el eje y. De esta manera se forma la matriz de 5x5 que sirve para obtener la ubicación con mayor intensidad de luz. 

Tras obtener los datos de los 10 dispositivos, la posición se calcula obteniendo el dipositivo con mayor luz en x y el dispositvo con mayor luz en y. Los dispositivos suben los datos a una base de datos no relacional.
## Algoritmo del movimiento y motores DC

Los motores empleados para el movimiento del carro son motores DC. Para controlar los motores se optó por usar el integrado LD293D, el integrado funciona tomando voltaje de la raspberry y compartiendo tierra común. Los motores por ser de corriente directa (DC) se
mueven dependiendo del voltaje que se les manda. Este voltaje lo manejamos con la raspberry con la libreria GPIO, que nos permite mandar LOW (cero lógico) o HIGH (uno lógico).

El algoritmo de movimiento se basa en mandar salidas a los pines por cierta cantidad de segundos, esto se realizó haciendo varias pruebas poniendo diferentes cantidades de tiempo y viendo cuanto se movía.
## Sensores de temperatura, humedad y proximidad
**1. Sensor de humedad y temperatura DHT11**

|Sensor de humedad & temperatura|
|---------------|
|Modelo: DHT11|
|Alimentación: 3.3-5V|
|Consumo: 2.5 mA|
|Salida: Señal dígital|
|Temperatura -----------------------------|
|Rango: 0-50 C|
|Precisión: +/- 2 C|
|Humedad ---------------------------------|
|Rango: 20-90%|
|Precisión: +/- 5%|

**2. Sensor de proximidad HC-SR04**

El HC-SR04 posee dos transductores cilindricos de color gris. El sensor envía un pulso de ultrasonidos a través de un transductor cuándo el pin “Trig” está en alto. El pulso avanza hasta que choca con un obstáculo y rebota, volviendo así al sensor. El segundo transductor detecta la señal de este “eco” y mide el tiempo que ha tardado la señal en rebotar. Después, activa el pin “Echo” durante un tiempo proporcional al que ha tardado en llegar el “eco” al segundo transductor. Esta señal después se envía a la Raspberry Pi, que mide la duración del pulso y la multiplica por una constante para tener la distancia en centímetros aproximada.
## Conexión Raspberry pi-Base de datos
La base de datos fue empleada en mongoDB, por lo que es una base de datos no relacional. A partir de eso se utiliza el servicio de mlab para poder manejar la base de datos por medio de una aplicacion diseñada en Node.js. Para la conexion con la base de datos se hace uso de un modulo de mongoDB para python que se llama pymongo, que permite conectarse a la base de datos y realizar tanto consultas como inserts.