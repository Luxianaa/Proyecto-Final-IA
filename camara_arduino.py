import cv2
import numpy as np
import tensorflow as tf
import serial
import time

arduino = serial.Serial('COM3', 9600)
time.sleep(2)

modelo = tf.keras.models.load_model("modelo_cnn++.h5")

TAM = 80
umbral = 0.90
ventana = 5
historial = []

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (5,5), 0)
    gray = cv2.equalizeHist(gray)

    img = cv2.resize(gray, (TAM, TAM))
    img = img.reshape(1, TAM, TAM, 1).astype("float32") / 255.0

    prob_no = float(modelo.predict(img, verbose=0)[0][0])
    prob_si = 1 - prob_no

    # Guardar historial
    historial.append(prob_si)
    if len(historial) > ventana:
        historial.pop(0)

    promedio = sum(historial) / len(historial)

    # Decisión por promedio
    if promedio > umbral:
        label = f"Cuchillo DETECTADO ({promedio:.2f})"
        color = (0, 0, 255)
        arduino.write(b'0')
    else:
        label = f"No Cuchillo ({promedio:.2f})"
        color = (0, 255, 0)
        arduino.write(b'1')

    cv2.putText(frame, label, (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)

    cv2.imshow("Detector", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
arduino.close()
cv2.destroyAllWindows()
