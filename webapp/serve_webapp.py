from flask import Flask, send_from_directory, redirect, session, request, jsonify, render_template, send_file
from flask_socketio import SocketIO, emit, join_room, leave_room
import os
from datetime import datetime
import mysql.connector
from mysql.connector import Error
import bcrypt
from dotenv import load_dotenv
import logging
import time

# Configurar logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Carregar variáveis de ambiente
load_dotenv()

app = Flask(__name__, static_folder="static", template_folder="templates")
app.config['SECRET_KEY'] = 'furia_chat_secret_key'
socketio = SocketIO(app, cors_allowed_origins="*")

# Configurações do MySQL
MYSQL_CONFIG = {
    'host': os.getenv('MYSQL_HOST', 'mysql'),
    'user': os.getenv('MYSQL_USER', 'root'),
    'password': os.getenv('MYSQL_PASSWORD', '123456'),
    'database': os.getenv('MYSQL_DATABASE', 'furia_chat'),
    'port': 3306,
    'auth_plugin': 'mysql_native_password',
    'use_pure': True,
    'connect_timeout': 30,
    'retries': 3,
    'delay': 5
}

def get_db_connection():
    retries = MYSQL_CONFIG.pop('retries', 3)
    delay = MYSQL_CONFIG.pop('delay', 5)
    
    for attempt in range(retries):
        try:
            logger.debug(f"Tentativa {attempt + 1} de {retries} para conectar ao MySQL")
            logger.debug(f"Configuração: {MYSQL_CONFIG}")
            
            connection = mysql.connector.connect(**MYSQL_CONFIG)
            logger.debug("Conexão com MySQL estabelecida com sucesso")
            return connection
        except Error as e:
            logger.error(f"Erro ao conectar ao MySQL (tentativa {attempt + 1}): {e}")
            if attempt < retries - 1:
                logger.debug(f"Aguardando {delay} segundos antes da próxima tentativa...")
                time.sleep(delay)
            else:
                logger.error("Todas as tentativas de conexão falharam")
                return None

def init_db():
    try:
        connection = get_db_connection()
        if connection:
            cursor = connection.cursor()
            logger.debug("Inicializando banco de dados...")
            
            # Criar banco de dados se não existir
            cursor.execute("CREATE DATABASE IF NOT EXISTS furia_chat")
            cursor.execute("USE furia_chat")
            
            # Criar tabelas
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    username VARCHAR(50) NOT NULL,
                    email VARCHAR(100) NOT NULL UNIQUE,
                    password VARCHAR(255) NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_login TIMESTAMP NULL,
                    is_active BOOLEAN DEFAULT TRUE
                )
            """)
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS chat_messages (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id INT NOT NULL,
                    message TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    room_id INT DEFAULT 1,
                    FOREIGN KEY (user_id) REFERENCES users(id)
                )
            """)
            
            connection.commit()
            logger.debug("Banco de dados inicializado com sucesso")
            
            cursor.close()
            connection.close()
    except Error as e:
        logger.error(f"Erro ao inicializar banco de dados: {e}")

def encrypt_password(password):
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode(), salt).decode()

def verify_password(hashed_password, password):
    try:
        # O hash no banco de dados já inclui o salt, então não precisamos gerar um novo
        return bcrypt.checkpw(password.encode(), hashed_password.encode())
    except Exception as e:
        logger.error(f"Erro ao verificar senha: {e}")
        logger.error(f"Hash da senha: {hashed_password}")
        logger.error(f"Senha fornecida: {password}")
        return False

# Dicionário para armazenar usuários online
online_users = {}
# Dicionário para armazenar mensagens
chat_messages = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register')
def register():
    logger.debug("Acessando rota /register")
    return render_template('register.html')

@app.route('/feed')
def feed():
    logger.debug("Acessando rota /feed")
    return render_template('feed.html')

@app.route('/calendario')
def calendario():
    logger.debug("Acessando rota /calendario")
    return render_template('calendario.html')

@app.route('/chat')
def chat_page():
    logger.debug("Acessando rota /chat")
    try:
        return render_template("chat.html")
    except Exception as e:
        logger.error(f"Erro ao servir chat.html: {e}")
        return str(e), 500
    
@app.route("/api/update-status", methods=["POST"])
def update_status():
    data = request.get_json()
    user_email = data.get("email")
    status = data.get("status")

    if not user_email or status not in ["online", "offline"]:
        return jsonify({"error": "Dados inválidos"}), 400

    try:
        conn = get_db_connection()  # <-- Aqui
        if not conn:
            return jsonify({"error": "Erro ao conectar ao banco de dados"}), 500
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE users SET status = %s WHERE email = %s", (status, user_email)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"message": "Status atualizado com sucesso"})
    except Exception as e:
        app.logger.error(f"Erro ao atualizar status: {e}")
        return jsonify({"error": "Erro interno no servidor"}), 500

    
@app.route("/api/online-users", methods=["GET"])
def get_online_users():
    try:
        conn = get_db_connection()
        if not conn:
            return jsonify({"error": "Erro ao conectar ao banco de dados"}), 500
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT username FROM users WHERE status = 'online'")
        users = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(users)
    except Exception as e:
        app.logger.error(f"Erro ao obter usuários online: {e}")
        return jsonify({"error": "Erro ao obter usuários online"}), 500

