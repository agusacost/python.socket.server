import socketio
import threading
import sys

# Crear cliente SocketIO
sio = socketio.Client()

nombre_usuario = ""
conectado = False


def mostrar_banner():
    """Muestra el banner de inicio"""
    print("\n" + "=" * 60)
    print("    CLIENTE PYTHON - CHAT WEB")
    print("    Conectando al servidor Flask-SocketIO")
    print("=" * 60 + "\n")


# ==================== EVENTOS DE SOCKETIO ====================

@sio.event
def connect():
    """Evento: Conexión establecida"""
    global conectado
    conectado = True
    print("[CLIENTE] ✓ Conectado al servidor web")
    print(f"[CLIENTE] Socket ID: {sio.sid}\n")


@sio.event
def disconnect():
    """Evento: Desconexión"""
    global conectado
    conectado = False
    print("\n[CLIENTE] Desconectado del servidor")


@sio.on('joined')
def on_joined(data):
    """Evento: Confirmación de unión al chat"""
    print(f"[SISTEMA] ¡Bienvenido al chat, {data['username']}!")
    print("\n" + "=" * 60)
    print("📝 Escribe tus mensajes y presiona Enter")
    print("   Comandos: /listar (usuarios) | /quitar (salir)")
    print("=" * 60 + "\n")


@sio.on('message')
def on_message(data):
    """Evento: Mensaje recibido"""
    username = data['username']
    message = data['message']
    timestamp = data['timestamp']
    
    # Extraer solo hora:minutos del timestamp
    time = timestamp.split('T')[1][:5] if 'T' in timestamp else timestamp[:5]
    
    # Mostrar mensaje
    print(f"[{time}] {username}: {message}")


@sio.on('user_joined')
def on_user_joined(data):
    """Evento: Nuevo usuario se unió"""
    print(f"[SISTEMA] *** {data['username']} se unió al chat ***")


@sio.on('user_left')
def on_user_left(data):
    """Evento: Usuario se desconectó"""
    print(f"[SISTEMA] *** {data['username']} abandonó el chat ***")


@sio.on('user_list')
def on_user_list(users):
    """Evento: Lista de usuarios conectados"""
    print("\n--- USUARIOS CONECTADOS ({}) ---".format(len(users)))
    for i, user in enumerate(users, 1):
        print(f"{i}. {user['username']}")
    print("--------------------------------\n")


@sio.on('error')
def on_error(data):
    """Evento: Error del servidor"""
    print(f"[ERROR] {data.get('message', 'Error desconocido')}")


# ==================== FUNCIONES PRINCIPALES ====================

def conectar_servidor(host='localhost', port=5001):
    """
    Conecta al servidor web
    
    Args:
        host (str): Dirección del servidor
        port (int): Puerto del servidor
    """
    try:
        url = f'http://{host}:{port}'
        print(f"[CLIENTE] Conectando a {url}...")
        sio.connect(url)
        return True
    except Exception as e:
        print(f"[CLIENTE] Error al conectar: {e}")
        print("[CLIENTE] Verifica que el servidor esté ejecutándose")
        return False


def unirse_chat():
    """
    Solicita el nombre de usuario y se une al chat
    """
    global nombre_usuario
    
    print("Ingresa tu nombre de usuario: ", end='')
    nombre_usuario = input().strip()
    
    if not nombre_usuario:
        print("[CLIENTE] El nombre no puede estar vacío")
        return False
    
    # Enviar evento 'join' al servidor
    sio.emit('join', {'username': nombre_usuario})
    return True


def enviar_mensaje(mensaje):
    """
    Envía un mensaje al servidor
    
    Args:
        mensaje (str): Texto del mensaje
    """
    if not conectado:
        print("[CLIENTE] No estás conectado al servidor")
        return
    
    # Procesar comandos especiales
    if mensaje == '/listar':
        sio.emit('request_user_list')
        return
    
    if mensaje == '/quitar':
        print("[CLIENTE] Desconectando del chat...")
        sio.disconnect()
        sys.exit(0)
    
    # Enviar mensaje normal
    sio.emit('message', {'message': mensaje})


def loop_mensajes():
    """
    Loop principal para leer y enviar mensajes
    """
    try:
        while conectado:
            mensaje = input()
            
            if mensaje.strip():
                enviar_mensaje(mensaje)
    
    except KeyboardInterrupt:
        print("\n[CLIENTE] Cerrando...")
        sio.disconnect()
    
    except EOFError:
        print("\n[CLIENTE] Cerrando...")
        sio.disconnect()


# ==================== FUNCIÓN PRINCIPAL ====================

def main():
    """
    Función principal del cliente
    """
    # Mostrar banner
    mostrar_banner()
    
    # Obtener host y puerto de argumentos (opcional)
    host = 'localhost'
    port = 5001
    
    if len(sys.argv) == 3:
        host = sys.argv[1]
        try:
            port = int(sys.argv[2])
        except ValueError:
            print("Error: El puerto debe ser un número")
            sys.exit(1)
    
    # Conectar al servidor
    if not conectar_servidor(host, port):
        sys.exit(1)
    
    # Esperar un momento para que se establezca la conexión
    import time
    time.sleep(0.5)
    
    # Unirse al chat
    if not unirse_chat():
        sio.disconnect()
        sys.exit(1)
    
    # Esperar confirmación
    time.sleep(0.5)
    
    # Loop de mensajes
    loop_mensajes()


if __name__ == "__main__":
    main()