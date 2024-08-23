import cv2
import mediapipe as mp
import time
import matplotlib.pyplot as plt
import csv

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

class EstadoAbdominales:
    ARRIBA_NARIZ = 1
    ABAJO_NARIZ = 2

def detectar_abdominales(resultados, estado_previo, umbral_nariz):
    num_de_abdominales_correctos = 0
    estado_actual = estado_previo

    # Si se detecta un pose, revisamos si cumple con los requisitos del abdominal
    if resultados.pose_landmarks:
        nariz = resultados.pose_landmarks.landmark[mp_pose.PoseLandmark.NOSE]

        # Si la nariz está por encima del umbral, consideramos que se trata del inicio del abdominal
        if nariz.y > umbral_nariz:
            estado_actual = EstadoAbdominales.ARRIBA_NARIZ
        else:
            estado_actual = EstadoAbdominales.ABAJO_NARIZ

        # Contabilizar un abdominal al pasar de "abajo" a "arriba"
        if estado_previo == EstadoAbdominales.ABAJO_NARIZ and estado_actual == EstadoAbdominales.ARRIBA_NARIZ:
            num_de_abdominales_correctos += 1

    return num_de_abdominales_correctos, estado_actual

def run_abdominales_cont(full_name, camera_index=0):
    pose = mp_pose.Pose()
    cap = cv2.VideoCapture(camera_index)
    
    conteo_abdominales = 0
    en_abdominal = False
    umbral_nariz = 0.4

    tiempo_inicio = time.time()
    tiempo_final = tiempo_inicio + 20

    conteo_total = []

    while cap.isOpened():
        # Leer un frame del video
        ret, frame = cap.read()

        if tiempo_inicio <= time.time() <= tiempo_final:
            # Convertir el frame a RGB para usar con MediaPipe
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Procesar el frame para detectar la pose
            results = pose.process(frame_rgb)

            # Dibujar los puntos del cuerpo en el frame
            mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

            # Detectar y contar abdominales correctos
            num_de_abdominales, en_abdominal = detectar_abdominales(results, en_abdominal, umbral_nariz)

            # Agregar al contador total de abdominales
            conteo_abdominales += num_de_abdominales

            # Agregar al conteo total
            conteo_total.append(conteo_abdominales)

            # Mostrar el número de abdominales realizados en el frame
            cv2.putText(frame, f"Total Abdominales: {conteo_abdominales}", (10, 200), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        elif tiempo_final < time.time():
            # Muestra el resultado al final de los 20 segundos
            cv2.putText(frame, f"Felicidades. Realizaste {conteo_abdominales} abdominales en 20 segundos.", (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 3)
        else:
            break  # Sale del bucle si el tiempo no está en ninguna de las fases anteriores

        # Mostrar el frame en una ventana
        cv2.imshow('Verificacion de Abdominales', frame)

        # Salir del bucle si se presiona la tecla 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        if tiempo_final < time.time():
            break  # Sale del bucle después de mostrar el resultado al final de los 20 segundos

    # Liberar los recursos y cerrar la ventana
    cap.release()
    cv2.destroyAllWindows()

    # Mostrar solo el último resultado en la consola
    if conteo_total:
        ultimo_resultado = conteo_total[-1]
        print(f"Resultados guardados en resultados_abdominales.csv. Último resultado: {ultimo_resultado}")
    else:
        print("No se encontraron resultados de abdominales.")

    # Guardar los resultados en un archivo CSV
    with open('resultados_abdominales.csv', 'a', newline='') as csvfile:
        fieldnames = ['Nombre', 'Abdominales']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # Escribir el encabezado solo si es la primera vez que se escribe en el archivo
        if csvfile.tell() == 0:
            writer.writeheader()

        # Escribir el nombre y el último valor del conteo de abdominales en el archivo CSV
        writer.writerow({'Nombre': full_name, 'Abdominales': ultimo_resultado})

    # Generar la gráfica de los resultados
    if tiempo_final < time.time():
        plt.plot(range(1, len(conteo_total) + 1), conteo_total, label="Abdominales")
        plt.xlabel("Tiempo (segundos)")
        plt.ylabel("Abdominales")
        plt.title(f"Resultados de abdominales")
        plt.show()

if __name__ == "__main__":
    run_abdominales_cont("Prueba")