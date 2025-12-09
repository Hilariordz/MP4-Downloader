#!/usr/bin/env python3
"""
Descargador de Videos Universal
Soporta múltiples plataformas usando yt-dlp
"""

import os
import sys
from pathlib import Path

try:
    import yt_dlp
except ImportError:
    print("Error: yt-dlp no está instalado.")
    print("Instálalo con: pip install yt-dlp")
    sys.exit(1)

# Agregar FFmpeg al PATH si está instalado por WinGet
ffmpeg_path = Path(os.environ.get('LOCALAPPDATA', '')) / 'Microsoft' / 'WinGet' / 'Links'
if ffmpeg_path.exists() and str(ffmpeg_path) not in os.environ.get('PATH', ''):
    os.environ['PATH'] = str(ffmpeg_path) + os.pathsep + os.environ.get('PATH', '')


class VideoDownloader:
    def __init__(self, output_dir="descargas"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
    
    def obtener_formatos_disponibles(self, url):
        """Obtiene los formatos disponibles para un video"""
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
        }
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                formatos = []
                
                if 'formats' in info:
                    for f in info['formats']:
                        if f.get('vcodec') != 'none' and f.get('acodec') != 'none':
                            formato_info = {
                                'format_id': f.get('format_id'),
                                'ext': f.get('ext'),
                                'resolution': f.get('resolution', 'audio only'),
                                'filesize': f.get('filesize', 0),
                            }
                            formatos.append(formato_info)
                
                return formatos, info.get('title', 'video')
        except Exception as e:
            print(f"Error al obtener formatos: {e}")
            return [], None
    
    def descargar_video(self, url, calidad='best'):
        """
        Descarga un video con la calidad especificada
        
        Opciones de calidad:
        - 'best': Mejor calidad disponible
        - 'worst': Peor calidad
        - '1080': 1080p
        - '720': 720p
        - '480': 480p
        - '360': 360p
        """
        
        # Configurar formato según calidad con FFmpeg
        if calidad == 'best':
            format_string = 'bestvideo+bestaudio/best'
        elif calidad == 'worst':
            format_string = 'worstvideo+worstaudio/worst'
        else:
            format_string = f'bestvideo[height<={calidad}]+bestaudio/best[height<={calidad}]'
        
        ydl_opts = {
            'format': format_string,
            'outtmpl': str(self.output_dir / '%(title)s.%(ext)s'),
            'merge_output_format': 'mp4',
            'progress_hooks': [self._progress_hook],
        }
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                print(f"\n🎬 Descargando video en calidad: {calidad}")
                print(f"📁 Guardando en: {self.output_dir.absolute()}\n")
                ydl.download([url])
                print("\n✅ Descarga completada!")
                return True
        except Exception as e:
            print(f"\n❌ Error al descargar: {e}")
            return False
    
    def _progress_hook(self, d):
        """Hook para mostrar progreso de descarga"""
        if d['status'] == 'downloading':
            percent = d.get('_percent_str', 'N/A')
            speed = d.get('_speed_str', 'N/A')
            eta = d.get('_eta_str', 'N/A')
            print(f"\rProgreso: {percent} | Velocidad: {speed} | ETA: {eta}", end='')
        elif d['status'] == 'finished':
            print("\n🔄 Procesando video...")


def mostrar_menu():
    """Muestra el menú principal"""
    print("\n" + "="*50)
    print("🎥 DESCARGADOR DE VIDEOS UNIVERSAL")
    print("="*50)
    print("\nOpciones de calidad:")
    print("  1. Mejor calidad (best)")
    print("  2. 1080p")
    print("  3. 720p")
    print("  4. 480p")
    print("  5. 360p")
    print("  6. Peor calidad (worst)")
    print("  7. Ver formatos disponibles")
    print("  0. Salir")
    print("="*50)


def main():
    downloader = VideoDownloader()
    
    while True:
        mostrar_menu()
        
        opcion = input("\n👉 Selecciona una opción: ").strip()
        
        if opcion == '0':
            print("\n👋 ¡Hasta luego!")
            break
        
        url = input("\n🔗 Ingresa la URL del video: ").strip()
        
        if not url:
            print("❌ URL inválida")
            continue
        
        if opcion == '7':
            print("\n🔍 Obteniendo formatos disponibles...")
            formatos, titulo = downloader.obtener_formatos_disponibles(url)
            if formatos:
                print(f"\n📹 Video: {titulo}")
                print("\nFormatos disponibles:")
                for i, f in enumerate(formatos[:10], 1):
                    size = f['filesize'] / (1024*1024) if f['filesize'] else 0
                    print(f"  {i}. {f['resolution']} - {f['ext']} ({size:.1f} MB)")
            continue
        
        calidad_map = {
            '1': 'best',
            '2': '1080',
            '3': '720',
            '4': '480',
            '5': '360',
            '6': 'worst'
        }
        
        calidad = calidad_map.get(opcion)
        
        if calidad:
            downloader.descargar_video(url, calidad)
        else:
            print("❌ Opción inválida")
        
        input("\n⏎ Presiona Enter para continuar...")


if __name__ == "__main__":
    main()
