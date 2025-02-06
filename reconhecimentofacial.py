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
    print("Posicione seu rosto na câmera e aguarde o sistema detectar automaticamente")
    
def cadastrar_usuario(nome):
    cap = cv2.VideoCapture(0)
    print("Posicione seu rosto na câmera e aguarde o sistema detectar automaticamente.")
    
    while True:
        ret, frame = cap.read()
        cv2.imshow("Cadastro", frame)

        # Detecta o rosto em tempo real
        face_locations = face_recognition.face_locations(frame)
        
        if face_locations:
            face_encoding = face_recognition.face_encodings(frame, face_locations)[0]  # Codifica a face
            
            # Salva a imagem
            imagem_path = f"imagens/{nome}_imagem.jpg"
            if not os.path.exists("imagens"):
                os.makedirs("imagens")
            cv2.imwrite(imagem_path, frame)  # Salva a imagem capturada

            # Salva no banco de dados
            salvar_no_banco(nome, face_encoding, imagem_path)
            print("Usuário cadastrado com sucesso!")
            break
        
        # Pode adicionar um tempo de espera ou uma mensagem, caso o rosto não seja encontrado
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
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
        
        # Pausa ou verifica o rosto a cada frame
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

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
