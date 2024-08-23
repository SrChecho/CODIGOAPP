# barras_cont.py
import cv2
import mediapipe as mp
import time
import matplotlib.pyplot as plt
import csv
from tkinter import simpledialog

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

# Enum para los estados
class EstadoDominada:
    ARRIBA_BARRA = 1
    ABAJO_BARRA = 2

def detectar_dominada(resultados, estado_previo):
    num_de_dominadas_correctas = 0
    estado_actual = estado_previo

    # Si se detecta un pose, revisamos si cumple con los requisitos de la dominada
    if resultados.pose_landmarks:
        muneca_izquierda = resultados.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_WRIST]
        codo_izquierdo = resultados.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_ELBOW]
        hombro_izquierdo = resultados.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER]

        # Si el hombro está por encima de la muñeca y el hombro está por encima del codo, consideramos que se trata de una dominada correcta
        if hombro_izquierdo.y < muneca_izquierda.y and hombro_izquierdo.y < codo_izquierdo.y:
            estado_actual = EstadoDominada.ARRIBA_BARRA
        else:
            estado_actual = EstadoDominada.ABAJO_BARRA

        # Contabilizar una dominada al pasar de "abajo" a "arriba"
        if estado_previo == EstadoDominada.ABAJO_BARRA and estado_actual == EstadoDominada.ARRIBA_BARRA:
            num_de_dominadas_correctas += 1

    return num_de_dominadas_correctas, estado_actual

def run_barras_cont(full_name, camera_index=0):
    # Inicializar las soluciones de pose y reconocimiento facial de MediaPipe
    with mp_pose.Pose(min_detection_confidence=0.4, min_tracking_confidence=0.4) as pose:
        # Crear un objeto de captura de video
        cap = cv2.VideoCapture(camera_index)
        
        num_de_dominadas = 0  # Inicializar el contador de dominadas correctas
        estado = EstadoDominada.ABAJO_BARRA  # Inicializar el estado
        total_de_dominadas = 0  # Inicializar el contador total de dominadas

        tiempo_inicio = time.time()
        tiempo_final = tiempo_inicio + 21  # 21 segundos de conteo de dominadas

        conteo_total = []  # Lista para almacenar el conteo total de dominadas

        while cap.isOpened() and time.time() <= tiempo_final:
            # Leer un frame del video
            ret, frame = cap.read()

            # Convertir el frame en un frame RGB (abierto por MediaPipe)
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Procesar el frame para detectar el pose
            results = pose.process(rgb_frame)

            # Dibujar el resultado en el frame
            mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

            # Detectar y contar dominadas correctas
            num_de_dominadas, estado = detectar_dominada(results, estado)

            # Agregar al contador total de dominadas
            total_de_dominadas += num_de_dominadas

            # Agregar al conteo total
            conteo_total.append(total_de_dominadas)

            # Mostrar el número de dominadas correctas y el total en el frame
            cv2.putText(frame, f"Total Dominadas: {total_de_dominadas}", (10, 200), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

            # Mostrar el frame en una ventana
            cv2.imshow('Video', frame)

            # Salir del bucle si se presiona la tecla 'q'
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # Liberar los recursos y cerrar todas las ventanas
        cap.release()
        cv2.destroyAllWindows()

        # Mostrar solo el último resultado en la consola
        ultimo_resultado = conteo_total[-1]
        print(f"Resultados guardados en {full_name}_resultados_dominadas.csv. Último resultado: {ultimo_resultado}")

        # Guardar los resultados en un archivo CSV
        with open('resultados_dominadas.csv', 'a', newline='') as csvfile:
            fieldnames = ['Nombre','Dominadas']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            # Escribir el encabezado
            if csvfile.tell() == 0:
                writer.writeheader()

            # Escribir el último valor del conteo total de dominadas en el archivo CSV
            writer.writerow({'Nombre': full_name,'Dominadas': ultimo_resultado})

        # Generar la gráfica de los resultados
        plt.plot(range(1, len(conteo_total) + 1), conteo_total, label="Dominadas")
        plt.xlabel("Tiempo (segundos)")
        plt.ylabel("Dominadas")
        plt.title("Resultados del ejercicio de dominadas")
        plt.show()

if __name__ == "__main__":
    run_barras_cont("Prueba")
