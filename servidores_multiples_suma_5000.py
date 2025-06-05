import socket
import threading

HOST = '0.0.0.0'
PORT = 5000

def manejar_cliente(conn, addr):
    print(f"Conexión desde {addr}")
    f = conn.makefile('rwb', buffering=0)
    f.write("Servidor de suma listo. Usa /suma num1 num2\r\n".encode('utf-8'))
    while True:
        line = f.readline()
        if not line:
            break

        data = line.decode('utf-8', errors='replace').strip()
        print(f"> {addr} -> {data!r}")
        partes = data.split()
        if len(partes) == 3 and partes[0] == "/suma":
            try:
                n1 = float(partes[1])
                n2 = float(partes[2])
                resp = f"{n1:g} + {n2:g} = {n1+n2:g}\r\n"
                f.write(resp.encode('utf-8'))
            except ValueError:
                f.write("Error: argumentos no numéricos. Cerrando.\r\n".encode('utf-8'))
                break
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
        print(f"[suma] escuchando en puerto {PORT}")
        while True:
            conn, addr = s.accept()
            threading.Thread(target=manejar_cliente, args=(conn, addr)).start()  #daemon=True, lo pondria para cerrar el hilo de los clientes total...

if __name__ == "__main__":
    main()
