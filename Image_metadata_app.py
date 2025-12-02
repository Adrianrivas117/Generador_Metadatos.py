import sys
import json
import os
from datetime import datetime
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QLabel, QLineEdit, 
                             QTextEdit, QFileDialog, QMessageBox, QListWidget,
                             QScrollArea, QFrame)
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt
from login import LoginDialog


class ImageMetadataApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.current_image_path = None
        self.metadata_file = "image_metadata.json"
        self.metadata_db = self.load_metadata()
        self.init_ui()
        
    def init_ui(self):
        self.setWindowTitle("📸 Generador de Metadatos de Imágenes")
        self.setGeometry(100, 100, 1400, 900)
        
        # Estilo general simple
        self.setStyleSheet("""
            QMainWindow {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #667eea, stop:1 #764ba2);
            }
            QWidget {
                font-family: 'Segoe UI', Arial, sans-serif;
            }
        """)
        
        # Widget central con fondo blanco
        central_widget = QWidget()
        central_widget.setStyleSheet("""
            QWidget {
                background-color: white;
                border-radius: 20px;
            }
        """)
        self.setCentralWidget(central_widget)
        
        # Layout principal con márgenes
        main_container = QVBoxLayout()
        main_container.setContentsMargins(20, 20, 20, 20)
        central_widget.setLayout(main_container)
        
        # Header
        header = self.create_header()
        main_container.addWidget(header)
        
        # Contenido principal
        content_layout = QHBoxLayout()
        content_layout.setSpacing(30)
        
        # Panel izquierdo
        left_panel = self.create_left_panel()
        content_layout.addWidget(left_panel, 1)
        
        # Panel derecho
        right_panel = self.create_right_panel()
        content_layout.addWidget(right_panel, 1)
        
        main_container.addLayout(content_layout)
        
    def create_header(self):
        header = QFrame()
        header.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #667eea, stop:1 #764ba2);
                border-radius: 15px;
                padding: 25px;
            }
            QLabel {
                color: white;
            }
        """)
        
        header_layout = QVBoxLayout()
        header.setLayout(header_layout)
        
        title = QLabel("📸 Generador de Metadatos de Imágenes")
        title.setFont(QFont("Segoe UI", 24, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        
        subtitle = QLabel("Carga imágenes y genera metadatos en formato JSON")
        subtitle.setFont(QFont("Segoe UI", 12))
        subtitle.setAlignment(Qt.AlignCenter)
        
        header_layout.addWidget(title)
        header_layout.addWidget(subtitle)
        
        return header
    
    def create_left_panel(self):
        panel = QFrame()
        panel.setStyleSheet("""
            QFrame {
                background-color: #f8f9fa;
                border-radius: 15px;
                padding: 20px;
            }
        """)
        
        layout = QVBoxLayout()
        panel.setLayout(layout)
        
        # Título del panel
        title = QLabel("🖼️ Imagen")
        title.setFont(QFont("Segoe UI", 18, QFont.Bold))
        title.setStyleSheet("color: #667eea; padding: 10px;")
        layout.addWidget(title)
        
        # Vista previa de imagen
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setMinimumSize(500, 450)
        self.image_label.setMaximumSize(700, 500)
        self.image_label.setStyleSheet("""
            QLabel {
                border: 3px dashed #667eea;
                border-radius: 15px;
                background-color: white;
                padding: 20px;
            }
        """)
        self.set_placeholder_image()
        layout.addWidget(self.image_label)
        
        # Botón cargar imagen
        self.load_button = QPushButton("📁 Cargar Imagen")
        self.load_button.clicked.connect(self.load_image)
        self.load_button.setFont(QFont("Segoe UI", 12, QFont.Bold))
        self.load_button.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #667eea, stop:1 #764ba2);
                color: white;
                border: none;
                border-radius: 10px;
                padding: 15px;
                margin-top: 10px;
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
        layout.addWidget(self.load_button)
        
        # Información del archivo
        self.file_info_label = QLabel()
        self.file_info_label.setWordWrap(True)
        self.file_info_label.setStyleSheet("""
            QLabel {
                background-color: #e3f2fd;
                border-radius: 10px;
                padding: 15px;
                margin-top: 10px;
                border: none;
            }
        """)
        self.file_info_label.hide()
        layout.addWidget(self.file_info_label)
        
        layout.addStretch()
        
        return panel
    
    def create_right_panel(self):
        panel = QFrame()
        panel.setStyleSheet("""
            QFrame {
                background-color: #f8f9fa;
                border-radius: 15px;
                padding: 20px;
            }
        """)
        
        layout = QVBoxLayout()
        panel.setLayout(layout)
        
        # Scroll area para el contenido
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: transparent;
            }
        """)
        
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout()
        scroll_content.setLayout(scroll_layout)
        
        # Botones
        button_layout = QHBoxLayout()
        button_layout.setSpacing(15)
        
        self.save_button = QPushButton("💾 Guardar")
        self.save_button.clicked.connect(self.save_metadata)
        self.save_button.setEnabled(False)
        self.save_button.setFont(QFont("Segoe UI", 11, QFont.Bold))
        self.save_button.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #11998e, stop:1 #38ef7d);
                color: white;
                border: none;
                border-radius: 10px;
                padding: 15px;
                margin-top: 15px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #0f8b7f, stop:1 #2ed96d);
            }
            QPushButton:disabled {
                background-color: #cccccc;
                color: #666666;
            }
        """)
        button_layout.addWidget(self.save_button)
        
        self.export_button = QPushButton("📤 Exportar JSON")
        self.export_button.clicked.connect(self.export_json)
        self.export_button.setFont(QFont("Segoe UI", 11, QFont.Bold))
        self.export_button.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #3498db, stop:1 #2980b9);
                color: white;
                border: none;
                border-radius: 10px;
                padding: 15px;
                margin-top: 15px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #2e86c1, stop:1 #21618c);
            }
        """)
        button_layout.addWidget(self.export_button)
        
        scroll_layout.addLayout(button_layout)
        
        # Imágenes guardadas
        saved_title = QLabel("📚 Imágenes Guardadas")
        saved_title.setFont(QFont("Segoe UI", 16, QFont.Bold))
        saved_title.setStyleSheet("color: #667eea; padding: 10px; margin-top: 20px;")
        scroll_layout.addWidget(saved_title)
        
        self.saved_list = QListWidget()
        self.saved_list.itemClicked.connect(self.load_saved_metadata)
        self.saved_list.setMinimumHeight(300)
        self.saved_list.setStyleSheet("""
            QListWidget {
                border: 2px solid #e0e0e0;
                border-radius: 10px;
                background-color: white;
                padding: 10px;
            }
            QListWidget::item {
                padding: 15px;
                border-radius: 8px;
                margin-bottom: 8px;
                background-color: #f8f9fa;
            }
            QListWidget::item:hover {
                background-color: #e3f2fd;
            }
            QListWidget::item:selected {
                background-color: #667eea;
                color: white;
            }
        """)
        scroll_layout.addWidget(self.saved_list)
        
        scroll.setWidget(scroll_content)
        layout.addWidget(scroll)
        
        self.update_saved_list()
        
        return panel
    
    def set_placeholder_image(self):
        self.image_label.setText(
            "📁\n\n"
            "No hay imagen cargada\n\n"
            "Haz clic en 'Cargar Imagen' para empezar"
        )
        self.image_label.setStyleSheet(self.image_label.styleSheet() + 
            "font-size: 16px; color: #999;")
    
    def load_image(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self, 
            "Seleccionar Imagen", 
            "", 
            "Imágenes (*.png *.jpg *.jpeg *.bmp *.gif)"
        )
        
        if file_name:
            self.current_image_path = file_name
            
            # Mostrar imagen
            pixmap = QPixmap(file_name)
            scaled_pixmap = pixmap.scaled(
                self.image_label.size(), 
                Qt.KeepAspectRatio, 
                Qt.SmoothTransformation
            )
            self.image_label.setPixmap(scaled_pixmap)
            self.image_label.setStyleSheet("""
                QLabel {
                    border: 3px dashed #667eea;
                    border-radius: 15px;
                    background-color: white;
                    padding: 20px;
                }
            """)
            
            # Mostrar información del archivo
            file_size = os.path.getsize(file_name)
            file_info = f"<b>📄 Información del archivo:</b><br>"
            file_info += f"<b>Nombre:</b> {os.path.basename(file_name)}<br>"
            file_info += f"<b>Tamaño:</b> {file_size / 1024:.2f} KB<br>"
            file_info += f"<b>Dimensiones:</b> {pixmap.width()}x{pixmap.height()} px"
            self.file_info_label.setText(file_info)
            self.file_info_label.show()
            
            # Habilitar botón de guardar
            self.save_button.setEnabled(True)
            
            # Cargar metadatos si existen
            self.load_existing_metadata()
    
    def load_existing_metadata(self):
        pass
    
    def clear_metadata_fields(self):
        pass
    
    def save_metadata(self):
        if not self.current_image_path:
            QMessageBox.warning(self, "Error", "No hay imagen cargada")
            return
        
        # Obtener información de la imagen
        pixmap = QPixmap(self.current_image_path)
        file_size = os.path.getsize(self.current_image_path)
        file_stats = os.stat(self.current_image_path)
        
        # Calcular información adicional
        aspect_ratio = pixmap.width() / pixmap.height() if pixmap.height() > 0 else 0
        megapixels = (pixmap.width() * pixmap.height()) / 1_000_000
        
        # Determinar formato y extensión
        file_ext = os.path.splitext(self.current_image_path)[1].upper().replace('.', '')
        file_name_without_ext = os.path.splitext(os.path.basename(self.current_image_path))[0]
        
        # Calcular aspect ratio común (ej: 16:9, 4:3, etc)
        def gcd(a, b):
            while b:
                a, b = b, a % b
            return a
        
        width_height_gcd = gcd(pixmap.width(), pixmap.height())
        aspect_w = pixmap.width() // width_height_gcd if width_height_gcd > 0 else pixmap.width()
        aspect_h = pixmap.height() // width_height_gcd if width_height_gcd > 0 else pixmap.height()
        
        # Determinar orientación descriptiva
        if pixmap.width() > pixmap.height():
            orientation = "Horizontal (Landscape)"
        elif pixmap.height() > pixmap.width():
            orientation = "Vertical (Portrait)"
        else:
            orientation = "Cuadrado (Square)"
        
        # Calcular tamaño en diferentes unidades
        size_bytes = file_size
        size_kb = round(file_size / 1024, 2)
        size_mb = round(file_size / (1024 * 1024), 2)
        size_gb = round(file_size / (1024 * 1024 * 1024), 4)
        
        # Determinar categoría de tamaño
        if size_mb < 0.1:
            size_category = "Muy pequeño"
        elif size_mb < 1:
            size_category = "Pequeño"
        elif size_mb < 5:
            size_category = "Mediano"
        elif size_mb < 10:
            size_category = "Grande"
        else:
            size_category = "Muy grande"
        
        # Determinar categoría de resolución
        total_pixels = pixmap.width() * pixmap.height()
        if total_pixels < 500_000:
            resolution_category = "Baja resolución"
        elif total_pixels < 2_000_000:
            resolution_category = "Resolución estándar"
        elif total_pixels < 8_000_000:
            resolution_category = "Alta resolución (HD)"
        elif total_pixels < 20_000_000:
            resolution_category = "Muy alta resolución (Full HD/4K)"
        else:
            resolution_category = "Ultra alta resolución (8K+)"
        
        # Obtener información del directorio
        directory = os.path.dirname(self.current_image_path)
        drive = os.path.splitdrive(self.current_image_path)[0]
        
        # Calcular hash MD5 del archivo para verificación de integridad
        import hashlib
        md5_hash = hashlib.md5()
        with open(self.current_image_path, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b""):
                md5_hash.update(chunk)
        file_hash = md5_hash.hexdigest()
        
        # Información de bits por pixel (profundidad de color)
        bits_per_pixel = pixmap.depth()
        
        # Recopilar metadatos completos y detallados
        metadata = {
            # Información básica del archivo
            "file_info": {
                "filename": os.path.basename(self.current_image_path),
                "filename_without_extension": file_name_without_ext,
                "filepath": self.current_image_path,
                "directory": directory,
                "drive": drive,
                "file_extension": file_ext,
                "file_format": file_ext or "UNKNOWN"
            },
            
            # Tamaños en diferentes unidades
            "file_size": {
                "bytes": size_bytes,
                "kilobytes": size_kb,
                "megabytes": size_mb,
                "gigabytes": size_gb,
                "human_readable": f"{size_mb} MB" if size_mb >= 1 else f"{size_kb} KB",
                "category": size_category
            },
            
            # Dimensiones y resolución
            "image_dimensions": {
                "width_pixels": pixmap.width(),
                "height_pixels": pixmap.height(),
                "resolution": f"{pixmap.width()}x{pixmap.height()}",
                "total_pixels": total_pixels,
                "megapixels": round(megapixels, 2),
                "resolution_category": resolution_category
            },
            
            # Información de aspecto y orientación
            "aspect_ratio": {
                "decimal": round(aspect_ratio, 4),
                "ratio": f"{aspect_w}:{aspect_h}",
                "orientation": orientation,
                "is_landscape": pixmap.width() > pixmap.height(),
                "is_portrait": pixmap.height() > pixmap.width(),
                "is_square": pixmap.width() == pixmap.height()
            },
            
            # Información de color
            "color_info": {
                "bits_per_pixel": bits_per_pixel,
                "has_alpha_channel": pixmap.hasAlphaChannel(),
                "color_depth": f"{bits_per_pixel} bits"
            },
            
            # Fechas y tiempos
            "timestamps": {
                "metadata_created": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "file_modified": datetime.fromtimestamp(file_stats.st_mtime).strftime("%Y-%m-%d %H:%M:%S"),
                "file_accessed": datetime.fromtimestamp(file_stats.st_atime).strftime("%Y-%m-%d %H:%M:%S"),
                "file_created_system": datetime.fromtimestamp(file_stats.st_ctime).strftime("%Y-%m-%d %H:%M:%S"),
                "unix_timestamp_modified": int(file_stats.st_mtime),
                "unix_timestamp_accessed": int(file_stats.st_atime)
            },
            
            # Información del sistema
            "system_info": {
                "file_mode": oct(file_stats.st_mode),
                "file_inode": file_stats.st_ino if hasattr(file_stats, 'st_ino') else None,
                "operating_system": os.name,
                "file_hash_md5": file_hash
            },
            
            # Estadísticas adicionales
            "statistics": {
                "aspect_ratio_percentage": round((pixmap.width() / pixmap.height() * 100) if pixmap.height() > 0 else 0, 2),
                "compression_ratio_estimate": "N/A",
                "pixel_density_category": resolution_category,
                "recommended_use": self.get_recommended_use(pixmap.width(), pixmap.height(), size_mb)
            }
        }
        
        # Guardar en base de datos
        self.metadata_db[self.current_image_path] = metadata
        self.save_metadata_to_file()
        
        self.update_saved_list()
        
        QMessageBox.information(
            self, 
            "✅ Éxito", 
            "Metadatos guardados correctamente"
        )
    
    def get_recommended_use(self, width, height, size_mb):
        """Recomienda el uso según las dimensiones y tamaño"""
        total_pixels = width * height
        
        if total_pixels < 500_000:
            return "Iconos, miniaturas, web pequeña"
        elif total_pixels < 2_000_000:
            return "Web estándar, redes sociales"
        elif total_pixels < 8_000_000:
            return "Impresión pequeña, pantallas HD"
        elif total_pixels < 20_000_000:
            return "Impresión grande, fotografía profesional"
        else:
            return "Impresión comercial, publicidad, arte digital"
    
    def load_metadata(self):
        """Carga la base de datos JSON"""
        if os.path.exists(self.metadata_file):
            try:
                with open(self.metadata_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    # Si es el formato antiguo (sin estructura), convertir
                    if not isinstance(data, dict) or 'images' not in data:
                        return self.migrate_old_format(data)
                    return data.get('images', {})
            except Exception as e:
                print(f"Error al cargar base de datos: {e}")
                return {}
        else:
            # Crear base de datos inicial
            self.initialize_database()
            return {}
    
    def initialize_database(self):
        """Inicializa la base de datos con estructura"""
        initial_db = {
            "metadata_version": "1.0",
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "total_images": 0,
            "images": {},
            "settings": {
                "auto_backup": True,
                "max_images": 1000
            }
        }
        with open(self.metadata_file, 'w', encoding='utf-8') as f:
            json.dump(initial_db, f, indent=4, ensure_ascii=False)
    
    def migrate_old_format(self, old_data):
        """Migra datos del formato antiguo al nuevo"""
        if isinstance(old_data, dict):
            return old_data
        return {}
    
    def save_metadata_to_file(self):
        """Guarda la base de datos JSON con estructura completa"""
        try:
            # Cargar estructura completa
            if os.path.exists(self.metadata_file):
                with open(self.metadata_file, 'r', encoding='utf-8') as f:
                    full_db = json.load(f)
            else:
                full_db = {
                    "metadata_version": "1.0",
                    "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "total_images": 0,
                    "images": {},
                    "settings": {
                        "auto_backup": True,
                        "max_images": 1000
                    }
                }
            
            # Actualizar datos
            full_db['images'] = self.metadata_db
            full_db['total_images'] = len(self.metadata_db)
            full_db['last_updated'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Guardar
            with open(self.metadata_file, 'w', encoding='utf-8') as f:
                json.dump(full_db, f, indent=4, ensure_ascii=False)
            
            # Crear backup si está habilitado
            if full_db.get('settings', {}).get('auto_backup', True):
                self.create_backup()
                
        except Exception as e:
            print(f"Error al guardar base de datos: {e}")
    
    def create_backup(self):
        """Crea un backup de la base de datos"""
        try:
            backup_dir = "backups"
            if not os.path.exists(backup_dir):
                os.makedirs(backup_dir)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_file = os.path.join(backup_dir, f"metadata_backup_{timestamp}.json")
            
            if os.path.exists(self.metadata_file):
                with open(self.metadata_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                with open(backup_file, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=4, ensure_ascii=False)
                
                # Mantener solo los últimos 10 backups
                self.cleanup_old_backups(backup_dir)
        except Exception as e:
            print(f"Error al crear backup: {e}")
    
    def cleanup_old_backups(self, backup_dir, max_backups=10):
        """Elimina backups antiguos manteniendo solo los más recientes"""
        try:
            backups = [f for f in os.listdir(backup_dir) if f.startswith("metadata_backup_")]
            backups.sort(reverse=True)
            
            for old_backup in backups[max_backups:]:
                os.remove(os.path.join(backup_dir, old_backup))
        except Exception as e:
            print(f"Error al limpiar backups: {e}")
    
    def update_saved_list(self):
        self.saved_list.clear()
        for path, metadata in self.metadata_db.items():
            # Extraer información según la estructura
            if isinstance(metadata.get('file_info'), dict):
                filename = metadata['file_info'].get('filename', 'Sin nombre')
                resolution = metadata['image_dimensions'].get('resolution', 'N/A')
                date = metadata['timestamps'].get('metadata_created', '')
            else:
                # Compatibilidad con formato antiguo
                filename = metadata.get('filename', 'Sin nombre')
                resolution = metadata.get('resolution', 'N/A')
                date = metadata.get('date_created', '')
            
            item_text = f"📷 {filename}\n"
            item_text += f"   🖼️ {resolution}\n"
            item_text += f"   📅 {date}"
            self.saved_list.addItem(item_text)
    
    def load_saved_metadata(self, item):
        index = self.saved_list.currentRow()
        paths = list(self.metadata_db.keys())
        
        if index < len(paths):
            selected_path = paths[index]
            
            if os.path.exists(selected_path):
                self.current_image_path = selected_path
                
                # Cargar imagen
                pixmap = QPixmap(selected_path)
                scaled_pixmap = pixmap.scaled(
                    self.image_label.size(), 
                    Qt.KeepAspectRatio, 
                    Qt.SmoothTransformation
                )
                self.image_label.setPixmap(scaled_pixmap)
                self.image_label.setStyleSheet("""
                    QLabel {
                        border: 3px dashed #667eea;
                        border-radius: 15px;
                        background-color: white;
                        padding: 20px;
                    }
                """)
                
                # Cargar info
                file_size = os.path.getsize(selected_path)
                file_info = f"<b>📄 Información del archivo:</b><br>"
                file_info += f"<b>Nombre:</b> {os.path.basename(selected_path)}<br>"
                file_info += f"<b>Tamaño:</b> {file_size / 1024:.2f} KB<br>"
                file_info += f"<b>Dimensiones:</b> {pixmap.width()}x{pixmap.height()} px"
                self.file_info_label.setText(file_info)
                self.file_info_label.show()
                
                self.save_button.setEnabled(True)
            else:
                QMessageBox.warning(
                    self, 
                    "Error", 
                    "La imagen no existe en la ruta especificada"
                )
    
    def export_json(self):
        if not self.metadata_db:
            QMessageBox.warning(
                self, 
                "Error", 
                "No hay metadatos para exportar"
            )
            return
        
        file_name, _ = QFileDialog.getSaveFileName(
            self, 
            "Exportar Metadatos", 
            "metadata_export.json", 
            "JSON (*.json)"
        )
        
        if file_name:
            with open(file_name, 'w', encoding='utf-8') as f:
                json.dump(self.metadata_db, f, indent=4, ensure_ascii=False)
            
            QMessageBox.information(
                self, 
                "✅ Éxito", 
                f"Metadatos exportados a {file_name}"
            )


def main():
    """Función principal para ejecutar la aplicación"""
    try:
        app = QApplication(sys.argv)
        app.setStyle('Fusion')  # Estilo moderno multiplataforma
        
        # Mostrar login primero
        login = LoginDialog()
        if login.exec_() == login.Accepted:
            # Si el login es exitoso, mostrar la aplicación principal
            window = ImageMetadataApp()
            window.show()
            sys.exit(app.exec_())
        else:
            # Si se cancela el login, salir
            sys.exit(0)
    except Exception as e:
        print(f"Error al iniciar la aplicación: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
