import streamlit as st
from descarga import download_playlist, download_single_video, can_access, get_downloads_directory

def main():
    st.title("Descargador de YouTube")

    url = st.text_input("Introduce la URL de YouTube:")
    download_type = st.selectbox("Selecciona el tipo de descarga:", ["Canción individual", "Lista de reproducción"])
    download_format = st.selectbox("Selecciona el formato de descarga:", ["MP3", "MP4"])

    format_code = "mp3" if download_format == "MP3" else "mp4"
    output_directory = get_downloads_directory()  # Usamos el directorio de 'Descargas'

    if can_access(url):
        try:
            if download_type == "Lista de reproducción":
                download_playlist(url, output_directory, format=format_code)
            elif download_type == "Canción individual":
                download_single_video(url, output_directory, format=format_code)

            download_button_text = f"Descargar {download_type} ({download_format})"
            st.download_button(download_button_text, key='download_button')
            st.success("¡Descarga completada!")
        except Exception as e:
            st.error(f"Ocurrió un error durante la descarga: {e}")
    else:
        st.error("No se puede acceder al URL proporcionado.")

if __name__ == "__main__":
    main()
