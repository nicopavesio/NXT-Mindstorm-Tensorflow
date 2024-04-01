import numpy as np
import tensorflow as tf
import nxt.motor
import nxt.sensor
import nxt.locator
import nxt.sensor.generic
import time

#Creacion artifical de datos
num_samples = 10000
distances = np.random.randint(0, 251, size=num_samples)  
actions = np.where(distances < 50, 1, 0)  
training_data = np.column_stack((distances, actions))
x_train = training_data[:, 0] / 250 
y_train = training_data[:, 1]

#Declaracion, compilacion y entrenamiento del modelo
model = tf.keras.Sequential([
    tf.keras.layers.Dense(10, activation='relu', input_shape=(1,)),
    tf.keras.layers.Dense(1, activation='sigmoid')
])
model.compile(optimizer='adam',
              loss='binary_crossentropy',
              metrics=['accuracy'])
model.fit(x_train, y_train, epochs=100)

#Implementacion con Robot
with nxt.locator.find(host="00:16:53:1B:A0:FD") as b:
    print("Conectado:", b.get_device_info()[0])
    motor_derecha = b.get_motor(nxt.motor.Port.B)
    motor_izquierda = b.get_motor(nxt.motor.Port.A)
    sensor = b.get_sensor(nxt.sensor.Port.S4)
    
    for i in range(1000):
        distancia = sensor.get_sample()
        distanciaNormalizada = distancia/250
        prediccion = model.predict(np.array([distanciaNormalizada]))
        print("Distancia: ", distancia)
        
        if prediccion > 0.5 :
            print("A girar")
            while distancia < 50:  
                print("Girando")
                motor_derecha.run(100)
                motor_izquierda.run(-100)
                distancia = sensor.get_sample()
            motor_derecha.brake()
            motor_izquierda.brake()
            
        else:
            print("Hacia adelante")
            motor_derecha.run(100)
            motor_izquierda.run(100)
            time.sleep(2)
            motor_derecha.brake()
            motor_izquierda.brake()
        time.sleep(1)
            
        
       