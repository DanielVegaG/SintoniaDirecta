import os
import yt_dlp

def get_downloads_directory():
    """Obtiene el directorio 'Descargas' para diferentes sistemas operativos."""
    return os.path.join(os.path.expanduser("~"), "Downloads")

def download_playlist(url, output_path=None, format='mp3'):
    """ Descarga una lista de reproducción de YouTube """
    if output_path is None:
        output_path = get_downloads_directory()

    ydl_opts = {
        'format': 'ba',  # 'ba' for best audio
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': format,  # audio format
        }, {
            'key': 'FFmpegMetadata'  # Añadir metadatos con FFmpeg
        }, {
            'key': 'EmbedThumbnail'  # Incrustar carátulas
        }],
        'outtmpl': os.path.join(output_path, '%(uploader)s', '%(title)s.%(ext)s'),
        'writethumbnail': True,  # Descargar carátulas
        'extractaudio': True,  # extract audio
        'audioformat': format,  # formato de audio
        'merge_output_format': None,  # disable merging audio and video
        'noplaylist': False,  # Activar la descarga de listas de reproducción
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

def download_single_video(url, output_path=None, format='mp4'):
    """ Descarga un video de YouTube """
    if output_path is None:
        output_path = get_downloads_directory()

    ydl_opts = {
        'format': 'bestvideo[ext='+format+']+bestaudio[ext=mp4]/best[ext='+format+']/best',
        'outtmpl': os.path.join(output_path, '%(uploader)s', '%(title)s.%(ext)s'),
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

# Función adicional para verificar acceso al URL
def can_access(url):
    # Lógica para verificar si el URL es accesible
    return True  # Implementa tu lógica según necesidades específicas
