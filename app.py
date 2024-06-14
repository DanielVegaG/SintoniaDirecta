import streamlit as st
import requests
from pytube import YouTube, StreamQuery

import base64
import os

def clear_text():
    st.session_state["url"] = ""
    st.session_state["mime"] = ""
    st.session_state["quality"] = ""

def download_file(stream, fmt):
    """  """
    if fmt == 'audio':
        title = stream.title + '.mp3'
    else:
        title = stream.title + '.mp4'

    stream.download(filename=title)
    
    if 'DESKTOP_SESSION' not in os.environ:
    
        with open(title, 'rb') as f:
            bytes = f.read()
            b64 = base64.b64encode(bytes).decode()
            href = f'<a href="data:file/zip;base64,{b64}" download=\'{title}\'>\
                Si le das a este link, se te descargará tu canción \
            </a>'
            st.markdown(href, unsafe_allow_html=True)

        os.remove(title)


def can_access(url):
    """ check whether you can access the video """
    access = False
    if len(url) > 0:
        try:
            tube = YouTube(url)
            if tube.check_availability() is None:
                access=True
        except:
            pass
    return access

def refine_format(fmt_type: str='audio') -> (str, bool):
    """ """
    if fmt_type == 'video':
        fmt = 'video'
        progressive = True
    else:
        fmt = 'audio'
        progressive = False

    return fmt, progressive


st.set_page_config(page_title=" Sintonía Directa", layout="wide")

# ====== SIDEBAR ======
with st.sidebar:

    st.title("Descargador de música de YouTube")

    url = st.text_input("Pon aquí el enlace:", key="url")

    fmt_type = st.selectbox("Escoge el formato:", ['audio (only)', 'video'], key='fmt')

    fmt, progressive = refine_format(fmt_type)

    if can_access(url):

        tube = YouTube(url)

        streams_fmt = [t for t in tube.streams if t.type==fmt and t.is_progressive==progressive]

        mime_types = set([t.mime_type for t in streams_fmt])
        mime_type = st.selectbox("Mime types:", mime_types, key='mime')

        streams_mime = StreamQuery(streams_fmt).filter(mime_type=mime_type)

        # quality is average bitrate for audio and resolution for video
        if fmt=='audio':
            quality = set([t.abr for t in streams_mime])
            quality_type = st.selectbox('Choose average bitrate: ', quality, key='quality')
            stream_quality = StreamQuery(streams_mime).filter(abr=quality_type)
        elif fmt=='video':
            quality = set([t.resolution for t in streams_mime])
            quality_type = st.selectbox('Choose resolution: ', quality, key='quality')
            stream_quality = StreamQuery(streams_mime).filter(res=quality_type)

        # === Download block === #
        if stream_quality is not None:
            stream_final = stream_quality[0]
            if 'DESKTOP_SESSION' in os.environ:
                download = st.button("Descargar canción", key='download')
            else:
                download = st.button("Get download link", key='download')

            if download:
                download_file(stream_final, fmt)
                st.success('Success download!')
                st.balloons()

        st.button("Clear all address boxes", on_click=clear_text)


# ====== MAIN PAGE ======

if can_access(url):
    if streams_fmt is None:
        st.write(f"No {fmt_type} stream found")
    st.video(url)