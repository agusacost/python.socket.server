# 💬 Aplicación de Chat en Tiempo Real con Python

## 📖 Descripción del Proyecto

Este proyecto implementa una aplicación de chat en tiempo real utilizando Python y sockets. Permite la comunicación simultánea entre múltiples usuarios a través de una red local o Internet. El proyecto incluye dos versiones:

1. **Versión Consola**: Chat mediante terminal usando sockets TCP/IP tradicionales
2. **Versión Web**: Chat mediante navegador usando WebSockets (Flask + SocketIO)

---

## 🎯 Objetivos del Trabajo Práctico

✅ Diseñar y desarrollar una aplicación de chat en red usando sockets  
✅ Permitir comunicación en tiempo real entre varios usuarios  
✅ Implementar interfaz de usuario (consola y web)  
✅ Utilizar sockets para establecer conexión cliente-servidor  
✅ Retransmitir mensajes de un cliente a todos los demás  
✅ Manejar conexiones y desconexiones de clientes  
✅ Implementar comandos especiales (`/listar`, `/quitar`)  
✅ Documentar el código con comentarios explicativos  

---

## 🔌 ¿Qué son los Sockets y cómo funcionan?

### Definición

Un **socket** es un punto final de comunicación bidireccional entre dos programas que se ejecutan en una red. Funcionan como "enchufes" virtuales que permiten que dos aplicaciones se conecten y se comuniquen.

### Analogía

Imagina los sockets como **enchufes de teléfono**:
- El **servidor** es como una central telefónica que espera llamadas
- Los **clientes** son como teléfonos que llaman a la central
- Una vez conectados, pueden hablar en ambas direcciones

### Tipos de Sockets Utilizados

#### 1. **TCP/IP Sockets (Versión Consola)**
```
Características:
- Protocolo orientado a conexión
- Garantiza la entrega de datos en orden
- Más confiable pero ligeramente más lento
- Usa TCP (Transmission Control Protocol)
```

#### 2. **WebSockets (Versión Web)**
```
Características:
- Comunicación bidireccional sobre HTTP
- Diseñado específicamente para aplicaciones web
- Mantiene conexión abierta (full-duplex)
- Compatible con navegadores modernos
```

### Funcionamiento de Sockets en este Proyecto

```
┌─────────────┐                          ┌─────────────┐
│  CLIENTE 1  │                          │  CLIENTE 2  │
└──────┬──────┘                          └──────┬──────┘
       │                                        │
       │ 1. socket.connect()                    │
       │────────────┐                           │
       │            ▼                           │
       │      ┌──────────────┐                  │
       │      │   SERVIDOR   │◄─────────────────┤
       │      │  socket.bind │   2. connect()   │
       │      │  socket.listen                  │
       │      └──────┬───────┘                  │
       │             │                          │
       │ 3. send("Hola")                        │
       │────────────►│                          │
       │             │ 4. broadcast()           │
       │             ├─────────────────────────►│
       │             │         5. recv()        │
       │◄────────────┤                          │
       │  6. recv()  │                          │
```

### Pasos de Comunicación con Sockets

#### **En el Servidor:**
1. **Crear socket**: `socket.socket(socket.AF_INET, socket.SOCK_STREAM)`
2. **Vincular a puerto**: `socket.bind((HOST, PORT))`
3. **Escuchar conexiones**: `socket.listen()`
4. **Aceptar clientes**: `socket.accept()`
5. **Recibir datos**: `socket.recv()`
6. **Enviar datos**: `socket.send()`

#### **En el Cliente:**
1. **Crear socket**: `socket.socket(socket.AF_INET, socket.SOCK_STREAM)`
2. **Conectar al servidor**: `socket.connect((HOST, PORT))`
3. **Enviar datos**: `socket.send()`
4. **Recibir datos**: `socket.recv()`

---

## 📁 Estructura del Proyecto

```
chat-proyecto/
│
├── README.md                    # Este archivo
├── requirements.txt             # Dependencias de Python
│
├── Versión Consola/
│   ├── servidor.py             # Servidor de chat por consola
│   └── cliente.py              # Cliente de chat por consola
│
└── Versión Web/
    ├── servidor_web.py         # Servidor web con Flask
    ├── templates/
    │   └── index.html          # Interfaz HTML del chat
    └── static/
        └── chat.js             # Lógica JavaScript del cliente
```

