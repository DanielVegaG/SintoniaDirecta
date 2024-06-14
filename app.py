import streamlit as st
import os
import yt_dlp

st.title('Downloader App')

url = st.text_input('Introduce la URL de YouTube:')
if url:
    output_dir = st.text_input('Directorio de salida:', './downloads')
    if st.button('Descargar'):        
        # Crear el directorio de salida si no existe
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        ffmpeg_dir = os.path.abspath('./ffmpeg')  # Ruta completa al directorio ffmpeg
        ffmpeg_location = os.path.join(ffmpeg_dir, 'ffmpeg.exe')  # Especificar el ejecutable con extensión .exe en Windows
        ffprobe_location = os.path.join(ffmpeg_dir, 'ffprobe.exe')  # Especificar el ejecutable con extensión .exe en Windows

        ydl_opts = {
            'format': 'ba',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
            }],
            'outtmpl': f'{output_dir}/%(title)s.%(ext)s',
            'extractaudio': True,
            'audioformat': 'mp3',
            'noplaylist': True,
            'nocache': True,  # Desactivar caché
            'ffmpeg_location': ffmpeg_location,  # Proveer la ruta completa de ffmpeg
            'ffprobe_location': ffprobe_location,  # Proveer la ruta completa de ffprobe
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            st.success(f'¡Descargado correctamente en {output_dir}!')
        except Exception as e:
            st.error(f'Error: {str(e)}')
