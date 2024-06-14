#################### Archivo adicional donde están los métodos necesarios para la descarga
import base64
import os
from pytube import YouTube

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