---

## 🚀 Instalación y Configuración

### Requisitos Previos

- **Python 3.6+** instalado
- **pip** (gestor de paquetes de Python)
- **Conexión a red** (local o Internet)

### Instalación de Dependencias

```bash
# Para la versión consola (sin dependencias externas)
# Solo se usa Python estándar

# Para la versión web
pip install flask flask-socketio
```

O usando el archivo requirements.txt:

```bash
pip install -r requirements.txt
```

---

## 🖥️ Versión 1: Chat por Consola

### Características

- Sin dependencias externas (solo Python estándar)
- Usa sockets TCP/IP tradicionales
- Interfaz por terminal
- Threading para múltiples clientes

### Librerías Utilizadas

```python
import socket      # Comunicación en red TCP/IP
import threading   # Manejo de múltiples clientes simultáneos
from datetime import datetime  # Timestamps en mensajes
```

### Cómo Ejecutar

#### 1. Iniciar el Servidor

```bash
cd "Versión Consola"
python3 servidor.py
```

**Salida esperada:**
```
============================================================
[SERVIDOR] Servidor de Chat iniciado
[SERVIDOR] Escuchando en 0.0.0.0:5555
[SERVIDOR] Biblioteca: socket (TCP/IP)
[SERVIDOR] Esperando conexiones de clientes...
============================================================
```

#### 2. Conectar Clientes

**En la misma computadora:**
```bash
python3 cliente.py
```

**Desde otra computadora en la red:**
```bash
python3 cliente.py 192.168.1.100 5555
```
*(Reemplaza 192.168.1.100 con la IP del servidor)*

#### 3. Usar el Chat

1. Ingresa tu nombre de usuario cuando se solicite
2. Escribe mensajes y presiona Enter para enviar
3. Usa comandos:
   - `/listar` - Ver usuarios conectados
   - `/quitar` - Salir del chat

### Funcionamiento Técnico - Versión Consola

#### **servidor.py**

```python
# 1. CREAR SOCKET DEL SERVIDOR
servidor_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# AF_INET = IPv4, SOCK_STREAM = TCP

# 2. VINCULAR A UN PUERTO
servidor_socket.bind((HOST, PORT))
# HOST = '0.0.0.0' escucha en todas las interfaces
# PORT = 5555 puerto específico

# 3. ESCUCHAR CONEXIONES
servidor_socket.listen(5)
# Máximo 5 conexiones en cola

# 4. ACEPTAR CLIENTES (bucle infinito)
while True:
    cliente_socket, direccion = servidor_socket.accept()
    # Crear hilo para cada cliente
    threading.Thread(target=manejar_cliente, args=(cliente_socket,)).start()

# 5. RETRANSMITIR MENSAJES (función broadcast)
def broadcast(mensaje, excluir_cliente=None):
    for cliente in clientes.keys():
        if cliente != excluir_cliente:
            cliente.send(mensaje.encode('utf-8'))
```

#### **cliente.py**

```python
# 1. CREAR SOCKET DEL CLIENTE
cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 2. CONECTAR AL SERVIDOR
cliente_socket.connect((HOST, PORT))

# 3. CREAR HILO PARA RECIBIR MENSAJES
threading.Thread(target=recibir_mensajes, daemon=True).start()

# 4. ENVIAR MENSAJES
while True:
    mensaje = input()
    cliente_socket.send(mensaje.encode('utf-8'))
```

### Puertos Utilizados - Versión Consola

- **Puerto TCP 5555** (configurable en las variables HOST y PORT)

---

## 🌐 Versión 2: Chat Web

### Características

- Interfaz gráfica moderna (HTML/CSS)
- Usa WebSockets para comunicación en tiempo real
- Accesible desde cualquier navegador
- No requiere instalación en el cliente

### Librerías Utilizadas

```python
from flask import Flask, render_template  # Framework web
from flask_socketio import SocketIO, emit # WebSockets
from datetime import datetime             # Timestamps
```

### Cómo Ejecutar

#### 1. Preparar la Estructura

```bash
cd "Versión Web"

# Crear carpetas necesarias
mkdir templates
mkdir static
```

