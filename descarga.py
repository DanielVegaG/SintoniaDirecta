import os
import yt_dlp
import tempfile
import shutil
from io import BytesIO

def get_downloads_directory():
    """Obtiene el directorio 'Descargas' para diferentes sistemas operativos."""
    return os.path.join(os.path.expanduser("~"), "Downloads")

def download_audio_to_buffer(url):
    """
    Descarga un audio desde YouTube y lo guarda en un buffer de memoria.
    """
    try:
        # Crear un archivo temporal
        temp_dir = tempfile.mkdtemp()
        temp_filename = os.path.join(temp_dir, "audio")

        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': temp_filename + '.%(ext)s',  # Guardamos el archivo temporalmente en disco
            'postprocessors': [
                {'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3'},  # Extraemos como mp3
                {'key': 'FFmpegMetadata'},  # Añadir metadatos al archivo
                {'key': 'EmbedThumbnail', 'already_have_thumbnail': False},  # Incrustar carátula
            ],
            'writethumbnail': True,  # Descargar carátulas
            'cookiefile': 'cookies.txt',
            'quiet': True,
            'noplaylist': True,  # Evitar que descargue listas de reproducción
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            data = ydl.extract_info(url, download=False)  # Obtener la información sin descargar
            titulo_original = data.get('title', 'sin_título')
            artista = data.get('uploader', 'desconocido')

            # Descargar el archivo con los metadatos añadidos
            ydl.download([url])

        # Cargar el archivo descargado en el buffer
        with open(temp_filename + '.mp3', 'rb') as f:
            buffer = BytesIO(f.read())
        
        # Limpiar el archivo temporal después de usarlo
        shutil.rmtree(temp_dir)

        return titulo_original, artista, buffer

    except Exception as e:
        raise Exception(f"Error durante la descarga: {e}")