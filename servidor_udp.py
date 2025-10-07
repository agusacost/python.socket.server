import socket
from datetime import datetime

# Configuración
HOST = '0.0.0.0'
PORT = 5556

# Almacenar clientes: {(ip, puerto): nombre_usuario}
clientes = {}

print("=" * 60)
print("[SERVIDOR UDP] Servidor de Chat UDP iniciado")
print(f"[SERVIDOR UDP] Protocolo: UDP (sin conexión)")
print(f"[SERVIDOR UDP] Escuchando en puerto: {PORT}")
print("=" * 60 + "\n")


def broadcast(mensaje, excluir_direccion=None):
    """
    Envía mensaje a todos los clientes registrados
    
    Args:
        mensaje (str): Mensaje a enviar
        excluir_direccion (tuple): Dirección a excluir
    """
    for direccion in list(clientes.keys()):
        if direccion != excluir_direccion:
            try:
                servidor_socket.sendto(mensaje.encode('utf-8'), direccion)
            except:
                print(f"[SERVIDOR UDP] Error enviando a {direccion}")


def iniciar_servidor():
    """Inicia el servidor UDP"""
    global servidor_socket
    
    # Crear socket UDP
    servidor_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # AF_INET = IPv4, SOCK_DGRAM = UDP
    
    # Vincular a puerto
    servidor_socket.bind((HOST, PORT))
    
    print(f"[SERVIDOR UDP] Esperando datagramas en {HOST}:{PORT}...\n")
    
    try:
        while True:
            # Recibir datagrama (no hay conexión establecida)
            data, direccion = servidor_socket.recvfrom(1024)
            mensaje = data.decode('utf-8').strip()
            
            # Procesar mensaje
            if mensaje.startswith('JOIN:'):
                # Nuevo usuario
                nombre = mensaje.split(':', 1)[1]
                clientes[direccion] = nombre
                
                print(f"[SERVIDOR UDP] Usuario registrado: {nombre}")
                print(f"[SERVIDOR UDP] Dirección: {direccion[0]}:{direccion[1]}")
                print(f"[SERVIDOR UDP] Clientes conectados: {len(clientes)}\n")
                
                # Confirmar registro
                timestamp = datetime.now().strftime("%H:%M:%S")
                bienvenida = f"[{timestamp}] Bienvenido al chat UDP, {nombre}!\n"
                bienvenida += "Comandos: /listar, /quitar\n"
                servidor_socket.sendto(bienvenida.encode('utf-8'), direccion)
                
                # Notificar a todos
                notif = f"[{timestamp}] *** {nombre} se unió al chat (UDP) ***"
                broadcast(notif, excluir_direccion=direccion)
            
            elif mensaje == 'LIST':
                # Solicitud de lista de usuarios
                lista = f"\n--- USUARIOS CONECTADOS ({len(clientes)}) ---\n"
                for i, nombre in enumerate(clientes.values(), 1):
                    lista += f"{i}. {nombre}\n"
                lista += "--------------------------------\n"
                servidor_socket.sendto(lista.encode('utf-8'), direccion)
            
            elif mensaje == 'QUIT':
                # Usuario se desconecta
                if direccion in clientes:
                    nombre = clientes[direccion]
                    del clientes[direccion]
                    
                    print(f"[SERVIDOR UDP] Usuario desconectado: {nombre}")
                    print(f"[SERVIDOR UDP] Clientes conectados: {len(clientes)}\n")
                    
                    # Notificar a todos
                    timestamp = datetime.now().strftime("%H:%M:%S")
                    notif = f"[{timestamp}] *** {nombre} abandonó el chat ***"
                    broadcast(notif)
                    
                    # Confirmar desconexión
                    servidor_socket.sendto("Desconectado.\n".encode('utf-8'), direccion)
            
            else:
                # Mensaje normal
                if direccion in clientes:
                    nombre = clientes[direccion]
                    timestamp = datetime.now().strftime("%H:%M:%S")
                    
                    print(f"[SERVIDOR UDP] {nombre}: {mensaje}")
                    
                    # Broadcast del mensaje
                    msg_formateado = f"[{timestamp}] {nombre}: {mensaje}"
                    broadcast(msg_formateado)
    
    except KeyboardInterrupt:
        print("\n[SERVIDOR UDP] Cerrando servidor...")
    
    finally:
        servidor_socket.close()
        print("[SERVIDOR UDP] Servidor cerrado")


if __name__ == "__main__":
    iniciar_servidor()