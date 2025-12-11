# Base de Datos JSON - Sistema de Metadatos de Imágenes

## Estructura de la Base de Datos

El sistema usa un archivo JSON (`image_metadata.json`) como base de datos simple y eficiente.

### Estructura Principal

```json
{
  "metadata_version": "1.0",
  "created_at": "2025-12-01 10:30:00",
  "last_updated": "2025-12-01 15:45:30",
  "total_images": 5,
  "images": {
    "C:\\ruta\\imagen1.jpg": { ... },
    "C:\\ruta\\imagen2.png": { ... }
  },
  "settings": {
    "auto_backup": true,
    "max_images": 1000
  }
}
```

## Características

### ✅ Funcionalidades Implementadas

1. **Estructura Organizada**
   - Versión de metadatos
   - Fechas de creación y actualización
   - Contador de imágenes totales
   - Configuraciones del sistema

2. **Sistema de Backups Automáticos**
   - Crea backups en la carpeta `backups/`
   - Formato: `metadata_backup_YYYYMMDD_HHMMSS.json`
   - Mantiene los últimos 10 backups
   - Se ejecuta automáticamente al guardar

3. **Migración de Datos**
   - Compatible con formato antiguo
   - Actualiza automáticamente a nueva estructura

4. **Metadatos Completos por Imagen**
   - Información del archivo (nombre, ruta, extensión, tamaño)
   - Dimensiones de imagen (ancho, alto, resolución, megapíxeles)
   - Relación de aspecto y orientación
   - Información de color (profundidad, canal alfa)
   - Timestamps (creación, modificación, acceso)
   - Hash MD5 para verificación de integridad
   - Estadísticas y recomendaciones de uso

## Ubicación de Archivos

```
Pagina/
├── image_metadata.json          # Base de datos principal
├── database_template.json       # Plantilla de estructura
└── backups/                     # Carpeta de backups
    ├── metadata_backup_20251201_103000.json
    ├── metadata_backup_20251201_114500.json
    └── ...
```

## Uso

### Guardar Metadatos
Los metadatos se guardan automáticamente al presionar el botón "💾 Guardar" en la aplicación.

### Exportar Base de Datos
Usa el botón "📤 Exportar JSON" para crear una copia personalizada de la base de datos.

### Restaurar desde Backup
1. Ve a la carpeta `backups/`
2. Copia el backup deseado
3. Renómbralo a `image_metadata.json`
4. Reinicia la aplicación

## Ejemplo de Metadatos de una Imagen

```json
{
  "file_info": {
    "filename": "paisaje.jpg",
    "filepath": "C:\\Users\\Adria\\Pictures\\paisaje.jpg",
    "file_extension": "JPG",
    "file_format": "JPG"
  },
  "file_size": {
    "bytes": 2048576,
    "kilobytes": 2000.56,
    "megabytes": 1.95,
    "human_readable": "1.95 MB"
  },
  "image_dimensions": {
    "width_pixels": 1920,
    "height_pixels": 1080,
    "resolution": "1920x1080",
    "megapixels": 2.07,
    "resolution_category": "Alta resolución (HD)"
  },
  "aspect_ratio": {
    "decimal": 1.7778,
    "ratio": "16:9",
    "orientation": "Horizontal (Landscape)"
  },
  "timestamps": {
    "metadata_created": "2025-12-01 15:30:00",
    "file_modified": "2025-11-28 10:20:15"
  },
  "system_info": {
    "file_hash_md5": "a1b2c3d4e5f6..."
  }
}
```

## Configuraciones

### Modificar Configuraciones
Edita el archivo `image_metadata.json` directamente:

```json
"settings": {
  "auto_backup": true,    // Activar/desactivar backups automáticos
  "max_images": 1000      // Límite máximo de imágenes
}
```

## Mantenimiento

### Limpiar Base de Datos
Para eliminar imágenes que ya no existen:
```python
# La aplicación verifica automáticamente si las imágenes existen
```

### Optimizar Tamaño
Los backups antiguos se eliminan automáticamente (se mantienen los últimos 10).

## Seguridad

- ✅ Codificación UTF-8 para caracteres especiales
- ✅ Formato JSON indentado (4 espacios)
- ✅ Hash MD5 para verificar integridad de archivos
- ✅ Backups automáticos para prevenir pérdida de datos
- ✅ Manejo de errores robusto

## Notas

- La base de datos se actualiza automáticamente al guardar
- Los backups no afectan el rendimiento
- Compatible con rutas de Windows
- Soporta caracteres especiales en nombres de archivo
