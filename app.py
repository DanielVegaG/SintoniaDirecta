import streamlit as st
import base64
import os
from pytube import YouTube, StreamQuery

# Función para descargar y convertir el archivo de audio a MP3
def download_file(stream, fmt):
    if fmt == 'audio':
        title = stream.title + '.mp3'  # Cambiar la extensión a .mp3
        stream.download(filename=title)  # Descargar el archivo con extensión .mp3

        # Leer el archivo descargado y convertirlo a base64 para generar el enlace de descarga
        with open(title, 'rb') as f:
            bytes = f.read()
            b64 = base64.b64encode(bytes).decode()
            href = f'<a href="data:file/mp3;base64,{b64}" download=\'{title}\'>\
                Click aquí para descargar {title}\
            </a>'
            st.markdown(href, unsafe_allow_html=True)

        os.remove(title)  # Eliminar el archivo MP3 después de generar el enlace de descarga

# Configuración de la página de Streamlit
st.set_page_config(page_title="YouTube Downloader", layout="wide")

# Sidebar con los controles de la aplicación
with st.sidebar:
    st.title("Aplicación para descargar desde YouTube")

    # Entrada para la URL de YouTube
    url = st.text_input("Inserta el enlace aquí:", key="url")

    # Selección del tipo de formato a descargar
    fmt_type = st.selectbox("Elige el formato:", ['video (solo)', 'audio (solo)', 'video + audio'], key='fmt')

# Página principal donde se muestra el video de YouTube si la URL es válida
if url and YouTube(url).check_availability() is not None:
    st.video(url)

    tube = YouTube(url)
    streams_fmt = [t for t in tube.streams if t.type == 'audio' and t.is_progressive == False]

    mime_types = set([t.mime_type for t in streams_fmt])
    mime_type = st.selectbox("Tipos de MIME:", mime_types, key='mime')

    streams_mime = StreamQuery(streams_fmt).filter(mime_type=mime_type)

    # Calidad del audio basada en la tasa de bits promedio (abr)
    if fmt_type == 'audio (solo)':
        quality = set([t.abr for t in streams_mime])
        quality_type = st.selectbox('Elige la tasa de bits promedio:', quality, key='quality')
        stream_quality = StreamQuery(streams_mime).filter(abr=quality_type)

    # Botón para descargar el archivo
    if stream_quality is not None:
        stream_final = stream_quality[0]
        download = st.button("Descargar archivo", key='download')

        if download:
            download_file(stream_final, 'audio')
            st.success('¡Descarga exitosa!')
            st.balloons()
