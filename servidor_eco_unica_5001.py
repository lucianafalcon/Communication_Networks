import socket
import sys

# Forzar UTF-8 (opción 2). Si no lo necesitás, puedes quitar estas dos líneas.
# sys.stdout.reconfigure(encoding='utf-8')

HOST = '0.0.0.0'
PORT = 5001

def manejar_cliente(conn, addr):
    print(f"Conexión desde {addr}")        # 'ó' y acentos siguen bien en cp1252
    f = conn.makefile('rwb', buffering=0)
    f.write("Servidor de eco listo. Usa /eco texto\r\n".encode('utf-8'))
    while True:
        line = f.readline()
        if not line:
            break
        # decodificamos según Latin-1 para aceptar cualquier byte sin error
        data = line.decode('latin-1').strip()    # pongo latin-1 en vez de 'utf-8 no acepta comandos en español, y el utf-16 ocupa mas espacio
        # usa ASCII arrow para evitar el UnicodeEncodeError
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
    while True:
        # 1) Creamos el socket de escucha
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen(1)  # backlog = 1 (suficiente)
        print(f"[eco] escuchando en puerto {PORT}")

        # 2) Esperamos y aceptamos UNA sola conexión
        conn, addr = s.accept()
        print(f"--> Conexión aceptada de {addr}")

        # 3) Cerramos el socket de escucha inmediatamente
        #    para que nuevos SYN reciban RST de inmediato
        s.close()

        # 4) Atendemos al cliente
        manejar_cliente(conn, addr)

        # 5) Cuando el cliente cierra, volvemos al loop y recreamos el listener

if __name__ == "__main__":
    main()