#### 2. Colocar los Archivos

```
Versión Web/
├── servidor_web.py
├── templates/
│   └── index.html
└── static/
    └── chat.js
```

#### 3. Iniciar el Servidor

```bash
python3 servidor_web.py
```

**Salida esperada:**
```
============================================================
[SERVIDOR WEB] Servidor de Chat Web iniciado
[SERVIDOR WEB] Framework: Flask + Flask-SocketIO
[SERVIDOR WEB] Puerto: 5001
============================================================

[SERVIDOR WEB] Iniciando servidor...
[SERVIDOR WEB] URL: http://localhost:5001
```

#### 4. Abrir en el Navegador

- **En la misma computadora**: `http://localhost:5001`
- **Desde otra computadora**: `http://IP-DEL-SERVIDOR:5001`

#### 5. Usar el Chat

1. Ingresa tu nombre de usuario
2. Haz clic en "Unirse al Chat"
3. Escribe mensajes en el campo de texto
4. Usa los comandos `/listar` o `/quitar`

### Funcionamiento Técnico - Versión Web

#### **servidor_web.py**

```python
# 1. CREAR APLICACIÓN FLASK
app = Flask(__name__)
socketio = SocketIO(app)

# 2. RUTA PARA SERVIR HTML
@app.route('/')
def index():
    return render_template('index.html')

# 3. MANEJAR EVENTO: USUARIO SE UNE
@socketio.on('join')
def handle_join(data):
    username = data['username']
    usuarios_conectados[request.sid] = username
    
    # Confirmar al usuario
    emit('joined', {'username': username})
    
    # Notificar a todos
    emit('user_joined', {'username': username}, broadcast=True)

# 4. MANEJAR EVENTO: MENSAJE
@socketio.on('message')
def handle_message(data):
    # Retransmitir a todos
    emit('message', {
        'username': usuarios_conectados[request.sid],
        'message': data['message']
    }, broadcast=True)

# 5. INICIAR SERVIDOR
socketio.run(app, host='0.0.0.0', port=5001)
```

#### **chat.js (Cliente)**

```javascript
// 1. CONECTAR AL SERVIDOR
const socket = io();

// 2. ENVIAR EVENTO: UNIRSE
socket.emit('join', { username: 'Juan' });

// 3. RECIBIR EVENTO: CONFIRMACIÓN
socket.on('joined', function(data) {
    // Mostrar panel de chat
    chatPanel.classList.add('active');
});

// 4. ENVIAR MENSAJE
socket.emit('message', { message: 'Hola a todos' });

// 5. RECIBIR MENSAJES
socket.on('message', function(data) {
    // Mostrar mensaje en pantalla
    addMessage(data);
});
```

### Puertos Utilizados - Versión Web

- **Puerto TCP 5001** (HTTP + WebSocket)

---

## 📊 Comparación de Versiones

| Característica | Versión Consola | Versión Web |
|----------------|-----------------|-------------|
| **Interfaz** | Terminal/CMD | Navegador web |
| **Tecnología** | Sockets TCP/IP | WebSockets |
| **Dependencias** | Ninguna (Python estándar) | Flask, Flask-SocketIO |
| **Instalación Cliente** | Python requerido | Solo navegador |
| **Acceso Móvil** | ❌ No | ✅ Sí |
| **Facilidad de Uso** | Media | Alta |
| **Ideal para** | Entender sockets básicos | Aplicación real |

---

## 🎯 Comandos Disponibles en el Chat

| Comando | Descripción | Ejemplo |
|---------|-------------|---------|
| `/listar` | Muestra lista de usuarios conectados | `/listar` |
| `/quitar` | Desconecta del chat y cierra la aplicación | `/quitar` |

---

## 📝 Explicación de Eventos Socket

### Versión Consola (TCP/IP)

No usa eventos nombrados. La comunicación es directa:
- `socket.send()` - Envía bytes
- `socket.recv()` - Recibe bytes

### Versión Web (WebSockets)

Usa eventos nombrados para comunicación estructurada:

