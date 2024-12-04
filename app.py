import streamlit as st
from pytube import YouTube
import yt_dlp
from io import BytesIO
from urllib.parse import unquote
import re
import tempfile
import shutil

st.set_page_config(page_title="Descargar Video", page_icon="icon.png", layout="centered", initial_sidebar_state="collapsed")

@st.cache_data(show_spinner=False)
def descargar_video_a_buffer(url, formato):
    """
    Descarga un video o audio desde YouTube y lo guarda en un buffer de memoria.
    """
    try:
        # Crear un archivo temporal
        temp_dir = tempfile.mkdtemp()
        temp_filename = os.path.join(temp_dir, "audio_o_video")

        ydl_opts = {
            'format': 'bestaudio/best' if formato == 'mp3' else 'bestvideo+bestaudio/best',
            'outtmpl': temp_filename + '.%(ext)s',  # Guardamos el archivo temporalmente en disco
            'postprocessors': [
                {'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3'} if formato == 'mp3' else {},
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
        st.error(f"Error durante la descarga: {e}")
        raise e
def clean_filename(filename):
    # Remove invalid characters for filenames in Windows
    return re.sub(r'[<>:"/\\|?*]', '', filename)

def main():
    try:
        st.title("Descargar video desde YouTube")
        url = st.text_input("Inserta la URL de YouTube:")
        formato = st.radio("Selecciona el formato de descarga:", ('MP3', 'MP4'))

        if url:
            with st.spinner(f"Descargando stream de {'audio' if formato == 'MP3' else 'video'} desde YouTube..."):
                titulo_original, artista, buffer = descargar_video_a_buffer(url, formato.lower())

            st.subheader("Título")
            st.write(f"🎵 **Título**: {titulo_original}")
            if formato == 'MP3':
                st.write(f"👤 **Artista**: {artista}")

            if formato == 'MP3':
                titulo_audio = clean_filename(titulo_original) + ".mp3"
                st.subheader("Descargar Archivo de Audio (MP3)")
                st.download_button(
                    label="Descargar MP3",
                    data=buffer,
                    file_name=titulo_audio,
                    mime="audio/mpeg"
                )
            else:
                titulo_video = clean_filename(titulo_original) + ".mp4"
                st.subheader("Ver video")
                st.video(buffer, format='video/mp4')
                st.subheader("Descargar Archivo de Video (MP4)")
                st.download_button(
                    label="Descargar MP4",
                    data=buffer,
                    file_name=titulo_video,
                    mime="video/mp4"
                )
    except Exception as e:
        st.error(f"Error inesperado: {e}")

if __name__ == "__main__":
    main()
