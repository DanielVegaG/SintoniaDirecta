import streamlit as st
from pytube import YouTube
import os

def clear_text():
    st.session_state["url"] = ""

def download_file(stream, fmt):
    if fmt == 'audio':
        title = stream.title + '.mp3'
    else:
        title = stream.title + '.mp4'

    stream.download(filename=title)

    if 'DESKTOP_SESSION' not in os.environ:
        st.success(f'Archivo descargado: {title}')

def can_access(url):
    access = False
    if len(url) > 0:
        try:
            tube = YouTube(url)
            if tube.check_availability() is None:
                access = True
        except Exception as e:
            st.error(f"Error: {e}")
    return access

st.set_page_config(page_title="Sintonía Directa", layout="wide")

# Sidebar
with st.sidebar:
    st.title("Descargador de música y vídeos de YouTube")
    url = st.text_input("Pon aquí el enlace:", key="url")

# Main page
if can_access(url):
    try:
        tube = YouTube(url)

        st.write(f"Video: {tube.title}")
        
        # Descarga de audio o video
        if st.button("Descargar", key="download"):
            # Si es audio
            if tube.streams.filter(only_audio=True, file_extension='mp4'):
                stream = tube.streams.filter(only_audio=True, file_extension='mp4').first()
                download_file(stream, 'audio')
            # Si es video
            elif tube.streams.filter(only_video=True, file_extension='mp4'):
                stream = tube.streams.filter(only_video=True, file_extension='mp4').first()
                download_file(stream, 'video')
            else:
                st.warning("No se encontraron streams de audio o video disponibles.")
    except Exception as e:
        st.error(f"Error: {e}")