| Evento | Dirección | Datos | Descripción |
|--------|-----------|-------|-------------|
| `connect` | Automático | - | Cliente conecta al servidor |
| `join` | Cliente → Servidor | `{username}` | Usuario se registra |
| `joined` | Servidor → Cliente | `{username, session_id}` | Confirmación de registro |
| `message` | Cliente → Servidor | `{message}` | Enviar mensaje |
| `message` | Servidor → Todos | `{username, message, timestamp}` | Retransmitir mensaje |
| `user_joined` | Servidor → Todos | `{username}` | Notificar nueva unión |
| `user_left` | Servidor → Todos | `{username}` | Notificar desconexión |
| `request_user_list` | Cliente → Servidor | - | Solicitar lista |
| `user_list` | Servidor → Cliente | `[{username}]` | Enviar lista |
| `disconnect` | Automático | - | Cliente se desconecta |

---

## 🐛 Solución de Problemas

### Error: "Address already in use"

**Problema:** El puerto ya está ocupado.

**Solución:**
```bash
# Ver qué usa el puerto
sudo lsof -i :5555  # Para consola
sudo lsof -i :5001  # Para web

# Matar proceso
kill -9 <PID>

# O cambiar puerto en el código
PORT = 5556  # Usar otro puerto
```

### Error: "Connection refused"

**Problema:** El servidor no está ejecutándose.

**Solución:** Asegúrate de iniciar el servidor antes de conectar clientes.

### Error: "Module not found"

**Problema:** Faltan dependencias.

**Solución:**
```bash
pip3 install flask flask-socketio
```

### No puedo conectar desde otra PC

**Problema:** Firewall o configuración de red.

**Solución:**
```bash
# Verificar IP del servidor
ip addr show  # Linux
ipconfig      # Windows

# Abrir puerto en firewall
sudo ufw allow 5555  # Consola
sudo ufw allow 5001  # Web
```

---

## 📚 Conceptos Técnicos Clave

### 1. **Socket**
Punto final de comunicación bidireccional entre dos programas en una red.

### 2. **TCP/IP**
Protocolo de comunicación confiable y orientado a conexión.

### 3. **WebSocket**
Protocolo de comunicación full-duplex sobre una conexión TCP.

### 4. **Threading**
Técnica para ejecutar múltiples operaciones simultáneamente.

### 5. **Broadcast**
Enviar un mensaje a todos los clientes conectados.

### 6. **Session ID**
Identificador único asignado a cada cliente conectado.

### 7. **Port (Puerto)**
Número que identifica un proceso o servicio específico en una computadora.

---

## 📈 Flujo de Datos Completo

```
USUARIO 1                SERVIDOR                 USUARIO 2
   │                        │                        │
   │  1. Conectar           │                        │
   ├───────────────────────►│                        │
   │                        │  2. Aceptar conexión   │
   │                        ├───────────────────────►│
   │                        │                        │
   │  3. Enviar nombre      │                        │
   ├───────────────────────►│                        │
   │                        │  4. Notificar unión    │
   │                        ├───────────────────────►│
   │                        │                        │
   │  5. Enviar mensaje     │                        │
   ├───────────────────────►│                        │
   │                        │  6. Retransmitir       │
   ├────────────────────────┤───────────────────────►│
   │  7. Recibir mensaje    │  8. Recibir mensaje    │
   │                        │                        │
```

---

## 🏆 Ventajas de Este Proyecto

✅ **Educativo**: Aprende sockets desde lo básico  
✅ **Práctico**: Aplicación funcional y útil  
✅ **Escalable**: Fácil de extender con más funciones  
✅ **Documentado**: Código con comentarios explicativos  
✅ **Multiplataforma**: Funciona en Windows, Linux, macOS  
✅ **Sin costos**: Solo requiere Python  

---

## 👥 Agustin Acosta

Proyecto desarrollado como trabajo práctico de redes y comunicaciones.

---
## 📞 Soporte

Para problemas o dudas:
1. Revisa la sección "Solución de Problemas"
2. Verifica los logs del servidor
3. Revisa la consola del navegador (F12) para versión web

---

## 🎓 Referencias

- [Documentación de Python Socket](https://docs.python.org/3/library/socket.html)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Flask-SocketIO Documentation](https://flask-socketio.readthedocs.io/)
- [Socket.IO Client](https://socket.io/docs/v4/client-api/)

---

**¡Gracias por usar esta aplicación de chat! 🚀**
