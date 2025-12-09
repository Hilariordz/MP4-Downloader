# 🎥 Descargador de Videos Universal

Programa en Python para descargar videos de múltiples plataformas con selección de calidad.

## 🌟 Características

- ✅ Descarga videos de YouTube, TikTok, Instagram, Twitter, Facebook y más
- ✅ Selección de calidad (1080p, 720p, 480p, 360p)
- ✅ Interfaz de línea de comandos fácil de usar
- ✅ Barra de progreso en tiempo real
- ✅ Conversión automática a MP4

## 📋 Requisitos

- Python 3.7 o superior
- pip (gestor de paquetes de Python)

## 🚀 Instalación

1. Clona o descarga este repositorio

2. Instala las dependencias:
```bash
pip install -r requirements.txt
```

## 💻 Uso

### 🎨 Versión con Diseño Moderno (Recomendado):
```bash
python video_downloader_modern.py
```

### 🖼️ Versión con Interfaz Gráfica:
```bash
python video_downloader_gui.py
```

### ⌨️ Versión de Línea de Comandos:
```bash
python video_downloader.py
```

## 🎨 Capturas de Pantalla

### Interfaz Moderna (ttkbootstrap)
- Diseño oscuro elegante
- Botones con colores vibrantes
- Barra de progreso animada
- Registro de actividad en tiempo real
- Botón para abrir carpeta de descargas

### Interfaz Gráfica (customtkinter)
- Tema oscuro moderno
- Interfaz limpia y minimalista
- Controles intuitivos

### Opciones disponibles:

1. **Mejor calidad**: Descarga en la máxima calidad disponible
2. **1080p**: Full HD
3. **720p**: HD
4. **480p**: Calidad estándar
5. **360p**: Calidad baja
6. **Peor calidad**: Mínima calidad (archivos más pequeños)
7. **Ver formatos**: Muestra todos los formatos disponibles para el video

## 🎯 Plataformas Soportadas

- YouTube
- TikTok
- Instagram
- Twitter/X
- Facebook
- Vimeo
- Dailymotion
- Reddit
- Y muchas más (1000+ sitios)

## 📁 Ubicación de Descargas

Los videos se guardan en la carpeta `descargas/` en el mismo directorio del programa.

## ⚠️ Nota Legal

Este programa es solo para uso educativo y personal. Respeta los derechos de autor y los términos de servicio de las plataformas. No uses este programa para:

- Descargar contenido protegido por derechos de autor sin permiso
- Violar términos de servicio de plataformas
- Redistribuir contenido sin autorización

## 🛠️ Solución de Problemas

### Error: "yt-dlp no está instalado"
```bash
pip install yt-dlp
```

### Error al descargar de ciertas plataformas
Actualiza yt-dlp a la última versión:
```bash
pip install --upgrade yt-dlp
```

## 📝 Ejemplos de Uso

```
🔗 Ingresa la URL del video: https://www.youtube.com/watch?v=ejemplo
👉 Selecciona una opción: 3

🎬 Descargando video en calidad: 720p
📁 Guardando en: C:\ruta\descargas

Progreso: 45.2% | Velocidad: 2.5MB/s | ETA: 00:15
```

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor, abre un issue o pull request.

## 📄 Licencia

Este proyecto es de código abierto y está disponible bajo la licencia MIT.
Desarrollado por JHRF