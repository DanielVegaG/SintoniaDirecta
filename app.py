import streamlit as st
from pytube import YouTube
from io import BytesIO
from pathlib import Path
import requests
from PIL import Image
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC, TIT2, TPE1
import os
import base64

st.set_page_config(page_title="Descargar Video", page_icon="icon.png", layout="centered", initial_sidebar_state="collapsed")

@st.cache_data(show_spinner=False)
def descargar_video_a_buffer(url):
    buffer = BytesIO()
    youtube_video = YouTube(url)
    video = youtube_video.streams.filter(progressive=True, file_extension="mp4").order_by('resolution').desc()
    video_720p = video[0]
    nombre_archivo = video_720p.default_filename
    video_720p.stream_to_buffer(buffer)

    # Descargar carátula
    response = requests.get(youtube_video.thumbnail_url)
    img = Image.open(BytesIO(response.content))
    img = img.convert('RGB')

    # Guardar carátula temporalmente
    temp_cover = os.path.join(get_temp_directory(), "cover.jpg")
    img.save(temp_cover, format='JPEG')

    return nombre_archivo, buffer, temp_cover, youtube_video

def add_metadata_to_mp3(file_path, cover_path, song_title, artist):
    try:
        audio = MP3(file_path, ID3=ID3)
    except:
        audio = MP3(file_path)
        audio.add_tags()

    audio.tags.add(TIT2(encoding=3, text=song_title))
    audio.tags.add(TPE1(encoding=3, text=artist))

    # Añadir carátula
    with open(cover_path, 'rb') as f:
        audio.tags.add(
            APIC(
                encoding=3,  # UTF-8
                mime='image/jpeg',  # image/jpeg or image/png
                type=3,  # Cover (front) image
                desc=u'Cover',
                data=f.read()
            )
        )

    audio.save(v2_version=3)

def main():
    st.title("Descargar video desde YouTube")
    url = st.text_input("Inserta la URL de YouTube:")
    if url:
        with st.spinner("Descargando stream de video desde YouTube..."):
            nombre_archivo, buffer, cover_path, youtube_video = descargar_video_a_buffer(url)

        st.subheader("Título")
        st.write(nombre_archivo)

        # Obtener el nombre del archivo sin extensión
        titulo_video = Path(nombre_archivo).stem

        st.subheader("Ver video")
        st.video(buffer, format='video/mp4')

        st.subheader("Descargar Archivo de Audio")

        # Descargar botón para MP4
        st.download_button(
            label="Descargar MP4",
            data=buffer,
            file_name=nombre_archivo,
            mime="video/mp4"
        )

        # Descargar botón para MP3 con metadatos
        if st.button("Descargar MP3 con Metadatos"):
            st.write("Descargando MP3 con metadatos...")

            try:
                # Guardar el buffer en un archivo temporal
                temp_audio_file = os.path.join(get_temp_directory(), f"{titulo_video}.mp3")
                with open(temp_audio_file, 'wb') as f:
                    f.write(buffer.getvalue())

                # Agregar metadatos al archivo MP3
                add_metadata_to_mp3(temp_audio_file, cover_path, titulo_video, youtube_video.author)

                # Descargar el archivo MP3
                st.markdown(get_binary_file_downloader_html(temp_audio_file, 'Audio MP3'), unsafe_allow_html=True)

            except Exception as e:
                st.error(f"Error al crear el archivo MP3: {e}")

            finally:
                # Eliminar archivos temporales
                try:
                    os.remove(temp_audio_file)
                    os.remove(cover_path)
                except Exception as e:
                    st.warning(f"No se pudo eliminar el archivo temporal: {e}")

def get_temp_directory():
    """Obtiene el directorio temporal."""
    return os.path.join(st._uploaded_file_manager._get_base_folder_path(), "temp")

def get_binary_file_downloader_html(bin_file, file_label='File'):
    with open(bin_file, 'rb') as f:
        data = f.read()
    b64 = base64.b64encode(data).decode()
    href = f'<a href="data:application/octet-stream;base64,{b64}" download="{Path(bin_file).name}">Descargar {file_label}</a>'
    return href

if __name__ == "__main__":
    main()
