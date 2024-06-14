import subprocess
import ffmpeg
import streamlit as st
import os
import yt_dlp

# Global variables
downloaded_mp3_file = None
downloaded_mp3_filename = None

# Función para descargar y convertir el video de YouTube a MP3 usando yt_dlp y ffmpeg
def download_and_convert_to_mp3(url):
    global downloaded_mp3_file, downloaded_mp3_filename

    # Directorio de salida para los archivos descargados
    output_dir = './downloads'
    os.makedirs(output_dir, exist_ok=True)

    # Ruta a los ejecutables de FFmpeg
    ffmpeg_dir = os.path.abspath('./ffmpeg')
    ffmpeg_location = os.path.join(ffmpeg_dir, 'ffmpeg.exe')
    ffprobe_location = os.path.join(ffmpeg_dir, 'ffprobe.exe')

    # Opciones para descargar y convertir el audio
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
        'ffmpeg_location': ffmpeg_location,
        'ffprobe_location': ffprobe_location,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            video_title = info_dict.get('title', 'video')
            downloaded_mp3_filename = f"{video_title}.mp3"
            downloaded_mp3_file = os.path.join(output_dir, downloaded_mp3_filename)
        return True
    except Exception as e:
        st.error(f'Error during download and conversion: {str(e)}')
        return False

# Función para convertir el archivo MP3 a WAV usando ffmpeg
@st.cache(allow_output_mutation=True)
def convert_mp3_to_wav(input_file):
    output_file = input_file.replace('.mp3', '.wav')

    ffmpeg.input(input_file).output(output_file).run(overwrite_output=True, quiet=True)

    with open(output_file, 'rb') as f:
        wav_bytes = f.read()
    
    os.remove(output_file)  # Eliminar el archivo WAV después de la conversión

    return wav_bytes

# App principal de Streamlit
if __name__ == '__main__':
    st.title('YouTube to MP3 Downloader and Converter')

    # Entrada de la URL de YouTube
    url = st.text_input('Enter YouTube URL:')
    
    if st.button('Download and Convert to MP3'):
        if url:
            if download_and_convert_to_mp3(url):
                st.success(f'Successfully downloaded and converted: {downloaded_mp3_filename}')
            else:
                st.error('Failed to download and convert the video.')

    if downloaded_mp3_file:
        st.markdown('---')
        st.subheader('Download Converted MP3 as WAV')
        st.audio(downloaded_mp3_file, format='audio/mp3')
        st.markdown('---')

        if st.button('Convert MP3 to WAV'):
            wav_bytes = convert_mp3_to_wav(downloaded_mp3_file)
            st.audio(wav_bytes, format='audio/wav', start_time=0)

