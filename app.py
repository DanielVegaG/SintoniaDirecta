import streamlit as st
from pytube import YouTube
from io import BytesIO
from pathlib import Path

st.set_page_config(page_title="Descargar Video", page_icon="icon.png", layout="centered", initial_sidebar_state="collapsed")

@st.cache_data(show_spinner=False)
def descargar_video_a_buffer(url, formato):
    buffer = BytesIO()
    youtube_video = YouTube(url)
    
    if formato == 'mp3':
        video = youtube_video.streams.filter(only_audio=True).first()
    else:
        video = youtube_video.streams.filter(progressive=True, file_extension="mp4").order_by('resolution').desc().first()

    nombre_archivo = video.default_filename
    video.stream_to_buffer(buffer)
    return nombre_archivo, buffer

def main():
    st.title("Descargar video desde YouTube")
    url = st.text_input("Inserta la URL de YouTube:")
    formato = st.radio("Selecciona el formato de descarga:", ('MP3', 'MP4'))

    if url:
        with st.spinner(f"Descargando stream de {'audio' if formato == 'MP3' else 'video'} desde YouTube..."):
            nombre_archivo, buffer = descargar_video_a_buffer(url, formato.lower())
        
        st.subheader("Título")
        st.write(nombre_archivo)
        
        if formato == 'MP3':
            titulo_audio = Path(nombre_archivo).with_suffix(".mp3").name
            st.subheader("Descargar Archivo de Audio (MP3)")
            st.download_button(
                label="Descargar MP3",
                data=buffer,
                file_name=titulo_audio,
                mime="audio/mpeg"
            )
        else:
            titulo_video = Path(nombre_archivo).with_suffix(".mp4").name
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
