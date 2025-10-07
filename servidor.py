"""
===========================================
SERVIDOR WEB DE CHAT - PYTHON CON FLASK Y SOCKETIO
===========================================

Archivo: servidor_web.py

INSTRUCCIONES:
1. pip install flask flask-socketio
2. Crear carpeta: mkdir templates static
3. Guardar index.html en templates/
4. Guardar chat.js en static/
5. Ejecutar: python3 servidor_web.py
6. Abrir: http://localhost:5001
"""

from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from datetime import datetime

# Crear aplicación Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = 'clave_secreta_chat'

# Inicializar SocketIO
socketio = SocketIO(app, cors_allowed_origins="*")

# Diccionario para almacenar usuarios conectados
usuarios_conectados = {}

print("=" * 60)
print("[SERVIDOR WEB] Servidor de Chat Web iniciado")
print("[SERVIDOR WEB] Framework: Flask + Flask-SocketIO")
print("[SERVIDOR WEB] Puerto: 5001")
print("=" * 60)


@app.route('/')
def index():
    """Renderiza la página principal del chat"""
    return render_template('index.html')


@socketio.on('connect')
def handle_connect():
    """Maneja la conexión de un cliente"""
    from flask import request
    print(f'[SERVIDOR WEB] Nueva conexión: {request.sid}')


@socketio.on('join')
def handle_join(data):
    """Maneja cuando un usuario se une al chat"""
    from flask import request
    session_id = request.sid
    username = data.get('username', '').strip()
    
    print(f'[SERVIDOR WEB] Solicitud de unión: {username} (ID: {session_id})')
    
    if not username:
        print('[SERVIDOR WEB] Error: Nombre vacío')
        emit('error', {'message': 'Nombre de usuario vacío'})
        return
    
    usuarios_conectados[session_id] = username
    print(f'[SERVIDOR WEB] Usuario registrado: {username}')
    print(f'[SERVIDOR WEB] Total conectados: {len(usuarios_conectados)}')
    
    # Confirmar unión
    emit('joined', {
        'username': username,
        'session_id': session_id
    })
    
    # Enviar lista de usuarios a todos
    user_list = [
        {'username': user, 'session_id': sid}
        for sid, user in usuarios_conectados.items()
    ]
    emit('user_list', user_list, broadcast=True)
    
    # Notificar a otros usuarios
    emit('user_joined', {
        'username': username,
        'timestamp': datetime.now().isoformat()
    }, broadcast=True, include_self=False)


@socketio.on('message')
def handle_message(data):
    """Maneja mensajes de los clientes"""
    from flask import request
    session_id = request.sid
    
    if session_id not in usuarios_conectados:
        emit('error', {'message': 'Debes unirte primero'})
        return
    
    username = usuarios_conectados[session_id]
    message = data.get('message', '').strip()
    
    if not message:
        return
    
    print(f'[SERVIDOR WEB] {username}: {message}')
    
    # Retransmitir a todos
    emit('message', {
        'username': username,
        'message': message,
        'timestamp': datetime.now().isoformat(),
        'session_id': session_id
    }, broadcast=True)


@socketio.on('request_user_list')
def handle_request_user_list():
    """Envía la lista de usuarios"""
    user_list = [
        {'username': user, 'session_id': sid}
        for sid, user in usuarios_conectados.items()
    ]
    emit('user_list', user_list)


@socketio.on('disconnect')
def handle_disconnect():
    """Maneja desconexión de clientes"""
    from flask import request
    session_id = request.sid
    
    if session_id in usuarios_conectados:
        username = usuarios_conectados[session_id]
        del usuarios_conectados[session_id]
        
        print(f'[SERVIDOR WEB] Desconectado: {username}')
        print(f'[SERVIDOR WEB] Total conectados: {len(usuarios_conectados)}')
        
        # Notificar a todos
        emit('user_left', {
            'username': username,
            'timestamp': datetime.now().isoformat()
        }, broadcast=True)
        
        # Actualizar lista de usuarios
        user_list = [
            {'username': user, 'session_id': sid}
            for sid, user in usuarios_conectados.items()
        ]
        emit('user_list', user_list, broadcast=True)


if __name__ == '__main__':
    print('\n[SERVIDOR WEB] Iniciando servidor...')
    print('[SERVIDOR WEB] URL: http://localhost:5001')
    print('[SERVIDOR WEB] Presiona Ctrl+C para detener\n')
    
    socketio.run(app, host='0.0.0.0', port=5001, debug=False, allow_unsafe_werkzeug=True)