@app.route('/api/register', methods=['POST'])
def register_api():
    try:
        data = request.get_json()
        logger.debug(f"Dados recebidos para registro: {data}")
        
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        
        if not all([username, email, password]):
            return jsonify({'error': 'Todos os campos são obrigatórios'}), 400
        
        connection = get_db_connection()
        if not connection:
            return jsonify({'error': 'Erro ao conectar ao banco de dados'}), 500
        
        try:
            cursor = connection.cursor()
            
            # Verificar se o e-mail já existe
            cursor.execute("SELECT id FROM users WHERE email = %s", (email,))
            if cursor.fetchone():
                return jsonify({'error': 'E-mail já cadastrado'}), 400
            
            # Criptografar a senha
            encrypted_password = encrypt_password(password)
            
            # Inserir novo usuário
            cursor.execute(
                "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)",
                (username, email, encrypted_password)
            )
            connection.commit()
            
            logger.debug(f"Usuário {username} registrado com sucesso")
            return jsonify({'message': 'Usuário registrado com sucesso'}), 201
            
        except Error as e:
            logger.error(f"Erro ao registrar usuário: {e}")
            return jsonify({'error': 'Erro ao registrar usuário'}), 500
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
    except Exception as e:
        logger.error(f"Erro inesperado no registro: {e}")
        return jsonify({'error': 'Erro interno do servidor'}), 500

@app.route('/api/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        logger.debug(f"Dados recebidos para login: {data}")
        
        email = data.get('email')
        password = data.get('password')
        
        if not all([email, password]):
            return jsonify({'error': 'E-mail e senha são obrigatórios'}), 400
        
        connection = get_db_connection()
        if not connection:
            return jsonify({'error': 'Erro ao conectar ao banco de dados'}), 500
        
        try:
            cursor = connection.cursor(dictionary=True)
            
            # MODIFIQUE A QUERY PARA INCLUIR O NOME COMPLETO
            cursor.execute("""
                SELECT id, username, password, email 
                FROM users 
                WHERE email = %s
            """, (email,))
            user = cursor.fetchone()
            
            if not user or not verify_password(user['password'], password):
                return jsonify({'error': 'E-mail ou senha inválidos'}), 401
            
            # Atualizar último login
            cursor.execute(
                "UPDATE users SET last_login = CURRENT_TIMESTAMP WHERE id = %s",
                (user['id'],)
            )
            connection.commit()
            
            # Armazenar informações do usuário na sessão
            session['user_id'] = user['id']
            session['username'] = user['username']
            
            logger.debug(f"Usuário {user['username']} fez login com sucesso")
            
            return jsonify({
                'message': 'Login bem-sucedido',
                'user': {
                    'id': user['id'],
                    'username': user['username'],
                    'email': user['email']
                }
            }), 200
            
        except Error as e:
            logger.error(f"Erro ao fazer login: {e}")
            return jsonify({'error': 'Erro ao fazer login'}), 500
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
    except Exception as e:
        logger.error(f"Erro inesperado no login: {e}")
        return jsonify({'error': 'Erro interno do servidor'}), 500

@socketio.on('connect')
def handle_connect():
    logger.debug('Cliente conectado')

@socketio.on('disconnect')
def handle_disconnect():
    user_id = session.get('user_id')
    if user_id in online_users:
        del online_users[user_id]
        emit('user_left', {'user_id': user_id}, broadcast=True)

@socketio.on('login')
def handle_login(data):
    username = data.get('username')
    user_id = session.get('user_id')
    
    if not user_id:
        return
    
    online_users[user_id] = {
        'username': username,
        'status': 'online'
    }
    
    emit('user_joined', {
        'user_id': user_id,
        'username': username
    }, broadcast=True)
    
    # Enviar lista de usuários online e histórico de mensagens
    emit('online_users', list(online_users.values()))
    emit('chat_history', chat_messages)

@socketio.on('send_message')
def handle_message(data):
    message = data.get('message')
    user_id = session.get('user_id')
    username = session.get('username')
    
    if message and user_id and username:
        message_data = {
            'user_id': user_id,
            'username': username,
            'message': message,
            'timestamp': datetime.now().strftime('%H:%M')
        }
        
        # Salvar mensagem no banco de dados
        connection = get_db_connection()
        if connection:
            try:
                cursor = connection.cursor()
                cursor.execute(
                    "INSERT INTO chat_messages (user_id, message) VALUES (%s, %s)",
                    (user_id, message)
                )
                connection.commit()
            except Error as e:
                logger.error(f"Erro ao salvar mensagem: {e}")
            finally:
                if connection.is_connected():
                    cursor.close()
                    connection.close()
        
        chat_messages.append(message_data)
        emit('new_message', message_data, broadcast=True)

if __name__ == '__main__':
    print("Starting Flask app...")
    print("Current directory:", os.getcwd())
    print("Files in current directory:", os.listdir("."))
    
    # Listar todas as rotas registradas
    print("\nRotas registradas:")
    for rule in app.url_map.iter_rules():
        print(f"Rota: {rule.rule}, Métodos: {rule.methods}")
    
    # Inicializar banco de dados
    init_db()
    
    socketio.run(app, host='0.0.0.0', port=8080, debug=True)

