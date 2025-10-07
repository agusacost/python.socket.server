// chat.js - Cliente de Chat Web

console.log("[CLIENTE WEB] Iniciando aplicación de chat");

// Conectar a Socket.IO
const socket = io();

let currentUsername = "";
let currentSessionId = "";

// Elementos del DOM
const loginPanel = document.getElementById("loginPanel");
const chatPanel = document.getElementById("chatPanel");
const usernameInput = document.getElementById("usernameInput");
const joinBtn = document.getElementById("joinBtn");
const messageInput = document.getElementById("messageInput");
const sendBtn = document.getElementById("sendBtn");
const messagesDiv = document.getElementById("messages");
const currentUserSpan = document.getElementById("currentUser");
const userCount = document.getElementById("userCount");
const quitBtn = document.getElementById("quitBtn");
const statusDiv = document.getElementById("status");

// Evento: Conexión establecida
socket.on("connect", function () {
  console.log("[CLIENTE WEB] Conectado al servidor");
  console.log("[CLIENTE WEB] Socket ID:", socket.id);
  showStatus("Conectado al servidor", "success");
});

// Unirse al chat
joinBtn.addEventListener("click", function () {
  const username = usernameInput.value.trim();
  console.log("[CLIENTE WEB] Botón presionado. Usuario:", username);

  if (username) {
    currentUsername = username;
    console.log("[CLIENTE WEB] Emitiendo evento join con:", username);
    socket.emit("join", { username: username });
  } else {
    console.log("[CLIENTE WEB] Error: Nombre vacío");
    showStatus("Por favor ingresa un nombre de usuario", "error");
  }
});

usernameInput.addEventListener("keypress", function (e) {
  if (e.key === "Enter") {
    joinBtn.click();
  }
});

// Evento: Unión exitosa
socket.on("joined", function (data) {
  console.log("[CLIENTE WEB] Evento joined recibido:", data);
  currentSessionId = data.session_id;

  loginPanel.style.display = "none";
  chatPanel.classList.add("active");
  currentUserSpan.textContent = data.username;
  messageInput.disabled = false;
  sendBtn.disabled = false;
  messageInput.focus();

  addSystemMessage("¡Bienvenido al chat, " + data.username + "!");
  console.log("[CLIENTE WEB] Chat activado correctamente");
});

// Enviar mensaje
function sendMessage() {
  const message = messageInput.value.trim();
  if (message) {
    if (message === "/listar") {
      socket.emit("request_user_list");
      messageInput.value = "";
      return;
    }

    if (message === "/quitar") {
      quitChat();
      return;
    }

    console.log("[CLIENTE WEB] Enviando:", message);
    socket.emit("message", { message: message });
    messageInput.value = "";
  }
}

sendBtn.addEventListener("click", sendMessage);

messageInput.addEventListener("keypress", function (e) {
  if (e.key === "Enter") {
    sendMessage();
  }
});

// Recibir mensaje
socket.on("message", function (data) {
  console.log("[CLIENTE WEB] Mensaje de", data.username + ":", data.message);
  addMessage(data);
});

// Lista de usuarios
socket.on("user_list", function (users) {
  console.log("[CLIENTE WEB] Usuarios:", users);
  userCount.textContent = users.length;

  let lista = "\n👥 USUARIOS CONECTADOS:\n";
  for (let i = 0; i < users.length; i++) {
    lista += i + 1 + ". " + users[i].username + "\n";
  }
  addSystemMessage(lista);
});

// Usuario se unió
socket.on("user_joined", function (data) {
  addSystemMessage(data.username + " se unió al chat");
});

// Usuario se fue
socket.on("user_left", function (data) {
  addSystemMessage(data.username + " abandonó el chat");
});

// Funciones auxiliares
function addMessage(data) {
  const messageDiv = document.createElement("div");
  messageDiv.className = "message user";

  if (data.session_id === currentSessionId) {
    messageDiv.classList.add("own");
  }

  const time = new Date(data.timestamp).toLocaleTimeString("es-AR", {
    hour: "2-digit",
    minute: "2-digit",
  });

  messageDiv.innerHTML =
    '<div class="message-header">' +
    '<span class="username">' +
    escapeHtml(data.username) +
    "</span>" +
    '<span class="timestamp">' +
    time +
    "</span>" +
    "</div>" +
    '<div class="message-text">' +
    escapeHtml(data.message) +
    "</div>";

  messagesDiv.appendChild(messageDiv);
  messagesDiv.scrollTop = messagesDiv.scrollHeight;
}

function addSystemMessage(text) {
  const messageDiv = document.createElement("div");
  messageDiv.className = "message system";
  messageDiv.textContent = text;
  messagesDiv.appendChild(messageDiv);
  messagesDiv.scrollTop = messagesDiv.scrollHeight;
}

function quitChat() {
  socket.disconnect();
  location.reload();
}

quitBtn.addEventListener("click", quitChat);

function showStatus(message, type) {
  statusDiv.textContent = message;
  statusDiv.className = "status show" + (type === "error" ? " error" : "");
  setTimeout(function () {
    statusDiv.classList.remove("show");
  }, 3000);
}

function escapeHtml(text) {
  const div = document.createElement("div");
  div.textContent = text;
  return div.innerHTML;
}

socket.on("error", function (error) {
  console.error("[CLIENTE WEB] Error:", error);
  showStatus(error.message || "Error desconocido", "error");
});

socket.on("disconnect", function () {
  console.log("[CLIENTE WEB] Desconectado");
  showStatus("Desconectado del servidor", "error");
});

socket.on("connect_error", function (error) {
  console.error("[CLIENTE WEB] Error de conexión:", error);
  showStatus("Error al conectar con el servidor", "error");
});
