from pytube import YouTube
import os
import streamlit as st

# Configuración de página y barra lateral
st.set_page_config(page_title='Descargador de YouTube', page_icon='icon.png', layout='centered', initial_sidebar_state='collapsed')

# Barra lateral con opciones
st.sidebar.title('YouTube Downloader')

add_selectbox = st.sidebar.selectbox(
    "Selecciona qué deseas descargar",
    ("Audio", "Video")
)


def Download():
    st.header("Descargador de YouTube")

    if add_selectbox == 'Video':
        # Entrada de URL de YouTube
        youtube_url = st.text_input("Ingresa la URL de YouTube")

        # Selección de resolución del video
        genre = st.radio(
            "Selecciona la resolución que deseas descargar",
            ["Mejor Resolución", "720p", "480p", "360p", "240p", "144p"]
        )

        # Botón de descarga del video
        if st.button("Descargar video"):
            try:
                youtubeObject = YouTube(youtube_url)

                if genre == "Mejor Resolución":
                    youtubeObject = youtubeObject.streams.get_highest_resolution()
                elif genre == "720p":
                    youtubeObject = youtubeObject.streams.get_by_resolution("720p")
                elif genre == "480p":
                    youtubeObject = youtubeObject.streams.get_by_resolution("480p")
                elif genre == "360p":
                    youtubeObject = youtubeObject.streams.get_by_resolution("360p")
                else:
                    youtubeObject = youtubeObject.streams.get_by_resolution("144p")

                # Directorio de salida para descarga de videos
                save_dir = 'output/videos/'
                os.makedirs(save_dir, exist_ok=True)
                youtubeObject.download(output_path=save_dir)
                st.success(f"Descarga del video '{youtubeObject.title}' completada exitosamente en '{save_dir}'.")
                st.info("Revisa la carpeta 'output/videos/' para encontrar el archivo descargado.")

            except Exception as e:
                st.error(f"Ha ocurrido un error: {e}")

    elif add_selectbox == 'Audio':
        # Entrada de URL de YouTube para descarga de audio
        youtube_url = st.text_input("Ingresa la URL de YouTube")

        # Botón de descarga de audio
        if st.button("Descargar audio"):
            try:
                youtubeObject = YouTube(youtube_url)
                audio = youtubeObject.streams.filter(only_audio=True).first()

                # Directorio de salida para descarga de audio
                save_dir = 'output/audios/'
                os.makedirs(save_dir, exist_ok=True)
                audio.download(output_path=save_dir)
                st.success(f"Descarga del audio '{audio.title}' completada exitosamente en '{save_dir}'.")
                st.info("Revisa la carpeta 'output/audios/' para encontrar el archivo descargado.")

            except Exception as e:
                st.error(f"Ha ocurrido un error: {e}")

if __name__ == '__main__':
    Download()
