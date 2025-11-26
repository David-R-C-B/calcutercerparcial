import json
import os
import bcrypt
import pyotp

class AuthManager:
    DATA_FILE = "data/users.json"

    def __init__(self):
        self._ensure_data_file()

    def _ensure_data_file(self):
        if not os.path.exists("data"):
            os.makedirs("data")
        if not os.path.exists(self.DATA_FILE):
            with open(self.DATA_FILE, "w") as f:
                json.dump({}, f)

    def _load_users(self):
        with open(self.DATA_FILE, "r") as f:
            return json.load(f)

    def _save_users(self, users):
        with open(self.DATA_FILE, "w") as f:
            json.dump(users, f, indent=4)

    def user_exists(self, username):
        users = self._load_users()
        return username in users

    def has_users(self):
        users = self._load_users()
        return len(users) > 0

    def register_user(self, username, password):
        if self.user_exists(username):
            raise ValueError("El usuario ya existe.")

        # Hash password
        hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        # Generate TOTP secret
        totp_secret = pyotp.random_base32()

        users = self._load_users()
        users[username] = {
            "password": hashed_pw,
            "totp_secret": totp_secret
        }
        self._save_users(users)

        # Generate Provisioning URI for QR Code
        totp_uri = pyotp.totp.TOTP(totp_secret).provisioning_uri(name=username, issuer_name="CalculadoraSimulacion")
        return totp_uri, totp_secret

    def verify_login(self, username, password, totp_code):
        users = self._load_users()
        if username not in users:
            return False, "Usuario no encontrado."

        user_data = users[username]
        stored_hash = user_data["password"].encode('utf-8')

        # Verify password
        if not bcrypt.checkpw(password.encode('utf-8'), stored_hash):
            return False, "Contraseña incorrecta."

        # Verify TOTP
        totp_secret = user_data["totp_secret"]
        totp = pyotp.TOTP(totp_secret)
        if not totp.verify(totp_code):
            return False, "Código 2FA inválido."

        return True, "Login exitoso."

    def get_user_theme(self, username):
        users = self._load_users()
        if username in users:
            return users[username].get("theme", "blue")
        return "blue"

    def set_user_theme(self, username, theme):
        users = self._load_users()
        if username in users:
            users[username]["theme"] = theme
            self._save_users(users)
            return True
        return False
