import socket
import threading

HOST = '0.0.0.0'
PORT = 5001

def manejar_cliente(conn, addr):
    print(f"Conexión desde {addr}")
    f = conn.makefile('rwb', buffering=0)
    f.write("Servidor de eco listo. Usa /eco texto\r\n".encode('utf-8'))
    while True:
        line = f.readline()
        if not line:
            break
        data = line.decode('latin-1').strip()
        print(f"> {addr} -> {data!r}")
        if data.startswith("/eco "):
            mensaje = data[5:]
            f.write((mensaje + "\r\n").encode('utf-8'))
        else:
            f.write("Comando inválido. Cerrando conexión.\r\n".encode('utf-8'))
            break
    conn.close()
    print(f"Cerrada conexión con {addr}")

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen()
        print(f"[eco] escuchando en puerto {PORT}")
        while True:
            conn, addr = s.accept()
            threading.Thread(target=manejar_cliente, args=(conn, addr), daemon=True).start()

if __name__ == "__main__":
    main()
