import streamlit as st
from descarga import download_audio_to_buffer  # Importa la función de descarga desde descarga.py
import re

st.set_page_config(page_title="Descargar Audio", page_icon="icon.png", layout="centered", initial_sidebar_state="collapsed")

def clean_filename(filename):
    """Eliminar caracteres no válidos para nombres de archivos en Windows."""
    return re.sub(r'[<>:"/\\|?*]', '', filename)

def main():
    try:
        st.title("Descargar Audio desde YouTube")
        url = st.text_input("Inserta la URL de YouTube:")

        if url:
            with st.spinner("Descargando audio desde YouTube..."):
                titulo_original, artista, buffer = download_audio_to_buffer(url)

            st.subheader("Título")
            st.write(f"🎵 **Título**: {titulo_original}")
            st.write(f"👤 **Artista**: {artista}")

            titulo_audio = clean_filename(titulo_original) + ".mp3"
            st.subheader("Descargar Archivo de Audio (MP3)")
            st.download_button(
                label="Descargar MP3",
                data=buffer,
                file_name=titulo_audio,
                mime="audio/mpeg"
            )

    except Exception as e:
        st.error(f"Error inesperado: {e}")

if __name__ == "__main__":
    main()