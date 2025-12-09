import os
import sys
import threading
from pathlib import Path
import webbrowser

try:
    import ttkbootstrap as ttk
    from ttkbootstrap.constants import *
    import yt_dlp
except ImportError:
    print("Error: Faltan dependencias.")
    print("Instala con: pip install ttkbootstrap yt-dlp")
    sys.exit(1)

ffmpeg_path = Path(os.environ.get('LOCALAPPDATA', '')) / 'Microsoft' / 'WinGet' / 'Links'
if ffmpeg_path.exists() and str(ffmpeg_path) not in os.environ.get('PATH', ''):
    os.environ['PATH'] = str(ffmpeg_path) + os.pathsep + os.environ.get('PATH', '')


class ModernVideoDownloader:
    def __init__(self):
        self.window = ttk.Window(themename="darkly")
        self.window.title("VidGrab Pro - Descargador Profesional")
        self.window.geometry("750x750")
        
        self.output_dir = Path("descargas")
        self.output_dir.mkdir(exist_ok=True)
        
        self.setup_ui()
    
    def setup_ui(self):
        # Header profesional
        header = ttk.Frame(self.window, bootstyle="primary")
        header.pack(fill="x", padx=0, pady=0)
        
        # Logo y título
        title_frame = ttk.Frame(header, bootstyle="primary")
        title_frame.pack(pady=20)
        
        title_label = ttk.Label(
            title_frame,
            text=" VidGrab Pro",
            font=("Segoe UI", 32, "bold"),
            bootstyle="inverse-primary"
        )
        title_label.pack()
        
        subtitle = ttk.Label(
            title_frame,
            text="Professional Video Downloader",
            font=("Segoe UI", 11, "italic"),
            bootstyle="inverse-secondary"
        )
        subtitle.pack(pady=(5, 0))
        
        container = ttk.Frame(self.window, padding=20)
        container.pack(fill="both", expand=True)
        
        # Card para URL con diseño mejorado
        url_card = ttk.Labelframe(
            container,
            text="  🔗 Video URL  ",
            padding=15,
            bootstyle="info"
        )
        url_card.pack(fill="x", pady=(0, 15))
        
        self.url_entry = ttk.Entry(
            url_card,
            font=("Segoe UI", 12),
            bootstyle="info"
        )
        self.url_entry.pack(fill="x", ipady=10)
        self.url_entry.insert(0, "Paste video link here...")
        self.url_entry.bind("<FocusIn>", self.clear_placeholder)
        
        # Card para calidad con diseño profesional
        quality_card = ttk.Labelframe(
            container,
            text="  📊 Quality Settings  ",
            padding=15,
            bootstyle="success"
        )
        quality_card.pack(fill="x", pady=(0, 15))
        
        self.quality_var = ttk.StringVar(value="best")
        
        # Grid para radio buttons con diseño mejorado
        qualities = [
            ("🏆 Best Quality", "best", "success"),
            ("📺 1080p Full HD", "1080", "info"),
            ("📺 720p HD", "720", "info"),
            ("📺 480p SD", "480", "warning"),
            ("📺 360p", "360", "warning"),
            ("💾 Smallest Size", "worst", "secondary")
        ]
        
        for i, (text, value, style) in enumerate(qualities):
            row = i // 2
            col = i % 2
            
            radio = ttk.Radiobutton(
                quality_card,
                text=text,
                variable=self.quality_var,
                value=value,
                bootstyle=style
            )
            radio.grid(row=row, column=col, sticky="w", padx=10, pady=5)
        
        # Card para carpeta de salida
        output_card = ttk.Labelframe(
            container,
            text="  📁 Output Folder  ",
            padding=15,
            bootstyle="secondary"
        )
        output_card.pack(fill="x", pady=(0, 15))
        
        output_frame = ttk.Frame(output_card)
        output_frame.pack(fill="x")
        
        self.output_label = ttk.Label(
            output_frame,
            text=str(self.output_dir.absolute()),
            font=("Segoe UI", 10),
            bootstyle="secondary"
        )
        self.output_label.pack(side="left", fill="x", expand=True)
        
        open_folder_btn = ttk.Button(
            output_frame,
            text="📂 Open Folder",
            command=self.open_folder,
            bootstyle="secondary-outline",
            width=15
        )
        open_folder_btn.pack(side="right", padx=(15, 0))
        
        # Botón de descarga principal - MUY VISIBLE
        self.download_btn = ttk.Button(
            container,
            text="⬇️  DOWNLOAD VIDEO",
            command=self.start_download,
            bootstyle="success",
            width=30
        )
        self.download_btn.pack(fill="x", pady=(0, 15), ipady=12)
        
        # Barra de progreso
        progress_frame = ttk.Frame(container)
        progress_frame.pack(fill="x", pady=(0, 10))
        
        self.progress_bar = ttk.Progressbar(
            progress_frame,
            mode="determinate",
            bootstyle="success-striped"
        )
        self.progress_bar.pack(fill="x")
        
        # Label de estado con diseño mejorado
        self.status_label = ttk.Label(
            container,
            text="✨ Ready to download",
            font=("Segoe UI", 11, "bold"),
            bootstyle="info"
        )
        self.status_label.pack(pady=(0, 15))
        
        # Área de log profesional
        log_frame = ttk.Labelframe(
            container,
            text="  📋 Activity Log  ",
            padding=15,
            bootstyle="dark"
        )
        log_frame.pack(fill="both", expand=True)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(log_frame, bootstyle="dark-round")
        scrollbar.pack(side="right", fill="y")
        
        self.log_text = ttk.Text(
            log_frame,
            height=8,
            font=("Consolas", 9),
            yscrollcommand=scrollbar.set,
            wrap="word"
        )
        self.log_text.pack(fill="both", expand=True)
        scrollbar.config(command=self.log_text.yview)
        
        # Footer profesional
        footer = ttk.Frame(self.window, bootstyle="primary")
        footer.pack(fill="x", side="bottom")
        
        footer_label = ttk.Label(
            footer,
            text="YouTube • TikTok • Instagram • Twitter • Facebook • Vimeo • 1000+ Sites",
            font=("Segoe UI", 9),
            bootstyle="inverse-secondary"
        )
        footer_label.pack(pady=12)
    
    def clear_placeholder(self, event):
        """Limpia el placeholder al hacer clic"""
        if self.url_entry.get() == "Paste video link here...":
            self.url_entry.delete(0, "end")
    
    def open_folder(self):
        """Abre la carpeta de descargas"""
        os.startfile(self.output_dir.absolute())
    
    def log(self, message):
        """Agrega mensaje al log"""
        self.log_text.insert("end", message + "\n")
        self.log_text.see("end")
        self.window.update()
    
    def update_status(self, message, style="secondary"):
        """Actualiza el label de estado"""
        self.status_label.config(text=message, bootstyle=style)
        self.window.update()
    
    def start_download(self):
        """Inicia la descarga"""
        url = self.url_entry.get().strip()
        
        if not url or url == "Paste video link here...":
            self.update_status("❌ Please enter a valid URL", "danger")
            return
        
        self.download_btn.config(state="disabled", text="⏳ Downloading...")
        self.progress_bar["value"] = 0
        self.log_text.delete("1.0", "end")
        
        thread = threading.Thread(target=self.download_video, args=(url,))
        thread.daemon = True
        thread.start()
    
    def download_video(self, url):
        """Descarga el video"""
        quality = self.quality_var.get()
        
        # Configurar formato con FFmpeg
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
            self.log("=" * 60)
            self.log("🎬 STARTING DOWNLOAD")
            self.log("=" * 60)
            self.log(f"🔗 URL: {url}")
            self.log(f"📊 Quality: {quality}")
            self.log(f"📁 Destination: {self.output_dir.absolute()}")
            self.log("")
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                title = info.get('title', 'video')
                duration = info.get('duration', 0)
                
                self.log(f"📹 Title: {title}")
                if duration:
                    mins = duration // 60
                    secs = duration % 60
                    self.log(f"⏱️ Duration: {mins}:{secs:02d}")
                self.log("")
                self.log("⬇️ Downloading...")
                
                ydl.download([url])
            
            self.window.after(0, lambda: self.update_status("✅ Download completed successfully!", "success"))
            self.log("")
            self.log("=" * 60)
            self.log("✅ DOWNLOAD COMPLETED")
            self.log("=" * 60)
            self.window.after(0, lambda: self.progress_bar.config(value=100))
            
        except Exception as e:
            error_msg = str(e)
            self.window.after(0, lambda: self.update_status(f"❌ Error: {error_msg}", "danger"))
            self.log(f"\n❌ ERROR: {error_msg}")
        
        finally:
            self.window.after(0, lambda: self.download_btn.config(
                state="normal",
                text="⬇️  DOWNLOAD VIDEO"
            ))
    
    def progress_hook(self, d):
        """Hook para actualizar progreso"""
        if d['status'] == 'downloading':
            try:
                if 'total_bytes' in d:
                    percent = (d['downloaded_bytes'] / d['total_bytes']) * 100
                elif 'total_bytes_estimate' in d:
                    percent = (d['downloaded_bytes'] / d['total_bytes_estimate']) * 100
                else:
                    percent = 0
                
                self.window.after(0, lambda p=percent: self.progress_bar.config(value=p))
                
                percent_str = d.get('_percent_str', 'N/A')
                speed_str = d.get('_speed_str', 'N/A')
                eta_str = d.get('_eta_str', 'N/A')
                
                status = f"⬇️ {percent_str} | 🚀 {speed_str} | ⏱️ ETA: {eta_str}"
                self.window.after(0, lambda s=status: self.update_status(s, "info"))
                
            except Exception:
                pass
        
        elif d['status'] == 'finished':
            self.window.after(0, lambda: self.update_status("🔄 Processing and converting...", "warning"))
    
    def run(self):
        """Ejecuta la aplicación"""
        self.window.mainloop()


if __name__ == "__main__":
    app = ModernVideoDownloader()
    app.run()
