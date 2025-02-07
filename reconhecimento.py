import cv2
import face_recognition
import numpy as np
import sqlite3
from historico import registrar_login

def reconhecer_usuario():
    conn = sqlite3.connect("faces.db")
    cursor = conn.cursor()
    cursor.execute("SELECT nome, encoding FROM usuarios")  # Não é necessário pegar a imagem
    usuarios = cursor.fetchall()
    conn.close()

    cap = cv2.VideoCapture(0)
    print("Posicione seu rosto na câmera para login")

    while True:
        ret, frame = cap.read()
        cv2.imshow("Reconhecimento", frame)

        face_locations = face_recognition.face_locations(frame)
        
        if face_locations:
            face_encoding = face_recognition.face_encodings(frame, face_locations)[0]
            
            for nome, encoding in usuarios:
                stored_encoding = np.frombuffer(encoding, dtype=np.float64)
                match = face_recognition.compare_faces([stored_encoding], face_encoding)[0]
                
                if match:
                    print(f"Bem-vindo, {nome}!")
                    cap.release()
                    cv2.destroyAllWindows()
                    return
            print("Rosto não reconhecido.")
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

