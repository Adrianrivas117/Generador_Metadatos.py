import sys
import json
import hashlib
from PyQt5.QtWidgets import (QApplication, QDialog, QVBoxLayout, QHBoxLayout,
                             QLabel, QLineEdit, QPushButton, QMessageBox, QFrame)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt


class LoginDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.users_file = "users.json"
        self.init_ui()
        self.ensure_users_file()
        
    def init_ui(self):
        self.setWindowTitle("Login")
        self.setFixedSize(650, 750)
        self.setStyleSheet("""
            QDialog {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #667eea, stop:1 #764ba2);
            }
        """)
        
        # Layout principal
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(20)
        self.setLayout(main_layout)
        
        # Panel central
        panel = QFrame()
        panel.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 20px;
                padding: 30px;
            }
        """)
        panel_layout = QVBoxLayout()
        panel.setLayout(panel_layout)
        
        # Título
        title = QLabel("Iniciar Sesión")
        title.setFont(QFont("Segoe UI", 20, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: #667eea; margin-bottom: 10px; padding: 10px;")
        panel_layout.addWidget(title)
        
        subtitle = QLabel("Accede al generador de metadatos")
        subtitle.setFont(QFont("Segoe UI", 12))
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet("color: #888; margin-bottom: 25px; padding: 5px;")
        panel_layout.addWidget(subtitle)
        
        # Campo de usuario
        user_label = QLabel("👤 Usuario:")
        user_label.setFont(QFont("Segoe UI", 13, QFont.Bold))
        user_label.setStyleSheet("color: #444; margin-top: 15px; padding: 5px;")
        panel_layout.addWidget(user_label)
        
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Ingresa tu usuario")
        self.username_input.setFont(QFont("Segoe UI", 13))
        self.username_input.setStyleSheet("""
            QLineEdit {
                border: 2px solid #e0e0e0;
                border-radius: 10px;
                padding: 15px;
                background-color: #f8f9fa;
                color: #222;
                font-size: 13px;
            }
            QLineEdit:focus {
                border: 2px solid #667eea;
                background-color: white;
            }
        """)
        panel_layout.addWidget(self.username_input)
        
        # Campo de contraseña
        pass_label = QLabel("🔑 Contraseña:")
        pass_label.setFont(QFont("Segoe UI", 13, QFont.Bold))
        pass_label.setStyleSheet("color: #444; margin-top: 15px; padding: 5px;")
        panel_layout.addWidget(pass_label)
        
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Ingresa tu contraseña")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setFont(QFont("Segoe UI", 13))
        self.password_input.setStyleSheet("""
            QLineEdit {
                border: 2px solid #e0e0e0;
                border-radius: 10px;
                padding: 15px;
                background-color: #f8f9fa;
                color: #222;
                font-size: 13px;
            }
            QLineEdit:focus {
                border: 2px solid #667eea;
                background-color: white;
            }
        """)
        self.password_input.returnPressed.connect(self.login)
        panel_layout.addWidget(self.password_input)
        
        # Botón de login
        self.login_button = QPushButton("🚀 Iniciar Sesión")
        self.login_button.setFont(QFont("Segoe UI", 14, QFont.Bold))
        self.login_button.clicked.connect(self.login)
        self.login_button.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #667eea, stop:1 #764ba2);
                color: white;
                border: none;
                border-radius: 12px;
                padding: 18px;
                margin-top: 25px;
                font-size: 14px;
                font-weight: bold;
                min-height: 20px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #5568d3, stop:1 #6a3f8f);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #4a5abc, stop:1 #5c347c);
            }
        """)
        panel_layout.addWidget(self.login_button)
        
        # Botón de registro
        self.register_button = QPushButton("📝 Crear Cuenta")
        self.register_button.setFont(QFont("Segoe UI", 13))
        self.register_button.clicked.connect(self.register)
        self.register_button.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #667eea;
                border: 2px solid #667eea;
                border-radius: 12px;
                padding: 15px;
                margin-top: 12px;
                font-size: 13px;
                font-weight: bold;
                min-height: 20px;
            }
            QPushButton:hover {
                background-color: #f0f4ff;
                color: #5568d3;
            }
        """)
        panel_layout.addWidget(self.register_button)
        
        main_layout.addWidget(panel)
        
        # Info
        info_label = QLabel("ℹ️ Usuario por defecto: admin / admin123")
        info_label.setAlignment(Qt.AlignCenter)
        info_label.setFont(QFont("Segoe UI", 11))
        info_label.setStyleSheet("color: white; margin-top: 10px; padding: 5px;")
        main_layout.addWidget(info_label)
    
    def ensure_users_file(self):
        """Crea el archivo de usuarios si no existe"""
        if not os.path.exists(self.users_file):
            default_users = {
                "admin": {
                    "password": self.hash_password("admin123"),
                    "name": "Administrador",
                    "created_at": "2025-12-01"
                }
            }
            with open(self.users_file, 'w', encoding='utf-8') as f:
                json.dump(default_users, f, indent=4, ensure_ascii=False)
    
    def hash_password(self, password):
        """Hashea la contraseña con SHA256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def login(self):
        """Intenta iniciar sesión"""
        username = self.username_input.text().strip()
        password = self.password_input.text()
        
        if not username or not password:
            QMessageBox.warning(self, "Error", "Por favor completa todos los campos")
            return
        
        try:
            with open(self.users_file, 'r', encoding='utf-8') as f:
                users = json.load(f)
            
            if username in users:
                hashed_password = self.hash_password(password)
                if users[username]["password"] == hashed_password:
                    QMessageBox.information(
                        self, 
                        "✅ Éxito", 
                        f"Bienvenido, {users[username].get('name', username)}!"
                    )
                    self.accept()
                else:
                    QMessageBox.warning(self, "Error", "Contraseña incorrecta")
            else:
                QMessageBox.warning(self, "Error", "Usuario no encontrado")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al iniciar sesión: {e}")
    
    def register(self):
        """Abre el diálogo de registro"""
        dialog = RegisterDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            QMessageBox.information(
                self,
                "✅ Éxito",
                "Usuario registrado correctamente. Ya puedes iniciar sesión."
            )


class RegisterDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.users_file = "users.json"
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle("📝 Crear Cuenta")
        self.setFixedSize(400, 550)
        self.setStyleSheet("""
            QDialog {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #11998e, stop:1 #38ef7d);
            }
        """)
        
        # Layout principal
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(20)
        self.setLayout(main_layout)
        
        # Panel central
        panel = QFrame()
        panel.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 20px;
                padding: 30px;
            }
        """)
        panel_layout = QVBoxLayout()
        panel.setLayout(panel_layout)
        
        # Título
        title = QLabel("📝 Crear Nueva Cuenta")
        title.setFont(QFont("Segoe UI", 22, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: #11998e; margin-bottom: 20px;")
        panel_layout.addWidget(title)
        
        # Campo de nombre
        name_label = QLabel("👤 Nombre completo:")
        name_label.setFont(QFont("Segoe UI", 11, QFont.Bold))
        panel_layout.addWidget(name_label)
        
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Tu nombre")
        self.name_input.setStyleSheet(self.get_input_style())
        panel_layout.addWidget(self.name_input)
        
        # Campo de usuario
        user_label = QLabel("🔤 Usuario:")
        user_label.setFont(QFont("Segoe UI", 11, QFont.Bold))
        user_label.setStyleSheet("margin-top: 10px;")
        panel_layout.addWidget(user_label)
        
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Nombre de usuario")
        self.username_input.setStyleSheet(self.get_input_style())
        panel_layout.addWidget(self.username_input)
        
        # Campo de contraseña
        pass_label = QLabel("🔑 Contraseña:")
        pass_label.setFont(QFont("Segoe UI", 11, QFont.Bold))
        pass_label.setStyleSheet("margin-top: 10px;")
        panel_layout.addWidget(pass_label)
        
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Mínimo 6 caracteres")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setStyleSheet(self.get_input_style())
        panel_layout.addWidget(self.password_input)
        
        # Confirmar contraseña
        confirm_label = QLabel("🔐 Confirmar contraseña:")
        confirm_label.setFont(QFont("Segoe UI", 11, QFont.Bold))
        confirm_label.setStyleSheet("margin-top: 10px;")
        panel_layout.addWidget(confirm_label)
        
        self.confirm_input = QLineEdit()
        self.confirm_input.setPlaceholderText("Repite la contraseña")
        self.confirm_input.setEchoMode(QLineEdit.Password)
        self.confirm_input.setStyleSheet(self.get_input_style())
        panel_layout.addWidget(self.confirm_input)
        
        # Botones
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)
        
        cancel_button = QPushButton("Cancelar")
        cancel_button.clicked.connect(self.reject)
        cancel_button.setStyleSheet("""
            QPushButton {
                background-color: #e0e0e0;
                color: #333;
                border: none;
                border-radius: 8px;
                padding: 12px;
                font-size: 11px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #d0d0d0;
            }
        """)
        button_layout.addWidget(cancel_button)
        
        register_button = QPushButton("✅ Registrar")
        register_button.clicked.connect(self.register_user)
        register_button.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #11998e, stop:1 #38ef7d);
                color: white;
                border: none;
                border-radius: 8px;
                padding: 12px;
                font-size: 11px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #0f8b7f, stop:1 #2ed96d);
            }
        """)
        button_layout.addWidget(register_button)
        
        panel_layout.addSpacing(20)
        panel_layout.addLayout(button_layout)
        
        main_layout.addWidget(panel)
    
    def get_input_style(self):
        return """
            QLineEdit {
                border: 2px solid #e0e0e0;
                border-radius: 8px;
                padding: 12px;
                background-color: #f8f9fa;
                font-size: 11px;
            }
            QLineEdit:focus {
                border: 2px solid #11998e;
                background-color: white;
            }
        """
    
    def register_user(self):
        """Registra un nuevo usuario"""
        name = self.name_input.text().strip()
        username = self.username_input.text().strip()
        password = self.password_input.text()
        confirm = self.confirm_input.text()
        
        # Validaciones
        if not name or not username or not password:
            QMessageBox.warning(self, "Error", "Por favor completa todos los campos")
            return
        
        if len(username) < 3:
            QMessageBox.warning(self, "Error", "El usuario debe tener al menos 3 caracteres")
            return
        
        if len(password) < 6:
            QMessageBox.warning(self, "Error", "La contraseña debe tener al menos 6 caracteres")
            return
        
        if password != confirm:
            QMessageBox.warning(self, "Error", "Las contraseñas no coinciden")
            return
        
        try:
            # Cargar usuarios existentes
            with open(self.users_file, 'r', encoding='utf-8') as f:
                users = json.load(f)
            
            # Verificar si el usuario ya existe
            if username in users:
                QMessageBox.warning(self, "Error", "El usuario ya existe")
                return
            
            # Agregar nuevo usuario
            users[username] = {
                "password": hashlib.sha256(password.encode()).hexdigest(),
                "name": name,
                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
            # Guardar
            with open(self.users_file, 'w', encoding='utf-8') as f:
                json.dump(users, f, indent=4, ensure_ascii=False)
            
            self.accept()
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al registrar usuario: {e}")


# Importar para usar en el main
import os
from datetime import datetime
