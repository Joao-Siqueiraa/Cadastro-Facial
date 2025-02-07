import cv2
import face_recognition
import os
import numpy as np
from database import criar_tabelas  # Importa a função do banco de dados
import sqlite3


def cadastrar_usuario(nome):
    cap = cv2.VideoCapture(0)
    print("Posicione seu rosto na câmera e pressione 'q' para capturar.")

    while True:
        ret, frame = cap.read()
        cv2.imshow("Cadastro", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            face_locations = face_recognition.face_locations(frame)
            
            if face_locations:
                face_encoding = face_recognition.face_encodings(frame, face_locations)[0]
                
                imagem_path = f"imagens/{nome}_imagem.jpg"
                if not os.path.exists("imagens"):
                    os.makedirs("imagens")
                cv2.imwrite(imagem_path, frame)

                salvar_no_banco(nome, face_encoding, imagem_path)
                print("Usuário cadastrado com sucesso!")
                break
            else:
                print("Nenhum rosto detectado. Tente novamente.")

    cap.release()
    cv2.destroyAllWindows()

def salvar_no_banco(nome, face_encoding, imagem_path):
    with open(imagem_path, "rb") as f:
        imagem_bin = f.read()

    conn = sqlite3.connect("faces.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO usuarios (nome, encoding, imagem) VALUES (?, ?, ?)", 
                   (nome, face_encoding.tobytes(), imagem_bin))
    conn.commit()
    conn.close()
