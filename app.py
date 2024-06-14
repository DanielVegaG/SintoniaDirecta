import streamlit as st
from pytube import YouTube

import base64
import os

def clear_text():
    st.session_state["url"] = ""
    st.session_state["mime"] = ""
    st.session_state["quality"] = ""

def download_file(stream, fmt):
    """Descarga el archivo seleccionado."""
    if fmt == 'audio':
        # Descargar como mp3 si es audio
        title = stream.title + '.mp3'
        audio_stream = stream.streams.get_audio_only(subtype='mp4')
        audio_stream.download(filename=title)
    else:
        # Descargar como mp4 si es video
        title = stream.title + '.mp4'
        stream.download(filename=title)
    
    if 'DESKTOP_SESSION' not in os.environ:
        # Mostrar enlace de descarga si no está en sesión de escritorio
        with open(title, 'rb') as f:
            bytes = f.read()
            b64 = base64.b64encode(bytes).decode()
            href = f'<a href="data:file/zip;base64,{b64}" download=\'{title}\'>\
                Si le das a este link, se te descargará tu canción \
            </a>'
            st.markdown(href, unsafe_allow_html=True)

        os.remove(title)

def can_access(url):
    """Verifica si se puede acceder al video."""
    access = False
    if len(url) > 0:
        try:
            tube = YouTube(url)
            if tube.check_availability() is None:
                access = True
        except:
            pass
    return access

def refine_format(fmt_type: str='audio') -> (str, bool):
    """Refina el tipo de formato seleccionado."""
    if fmt_type == 'video':
        fmt = 'video'
        progressive = True
    else:
        fmt = 'audio'
        progressive = False

    return fmt, progressive

st.set_page_config(page_title=" Sintonía Directa", layout="wide")

# Sidebar
with st.sidebar:
    st.title("Descargador de música de YouTube")
    url = st.text_input("Pon aquí el enlace:", key="url")

    fmt_type = st.selectbox("Escoge el formato:", ['audio (only)', 'video'], key='fmt')
    fmt, progressive = refine_format(fmt_type)

    if can_access(url):
        tube = YouTube(url)
        streams_fmt = [t for t in tube.streams if t.type == fmt and t.is_progressive == progressive]

        mime_types = set([t.mime_type for t in streams_fmt])
        mime_type = st.selectbox("Mime types:", mime_types, key='mime')

        streams_mime = tube.streams.filter(only_audio=True, subtype='mp4')

        # Calidad promedio para audio y resolución para video
        if fmt == 'audio':
            quality = set([t.abr for t in streams_mime])
            quality_type = st.selectbox('Elige el bitrate promedio: ', quality, key='quality')
            stream_quality = tube.streams.filter(abr=quality_type)
        elif fmt == 'video':
            resolucion streams mimeType
