import socket

HOST = '0.0.0.0'
PORT = 5000

def manejar_cliente(conn, addr):          #conn: es el socket de la conexión, con el que podés enviar y recibir datos, addr guarda ip, puerto  cliente
    print(f"Conexión desde {addr}")         
    f = conn.makefile('rwb', buffering=0)       #Convierte el socket conn en un "archivo" f para leer y escribir más cómodamente. 'rwb' = read/write binary. buffering=0: sin búfer, los datos se mandan inmediatam.
    f.write(b"Servidor de suma listo. Usa /suma num1 num2\r\n")
    while True:
        line = f.readline()

        if not line:  #Esto verifica si el cliente cerró la conexión o no mandó nada
            break

        data = line.decode('utf-8', errors='replace').strip()    #decode('utf-8'): Convierte esos bytes en texto legible. .strip(): Saca espacios y saltos de línea del principio y el final.
        print(f"> {addr} -> {data!r}")
        partes = data.split()
        if len(partes) == 3 and partes[0] == "/suma":
            try:
                n1 = float(partes[1])
                n2 = float(partes[2])
                resp = f"{n1:g} + {n2:g} = {n1+n2:g}\r\n"
                f.write(resp.encode('utf-8'))
            except ValueError:
                f.write(b"Error: argumentos no numericos. Cerrando.\r\n")
                break
        else:
            f.write(b"Comando invalido. Cerrando conexion.\r\n")
            break

    conn.close()
    print(f"Cerrada conexión con {addr}")

def main():
    while True:
        # 1) Creamos el socket de escucha
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)      #socket.AF_INET: Indica que vas a usar direcciones IPv4.  socket.SOCK_STREAM: Vas a usar TCP (no UDP).
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)     #setsockopt(...): Permite reusar el puerto rápidamente si reiniciás el servidor
        s.bind((HOST, PORT))      #bind((HOST, PORT)): Le dice al sistema: “escuchá conexiones en esta IP y puerto”.
        s.listen() #se pone en escucha el socket
        print(f"[suma] escuchando en puerto {PORT}")

        # 2) Esperamos y aceptamos UNA sola conexión
        conn, addr = s.accept()
        print(f"--> Conexión aceptada de {addr}")

        # 3) Cerramos el socket de escucha inmediatamente
        #    para que nuevos SYN reciban RST de inmediato
        s.close()

        # 4) Atendemos al cliente
        manejar_cliente(conn, addr)

        # 5) Cuando el cliente cierra, volvemos al loop y recreamos el listener/

if __name__ == "__main__":
    main()
