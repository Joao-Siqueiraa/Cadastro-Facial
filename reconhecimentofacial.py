import cv2
import face_recognition
import sqlite3
import numpy as np
import os

def criar_tabela():
    conn = sqlite3.connect("faces.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS usuarios (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        nome TEXT,
                        encoding BLOB,
                        imagem BLOB)''')  # Adiciona a coluna imagem
    conn.commit()
    conn.close()

def cadastrar_usuario(nome):
    cap = cv2.VideoCapture(0)
    print("Posicione seu rosto na câmera e pressione 'q' para capturar")
    
    while True:
        ret, frame = cap.read()
        cv2.imshow("Cadastro", frame)

        # Espera até que a tecla 'q' seja pressionada
        if cv2.waitKey(1) & 0xFF == ord('q'):
            face_locations = face_recognition.face_locations(frame)  # Detecta a face
            if face_locations:
                face_encoding = face_recognition.face_encodings(frame, face_locations)[0]  # Codifica a face
                
                # Salva a imagem capturada
                imagem_path = f"imagens/{nome}_imagem.jpg"
                if not os.path.exists("imagens"):
                    os.makedirs("imagens")
                cv2.imwrite(imagem_path, frame)  # Salva a imagem como .jpg

                # Salva no banco de dados
                salvar_no_banco(nome, face_encoding, imagem_path)
                print("Usuário cadastrado com sucesso!")
                break
            else:
                print("Nenhum rosto detectado. Tente novamente.")
    
    cap.release()
    cv2.destroyAllWindows()

def salvar_no_banco(nome, face_encoding, imagem_path):
    # Converte a imagem para binário para armazenar no banco de dados
    with open(imagem_path, "rb") as f:
        imagem_bin = f.read()
    
    conn = sqlite3.connect("faces.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO usuarios (nome, encoding, imagem) VALUES (?, ?, ?)", 
                   (nome, face_encoding.tobytes(), imagem_bin))
    conn.commit()
    conn.close()

def reconhecer_usuario():
    conn = sqlite3.connect("faces.db")
    cursor = conn.cursor()
    cursor.execute("SELECT nome, encoding, imagem FROM usuarios")
    usuarios = cursor.fetchall()
    conn.close()

    cap = cv2.VideoCapture(0)
    print("Posicione seu rosto na câmera para login")

    while True:
        ret, frame = cap.read()
        cv2.imshow("Reconhecimento", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            face_locations = face_recognition.face_locations(frame)
            if face_locations:
                face_encoding = face_recognition.face_encodings(frame, face_locations)[0]
                
                for nome, encoding, imagem_bin in usuarios:
                    stored_encoding = np.frombuffer(encoding, dtype=np.float64)
                    match = face_recognition.compare_faces([stored_encoding], face_encoding)[0]
                    
                    if match:
                        print(f"Bem-vindo, {nome}!")
                        
                        # Exibir a imagem associada ao usuário
                        imagem_path = f"imagens/{nome}_imagem.jpg"
                        with open(imagem_path, "wb") as f:
                            f.write(imagem_bin)  # Salva a imagem binária em um arquivo para exibir
                        img = cv2.imread(imagem_path)
                        cv2.imshow(f"{nome}'s Foto", img)
                        cv2.waitKey(0)  # Espera até pressionar qualquer tecla
                        cv2.destroyAllWindows()
                        
                        cap.release()
                        cv2.destroyAllWindows()
                        return
                print("Rosto não reconhecido.")
            else:
                print("Nenhum rosto detectado. Tente novamente.")
    
    cap.release()
    cv2.destroyAllWindows()

# Criar banco de dados ao iniciar o código
criar_tabela()

# Exemplo de uso
opcao = input("Digite 'c' para cadastrar ou 'r' para reconhecer: ")
if opcao == 'c':
    nome = input("Digite seu nome: ")
    cadastrar_usuario(nome)
elif opcao == 'r':
    reconhecer_usuario()
else:
    print("Opção inválida.")
