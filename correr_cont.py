import cv2
import mediapipe as mp
import time
import pandas as pd
import matplotlib.pyplot as plt
import csv  # Añadido
from tkinter import simpledialog

def run_correr_cont(full_name, camera_index=0):
    # Inicializar MediaPipe
    mp_drawing = mp.solutions.drawing_utils
    mp_pose = mp.solutions.pose

    # Inicializar el contador de vueltas y los tiempos
    count = 0
    lap_times = []
    lap_start_time = None
    lap_complete = False

    # Umbral para activar el botón izquierdo y derecho
    left_threshold = 0.2  # Ajusta este valor según la posición de los botones en la pantalla
    right_threshold = 0.8  # Ajusta este valor según la posición de los botones en la pantalla

    # Punto de referencia (cambiar a 0 o 14 según el caso)
    reference_point_index = 0

    # Inicializar la captura de la cámara
    cap = cv2.VideoCapture(camera_index)  # Cambia el número a 1 si tienes una cámara externa

    # Crear un objeto para la detección de postura
    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                continue

            # Voltear el marco horizontalmente para que sea como un espejo
            frame = cv2.flip(frame, 1)

            # Convertir el marco a formato RGB
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Realizar la detección de la postura
            results = pose.process(frame_rgb)

            if results.pose_landmarks:
                # Obtener las coordenadas de los puntos clave de la postura
                landmarks = results.pose_landmarks.landmark

                # Obtener la coordenada x del punto de referencia
                reference_x = landmarks[reference_point_index].x

                 # Verificar el cruce (del umbral izquierdo y derecho
                if (reference_x < left_threshold) and not lap_complete:
                    lap_complete = True
                    if lap_start_time is None:
                        lap_start_time = time.time()
                    elif lap_start_time is not None:
                        lap_times.append(round(time.time() - lap_start_time, 2))
                        lap_start_time = None
                        lap_start_time = time.time()
                        count += 1
                elif (reference_x >= right_threshold) and lap_complete:
                    lap_complete = False

                # Dibujar líneas verticales en los umbrales izquierdo y derecho
                frame_height, frame_width, _ = frame.shape
                left_x_pixel = int(left_threshold * frame_width)
                right_x_pixel = int(right_threshold * frame_width)
                cv2.line(frame, (left_x_pixel, 0), (left_x_pixel, frame_height), (0, 255, 0), 2)
                cv2.line(frame, (right_x_pixel, 0), (right_x_pixel, frame_height), (0, 255, 0), 2)

                # Dibujar puntos clave en el marco
                mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

            # Mostrar el número de vueltas en el marco
            cv2.putText(frame, f'Vueltas: {count}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

            # Mostrar el marco
            cv2.imshow('Contador de Vueltas', frame)

            # Salir del bucle después de 5 vueltas
            if count >= 5:
                break

            # Salir del bucle si se presiona la tecla 'q'
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # Añadir los tiempos de las vueltas al archivo CSV existente
        with open('vueltasprueba.csv', 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            if csvfile.tell() == 0:
                writer.writerow(['Nombre', 'Vueltas', 'Tiempo por Vuelta (s)'])
            for lap_time in lap_times:
                writer.writerow([full_name, count, lap_time])

        # Generar una gráfica de los tiempos de vuelta
        plt.figure()
        plt.plot(range(1, len(lap_times) + 1), lap_times, marker='o', label='Tiempo por Vuelta')
        plt.title('Tiempos de Vuelta')
        plt.xlabel('Vuelta')
        plt.ylabel('Tiempo (s)')
        plt.legend()
        plt.grid(True)

        # Mostrar la gráfica
        plt.show()

        # Liberar los recursos
        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    run_correr_cont("Prueba")
