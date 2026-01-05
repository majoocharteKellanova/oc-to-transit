# importar librerías necesarias
import streamlit as st
import pandas as pd
import io

# formatito
# estilos globales
st.markdown("""
<style>
@font-face {
    font-family: 'Gilroy';
    src: url('https://raw.githubusercontent.com/majoocharteKellanova/oc-to-transit/main/assets/gilroy-medium.ttf');
}

/* fondo degradado vino -> rojo */
html, body, [data-testid="stAppViewContainer"], [class*="block-container"] {
    background: linear-gradient(180deg, #7A1531 0%, #E2003E 100%) !important;
    color-scheme: light !important;
}

/* fuente global y texto negro */
*, div, span, section, button, label, input, textarea, h1, h2, h3, p {
    font-family: 'Gilroy', sans-serif !important;
    color: #000000 !important;
}

/* tarjeta blanca centrada */
div[data-testid="stVerticalBlock"] {
    background-color: #ffffff;
    border-radius: 20px;
    padding: 3rem 5rem;
    margin-top: 3rem;
    margin-bottom: 3rem;
    box-shadow: 0px 8px 24px rgba(0,0,0,0.25);
    width: 80%;
    max-width: 800px;
}

/* centrado total */
section[data-testid="stSidebar"] ~ div[data-testid="stAppViewContainer"] > .main {
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
}

/* título */
h1, h1 span, [data-testid="stMarkdownContainer"] h1 {
    color: #7A1531 !important;       /* vino */
    text-align: center !important;
    padding-bottom: 0.8em !important;
    font-weight: 800 !important;     /* más bold */
    font-size: 2.8rem !important;    /* más grande */
    letter-spacing: 1px !important;  /* espaciamiento */
    text-transform: none !important; /* o "uppercase" si lo quieres en mayúsculas */
}


/* subtítulos */
h2, h3 {
    color: #7A1531 !important;
    text-align: center;
}

/* uploader */
div[data-testid="stFileUploaderDropzone"] {
    background-color: #f7f7f7 !important;
    border: 2px dashed #3d5ee8;
    border-radius: 12px;
    color: #3d5ee8;
    transition: 0.3s;
}
div[data-testid="stFileUploaderDropzone"]:hover {
    background-color: #edf0ff !important;
}

/* texto uploader */
div[data-testid="stFileUploaderDropzone"] p {
    color: #3d5ee8 !important;
}

/* botón de subida */
div[data-testid="stFileUploader"] section div div button {
    background-color: #3d5ee8 !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: bold !important;
    padding: 0.5em 1.2em !important;
    box-shadow: 0px 3px 6px rgba(0,0,0,0.2);
    transition: 0.3s;
}
div[data-testid="stFileUploader"] section div div button:hover {
    background-color: #2b48c0 !important;
    transform: scale(1.03);
}

/* botones generales */
button[data-testid="baseButton-primary"], button[kind="primary"] {
    background-color: #3d5ee8 !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: bold !important;
    padding: 0.6em 1.4em !important;
    box-shadow: 0px 3px 6px rgba(0,0,0,0.2);
    transition: 0.3s;
}
button[data-testid="baseButton-primary"]:hover, button[kind="primary"]:hover {
    background-color: #2b48c0 !important;
    transform: scale(1.03);
}

/* centrado general */
h1, h2, h3, p {
    text-align: center;
}
img {
    display: block;
    margin-left: auto;
    margin-right: auto;
    width: 120px;
    margin-bottom: 1em;
}

/* footer */
footer {
    text-align: center;
    font-size: 0.8rem;
    color: #ffffff;
    margin-top: 2rem;
    opacity: 0.8;
}
            
/* fuerza el estilo del título de Streamlit */
[data-testid="stMarkdownContainer"] h1,
[data-testid="stMarkdownContainer"] p strong,
[data-testid="stMarkdownContainer"] p span,
h1, h1 span {
    color: #7A1531 !important;       /* vino */
    text-align: center !important;
    font-family: 'Gilroy', sans-serif !important;
    font-weight: 1200 !important;     /* aún más bold */
    font-size: 2.8rem !important;    /* más grande */
    letter-spacing: 1px !important;
    text-transform: uppercase !important;
    line-height: 1.2 !important;
}

</style>
""", unsafe_allow_html=True)


st.image(
    "https://raw.githubusercontent.com/majoocharteKellanova/oc-to-transit/main/assets/logo_rojo_kelloggs.png",
    width=180
)

# título de la app
st.markdown("<h1> consolidador de ordenes kellanover</h1>", unsafe_allow_html=True)

st.write("---")

# descripción breve
st.write("sube aquí los archivos de OC .xlsx con el mismo formato y obtén un solo archivo consolidado :)")

# subir archivos
archivos = st.file_uploader("elige tus archivos de excel", type=["xlsx"], accept_multiple_files=True)

# verificar si se subieron archivos
if archivos: # una lista vacía se considera False y una con elementos es True, entonces se puede hacer únicamente un if Lista
    lista_dfs = []

    # leer cada archivo con pandas y pasarlo a dataframe, luego lo adjuntas en la lista_dfs
    for archivo in archivos:
        df_temp = pd.read_excel(archivo, skiprows=1)
        lista_dfs.append(df_temp)

    # concatenar todos los dataframes
    df_total = pd.concat(lista_dfs, ignore_index=True) # junta todas las columnas que se llaman igual y devuelve un solo df

    # detectar columnas de tienda
    cols_tienda = [c for c in df_total.columns if c.startswith("Tienda")] # forma de list comprehension

    # aplicar melt
    df_largo = pd.melt(
        df_total,
        id_vars=["No. Orden", "Código de Barras", "SKU", "Descripción", "U. por CasePack"],
        value_vars=cols_tienda,
        var_name="No. Tienda",
        value_name="Total"
    )
    # más cambios
    df = df_largo
    df['No. Tienda'] = df['No. Tienda'].str.replace('Tienda', '')
    df['ID'] = df['No. Tienda'] + df['Código de Barras'].astype(str)
    df.insert(0, 'ID', df.pop('ID'))

    # mostrar preview del dataframe
    st.markdown("<h3 style='color:#F7C844;'>vista previa del consolidado:</h3>", unsafe_allow_html=True)
    st.dataframe(df_largo.head())

    # convertir a excel para descargar
    from io import BytesIO
    output = BytesIO()
    df_largo.to_excel(output, index=False)
    output.seek(0)

    # botón de descarga
    st.download_button(
        label=" descargar ⬇️",
        data=output,
        file_name="OC_consolidado.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

else:
    st.info("sube al menos un archivo .xlsx para comenzar")

# footer visible
st.markdown(
    "<footer> hecho por majo ocharte :)</footer>",
    unsafe_allow_html=True
)


