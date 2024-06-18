import streamlit as st
import base64
import os
from pytube import YouTube
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC, TIT2, TPE1
from PIL import Image
import ffmpeg
import requests
from io import BytesIO

def download_file(stream, fmt):
    """ Pone el nombre del archivo al descargarlo
            -.mp3 para audios
            -.mp4 para vídeos """
    if fmt == 'audio':
        title = stream.title + '.webm'
        title_mp3 = stream.title + '.mp3'
    else:
        title = stream.title + '.mp4'

    stream.download(filename=title)
    
    if fmt == 'audio':
        # Convertir webm a mp3 usando ffmpeg-python
        try:
            ffmpeg.input(title).output(title_mp3, **{'vn': True, 'ab': '192k', 'ar': 44100, 'y': None}).run(overwrite_output=True)
            os.remove(title)  # Eliminar el archivo original .webm
            add_metadata(title_mp3, stream)
            title = title_mp3  # Actualizar el nombre del archivo a .mp3
        except Exception as e:
            st.error(f"Error al convertir el archivo: {e}")
            return
    
    if 'DESKTOP_SESSION' not in os.environ:  # comprobar que se ve desde un navegador
        try:
            with open(title, 'rb') as f:
                bytes = f.read()
                b64 = base64.b64encode(bytes).decode()
                href = f'<a href="data:application/octet-stream;base64,{b64}" download="{title}">\
                    Haz clic aquí para descargar {title} \
                </a>'
                st.markdown(href, unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Error al crear el enlace de descarga: {e}")
        finally:
            if os.path.exists(title):
                os.remove(title)

def add_metadata(file_path, stream):
    """ Añadir metadatos al archivo de audio """
    try:
        audio = MP3(file_path, ID3=ID3)
        
        # Añadir título y artista
        audio['TIT2'] = TIT2(encoding=3, text=stream.title)
        audio['TPE1'] = TPE1(encoding=3, text=stream.author)
        
        # Descargar y añadir carátula
        response = requests.get(stream.thumbnail_url)
        img = Image.open(BytesIO(response.content))
        img.save("cover.jpg")
        
        with open("cover.jpg", "rb") as img_file:
            audio.tags.add(
                APIC(
                    encoding=3,  # 3 is for utf-8
                    mime="image/jpeg",
                    type=3,  # 3 is for the cover image
                    desc="Cover",
                    data=img_file.read()
                )
            )
        audio.save()
        os.remove("cover.jpg")
    except Exception as e:
        st.error(f"Error al añadir metadatos: {e}")

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

from typing import Tuple

def refine_format(fmt_type: str='audio') -> Tuple[str, bool]:
    """ Refinar el formato del archivo basándose en el tipo que se haya seleccionado"""
    if fmt_type == 'video':
        fmt = 'video'
        progressive = True
    else:
        fmt = 'audio'
        progressive = False

    return fmt, progressive
