#!/usr/bin/env python3
"""
Descargador de Videos Universal - Interfaz Gráfica
"""

import os
import sys
import threading
from pathlib import Path

try:
    import customtkinter as ctk
    import yt_dlp
except ImportError:
    print("Error: Faltan dependencias.")
    print("Instala con: pip install customtkinter yt-dlp")
    sys.exit(1)

# Agregar FFmpeg al PATH si está instalado por WinGet
ffmpeg_path = Path(os.environ.get('LOCALAPPDATA', '')) / 'Microsoft' / 'WinGet' / 'Links'
if ffmpeg_path.exists() and str(ffmpeg_path) not in os.environ.get('PATH', ''):
    os.environ['PATH'] = str(ffmpeg_path) + os.pathsep + os.environ.get('PATH', '')


class VideoDownloaderGUI:
    def __init__(self):
        self.window = ctk.CTk()
        self.window.title("🎥 Descargador de Videos Universal")
        self.window.geometry("700x600")
        
        # Configurar tema
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        self.output_dir = Path("descargas")
        self.output_dir.mkdir(exist_ok=True)
        
        self.setup_ui()
    
    def setup_ui(self):
        # Frame principal
        main_frame = ctk.CTkFrame(self.window)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Título
        title = ctk.CTkLabel(
            main_frame,
            text="🎥 Descargador de Videos",
            font=ctk.CTkFont(size=28, weight="bold")
        )
        title.pack(pady=(20, 10))
        
        subtitle = ctk.CTkLabel(
            main_frame,
            text="Descarga videos de YouTube, TikTok, Instagram y más",
            font=ctk.CTkFont(size=12),
            text_color="gray"
        )
        subtitle.pack(pady=(0, 30))
        
        # Frame para URL
        url_frame = ctk.CTkFrame(main_frame)
        url_frame.pack(fill="x", padx=20, pady=10)
        
        url_label = ctk.CTkLabel(
            url_frame,
            text="🔗 URL del Video:",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        url_label.pack(anchor="w", padx=10, pady=(10, 5))
        
        self.url_entry = ctk.CTkEntry(
            url_frame,
            placeholder_text="Pega aquí el enlace del video...",
            height=40,
            font=ctk.CTkFont(size=13)
        )
        self.url_entry.pack(fill="x", padx=10, pady=(0, 10))
        
        # Frame para calidad
        quality_frame = ctk.CTkFrame(main_frame)
        quality_frame.pack(fill="x", padx=20, pady=10)
        
        quality_label = ctk.CTkLabel(
            quality_frame,
            text="📊 Calidad del Video:",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        quality_label.pack(anchor="w", padx=10, pady=(10, 5))
        
        self.quality_var = ctk.StringVar(value="best")
        
        qualities = [
            ("🏆 Mejor Calidad", "best"),
            ("📺 1080p (Full HD)", "1080"),
            ("📺 720p (HD)", "720"),
            ("📺 480p (SD)", "480"),
            ("📺 360p", "360"),
            ("💾 Peor Calidad (menor tamaño)", "worst")
        ]
        
        for text, value in qualities:
            radio = ctk.CTkRadioButton(
                quality_frame,
                text=text,
                variable=self.quality_var,
                value=value,
                font=ctk.CTkFont(size=12)
            )
            radio.pack(anchor="w", padx=20, pady=3)
        
        quality_frame.pack_configure(pady=(10, 10))
        
        # Frame para carpeta de salida
        output_frame = ctk.CTkFrame(main_frame)
        output_frame.pack(fill="x", padx=20, pady=10)
        
        output_label = ctk.CTkLabel(
            output_frame,
            text="📁 Guardar en:",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        output_label.pack(anchor="w", padx=10, pady=(10, 5))
        
        self.output_label = ctk.CTkLabel(
            output_frame,
            text=str(self.output_dir.absolute()),
            font=ctk.CTkFont(size=11),
            text_color="gray"
        )
        self.output_label.pack(anchor="w", padx=10, pady=(0, 10))
        
        # Botón de descarga
        self.download_btn = ctk.CTkButton(
            main_frame,
            text="⬇️ DESCARGAR VIDEO",
            command=self.start_download,
            height=50,
            font=ctk.CTkFont(size=16, weight="bold"),
            fg_color="#1f6aa5",
            hover_color="#144870"
        )
        self.download_btn.pack(fill="x", padx=20, pady=20)
        
        # Barra de progreso
        self.progress_bar = ctk.CTkProgressBar(main_frame)
        self.progress_bar.pack(fill="x", padx=20, pady=(0, 10))
        self.progress_bar.set(0)
        
        # Label de estado
        self.status_label = ctk.CTkLabel(
            main_frame,
            text="",
            font=ctk.CTkFont(size=12)
        )
        self.status_label.pack(pady=5)
        
        # Área de log
        self.log_text = ctk.CTkTextbox(
            main_frame,
            height=100,
            font=ctk.CTkFont(size=11)
        )
        self.log_text.pack(fill="both", expand=True, padx=20, pady=(10, 20))
    
    def log(self, message, color="white"):
        """Agrega mensaje al log"""
        self.log_text.insert("end", message + "\n")
        self.log_text.see("end")
    
    def update_status(self, message, color="white"):
        """Actualiza el label de estado"""
        self.status_label.configure(text=message, text_color=color)
    
    def start_download(self):
        """Inicia la descarga en un hilo separado"""
        url = self.url_entry.get().strip()
        
        if not url:
            self.update_status("❌ Por favor ingresa una URL", "red")
            return
        
        # Deshabilitar botón durante descarga
        self.download_btn.configure(state="disabled", text="⏳ Descargando...")
        self.progress_bar.set(0)
        self.log_text.delete("1.0", "end")
        
        # Ejecutar descarga en hilo separado
        thread = threading.Thread(target=self.download_video, args=(url,))
        thread.daemon = True
        thread.start()
    
    def download_video(self, url):
        """Descarga el video"""
        quality = self.quality_var.get()
        
        # Usar FFmpeg para mejor calidad
        if quality == 'best':
            format_string = 'bestvideo+bestaudio/best'
        elif quality == 'worst':
            format_string = 'worstvideo+worstaudio/worst'
        else:
            format_string = f'bestvideo[height<={quality}]+bestaudio/best[height<={quality}]'
        
        ydl_opts = {
            'format': format_string,
            'outtmpl': str(self.output_dir / '%(title)s.%(ext)s'),
            'merge_output_format': 'mp4',
            'progress_hooks': [self.progress_hook],
        }
        
        try:
            self.log(f"🎬 Iniciando descarga...")
            self.log(f"🔗 URL: {url}")
            self.log(f"📊 Calidad: {quality}")
            self.log(f"📁 Carpeta: {self.output_dir.absolute()}")
            self.log("-" * 50)
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                title = info.get('title', 'video')
                self.log(f"📹 Título: {title}")
                self.log("")
                
                ydl.download([url])
            
            self.window.after(0, lambda: self.update_status("✅ Descarga completada!", "green"))
            self.log("")
            self.log("✅ ¡Descarga completada exitosamente!")
            self.window.after(0, lambda: self.progress_bar.set(1))
            
        except Exception as e:
            error_msg = str(e)
            self.window.after(0, lambda: self.update_status(f"❌ Error: {error_msg}", "red"))
            self.log(f"❌ Error: {error_msg}")
        
        finally:
            # Rehabilitar botón
            self.window.after(0, lambda: self.download_btn.configure(
                state="normal",
                text="⬇️ DESCARGAR VIDEO"
            ))
    
    def progress_hook(self, d):
        """Hook para actualizar progreso"""
        if d['status'] == 'downloading':
            try:
                # Calcular porcentaje
                if 'total_bytes' in d:
                    percent = d['downloaded_bytes'] / d['total_bytes']
                elif 'total_bytes_estimate' in d:
                    percent = d['downloaded_bytes'] / d['total_bytes_estimate']
                else:
                    percent = 0
                
                # Actualizar barra de progreso
                self.window.after(0, lambda p=percent: self.progress_bar.set(p))
                
                # Actualizar estado
                percent_str = d.get('_percent_str', 'N/A')
                speed_str = d.get('_speed_str', 'N/A')
                eta_str = d.get('_eta_str', 'N/A')
                
                status = f"⬇️ Descargando: {percent_str} | Velocidad: {speed_str} | ETA: {eta_str}"
                self.window.after(0, lambda s=status: self.update_status(s, "cyan"))
                
            except Exception:
                pass
        
        elif d['status'] == 'finished':
            self.window.after(0, lambda: self.update_status("🔄 Procesando video...", "yellow"))
    
    def run(self):
        """Ejecuta la aplicación"""
        self.window.mainloop()


if __name__ == "__main__":
    app = VideoDownloaderGUI()
    app.run()
