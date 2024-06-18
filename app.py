import streamlit as st
from pytube import YouTube
from io import BytesIO
from pathlib import Path
import requests
from PIL import Image
from mutagen.mp3 import MP3, EasyMP3
from mutagen.id3 import ID3, APIC, TIT2, TPE1
import tempfile
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
    temp_cover = tempfile.NamedTemporaryFile(delete=False)
    img.save(temp_cover.name, format='JPEG')
    temp_cover.close()

    return nombre_archivo, buffer, temp_cover.name, youtube_video

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
                # Crear archivo MP3 con metadatos
                audio_file = nombre_archivo + ".mp3"
                audio = MP3(buffer)

                # Añadir metadatos al archivo MP3
                audio.add_tags()
                audio.tags.add(TIT2(encoding=3, text=titulo_video))
                if youtube_video.author:
                    audio.tags.add(TPE1(encoding=3, text=youtube_video.author))

                # Añadir carátula al archivo MP3
                with open(cover_path, 'rb') as f:
                    audio.tags.add(
                        APIC(
                            encoding=3,
                            mime='image/jpeg',
                            type=3,
                            desc='Cover',
                            data=f.read()
                        )
                    )

                # Guardar el archivo MP3
                audio.save(audio_file)

                # Descargar el archivo MP3
                st.markdown(get_binary_file_downloader_html(audio_file, 'Audio MP3'), unsafe_allow_html=True)

                # Eliminar el archivo temporal de la carátula
                try:
                    os.remove(cover_path)
                except Exception as e:
                    st.warning(f"No se pudo eliminar el archivo temporal de la carátula: {e}")

            except Exception as e:
                st.error(f"Error al crear el archivo MP3: {e}")

def get_binary_file_downloader_html(bin_file, file_label='File'):
    with open(bin_file, 'rb') as f:
        data = f.read()
    b64 = base64.b64encode(data).decode()
    href = f'<a href="data:application/octet-stream;base64,{b64}" download="{Path(bin_file).name}">Descargar {file_label}</a>'
    return href

if __name__ == "__main__":
    main()
