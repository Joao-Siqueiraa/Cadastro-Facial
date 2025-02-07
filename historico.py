import sqlite3
import datetime

def registrar_login(usuario_id, nome):
    conn = sqlite3.connect("faces.db")
    cursor = conn.cursor()
    data_hora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("INSERT INTO historico_logins (usuario_id, nome, data_hora) VALUES (?, ?, ?)", 
                   (usuario_id, nome, data_hora))
    conn.commit()
    conn.close()

def exibir_historico():
    conn = sqlite3.connect("faces.db")
    cursor = conn.cursor()
    cursor.execute("SELECT nome, data_hora FROM historico_logins ORDER BY data_hora DESC")
    logins = cursor.fetchall()
    conn.close()

    print("\n📌 Histórico de Logins:")
    for nome, data_hora in logins:
        print(f"{data_hora} - {nome}")
