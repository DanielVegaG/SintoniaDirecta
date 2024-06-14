import streamlit as st
from pytube import YouTube
from descarga import download_file, can_access, refine_format

st.set_page_config(page_title="Sintonía Directa", page_icon="icon.png", layout="wide")

def main():
    st.title("Descargador de música de YouTube")
    url = st.text_input("Pon aquí el enlace:", key="url")
    fmt_type = st.selectbox("Escoge el formato:", ['Audio', 'Vídeo'], key='fmt')

    fmt, progressive = refine_format(fmt_type)

    if can_access(url):
        tube = YouTube(url)

        streams_fmt = [t for t in tube.streams if t.type == fmt and t.is_progressive == progressive]

        if fmt == 'audio':
            # Selecciona el stream de audio con la mayor tasa de bits disponible
            stream_quality = max(streams_fmt, key=lambda s: s.abr)
        elif fmt == 'video':
            # Selecciona el stream de vídeo con la mayor resolución disponible
            stream_quality = max(streams_fmt, key=lambda s: s.resolution)

        # === Bloque que descarga === #
        if stream_quality:
            stream_final = stream_quality
            download = st.button("Obtener canción", key='download')

            if download:
                st.success('¡Obtención exitosa!')
                download_file(stream_final, fmt)
                st.balloons()

    if can_access(url):
        '''Aquí se pone la imagen del vídeo de youtube'''
        if not streams_fmt:
            st.write(f"No se encontró flujo de {fmt_type}")
        st.video(url)

if __name__ == "__main__":
    main()
