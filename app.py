import streamlit as st
from pytube import YouTube
from io import BytesIO
from urllib.parse import unquote
import re

st.set_page_config(page_title="Descargar Video", page_icon="icon.png", layout="centered", initial_sidebar_state="collapsed")

@st.cache_data(show_spinner=False)
def descargar_video_a_buffer(url, formato):
    buffer = BytesIO()
    youtube_video = YouTube(url)
    
    # Obtener el título original del video y decodificar caracteres especiales
    titulo_original = unquote(youtube_video.title)
    
    if formato == 'mp3':
        video = youtube_video.streams.filter(only_audio=True).first()
    else:
        video = youtube_video.streams.filter(progressive=True, file_extension="mp4").order_by('resolution').desc().first()

    nombre_archivo = video.default_filename
    video.stream_to_buffer(buffer)
    return titulo_original, buffer

def clean_filename(filename):
    # Remove invalid characters for filenames in Windows
    return re.sub(r'[<>:"/\\|?*]', '', filename)

def main():
    st.title("Descargar video desde YouTube")
    url = st.text_input("Inserta la URL de YouTube:")
    formato = st.radio("Selecciona el formato de descarga:", ('MP3', 'MP4'))

    if url:
        with st.spinner(f"Descargando stream de {'audio' if formato == 'MP3' else 'video'} desde YouTube..."):
            titulo_original, buffer = descargar_video_a_buffer(url, formato.lower())
        
        st.subheader("Título")
        st.write(titulo_original)
        
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

if __name__ == "__main__":
    main()
