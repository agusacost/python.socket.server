import socket
import threading
import sys

# Configuración
HOST = 'localhost'
PORT = 5556

conectado = False
nombre_usuario = ""


def recibir_mensajes(cliente_socket):
    """
    Recibe mensajes del servidor en un hilo separado
    """
    global conectado
    
    while conectado:
        try:
            # Recibir datagrama
            data, _ = cliente_socket.recvfrom(1024)
            mensaje = data.decode('utf-8')
            
            if mensaje:
                print(mensaje)
        
        except Exception as e:
            if conectado:
                print(f"\n[CLIENTE UDP] Error: {e}")
            break


def iniciar_cliente():
    """Inicia el cliente UDP"""
    global conectado, nombre_usuario
    
    print("\n" + "=" * 60)
    print("       CLIENTE DE CHAT UDP - PYTHON")
    print("=" * 60 + "\n")
    
    # Obtener host y puerto de argumentos
    host = HOST
    port = PORT
    
    if len(sys.argv) == 3:
        host = sys.argv[1]
        try:
            port = int(sys.argv[2])
        except ValueError:
            print("Error: El puerto debe ser un número")
            sys.exit(1)
    
    try:
        # Crear socket UDP
        cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # No hay connect() en UDP, se envían datagramas directamente
        
        servidor_addr = (host, port)
        print(f"[CLIENTE UDP] Configurado para enviar a {host}:{port}")
        
        # Solicitar nombre de usuario
        print("Ingresa tu nombre de usuario: ", end='')
        nombre_usuario = input().strip()
        
        if not nombre_usuario:
            print("[CLIENTE UDP] Nombre de usuario no puede estar vacío")
            return
        
        # Enviar JOIN al servidor
        mensaje_join = f"JOIN:{nombre_usuario}"
        cliente_socket.sendto(mensaje_join.encode('utf-8'), servidor_addr)
        
        conectado = True
        
        # Iniciar hilo para recibir mensajes
        hilo_recepcion = threading.Thread(
            target=recibir_mensajes,
            args=(cliente_socket,),
            daemon=True
        )
        hilo_recepcion.start()
        
        # Esperar un momento para recibir bienvenida
        import time
        time.sleep(0.3)
        
        print("\n" + "=" * 60)
        print("[CLIENTE UDP] Conectado al chat!")
        print("[CLIENTE UDP] Escribe mensajes y presiona Enter")
        print("[CLIENTE UDP] Comandos: /listar, /quitar")
        print("=" * 60 + "\n")
        
        # Loop principal para enviar mensajes
        try:
            while conectado:
                mensaje = input()
                
                if not mensaje.strip():
                    continue
                
                # Procesar comandos
                if mensaje == '/quitar':
                    cliente_socket.sendto('QUIT'.encode('utf-8'), servidor_addr)
                    time.sleep(0.2)
                    conectado = False
                    break
                
                elif mensaje == '/listar':
                    cliente_socket.sendto('LIST'.encode('utf-8'), servidor_addr)
                
                else:
                    # Enviar mensaje normal
                    cliente_socket.sendto(mensaje.encode('utf-8'), servidor_addr)
        
        except KeyboardInterrupt:
            print("\n[CLIENTE UDP] Desconectando...")
            cliente_socket.sendto('QUIT'.encode('utf-8'), servidor_addr)
        
        finally:
            conectado = False
            cliente_socket.close()
            print("[CLIENTE UDP] Desconectado")
    
    except Exception as e:
        print(f"[CLIENTE UDP] Error: {e}")


if __name__ == "__main__":
    iniciar_cliente()