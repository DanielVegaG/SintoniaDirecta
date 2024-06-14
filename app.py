import streamlit as st
from pytube import YouTube

import base64
import os

def download_file(stream, fmt):
    """ Pone el nombre del archivo al descargarlo
            -.mp3 para audios
            -.mp4 para vídeos """
    if fmt == 'audio':
        title = stream.title + '.mp3'
    else:
        title = stream.title + '.mp4'

    stream.download(filename=title)
    
    if 'DESKTOP_SESSION' not in os.environ: #comprobar que se ve desde un navegador
        with open(title, 'rb') as f:
            bytes = f.read()
            b64 = base64.b64encode(bytes).decode()
            href = f'<a href="data:file/zip;base64,{b64}" download=\'{title}\'>\
                Haz clic aquí para descargar {title} \
            </a>'
            st.markdown(href, unsafe_allow_html=True)

        os.remove(title)

def can_access(url):
    """ Comprueba si es posible acceder al vídeo """
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
    """ Refinar el formato del archivo basándose en el tipo que se haya seleccionado"""
    if fmt_type == 'video':
        fmt = 'video'
        progressive = True
    else:
        fmt = 'audio'
        progressive = False

    return fmt, progressive

st.set_page_config(page_title="Sintonía Directa", page_icon="icon.png",layout="wide")

st.title("Descargador de música de YouTube")
url = st.text_input("Pon aquí el enlace:", key="url")
fmt_type = st.selectbox("Escoge el formato:", ['Audio', 'Vídeo'], key='fmt')

fmt, progressive = refine_format(fmt_type)

if can_access(url):
    tube = YouTube(url)

    streams_fmt = [t for t in tube.streams if t.type == fmt and t.is_progressive == progressive]

    if fmt == 'audio':
        # Selecciona el stream de audio con la mayor tasa de bits disponible
        stream_quality = max(streams_fmt, key=lambda s: s.abr)
    elif fmt == 'video':
        # Selecciona el stream de vídeo con la mayor resolución disponible
        stream_quality = max(streams_fmt, key=lambda s: s.resolution)

    # === Bloque que descarga === #
    if stream_quality:
        stream_final = stream_quality
        download = st.button("Obtener canción", key='download')

        if download:
            st.success('¡Obtención exitosa!')
            download_file(stream_final, fmt)
            st.balloons()

if can_access(url):
    '''Aquí se pone la imagen del vídeo de youtube'''
    if not streams_fmt:
        st.write(f"No se encontró flujo de {fmt_type}")
    st.video(url)
