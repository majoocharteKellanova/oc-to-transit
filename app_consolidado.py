# importar librerías necesarias
import streamlit as st
import pandas as pd
import io
from datetime import datetime

st.set_page_config(layout="wide")

# formatito
# region
st.markdown("""
<style>
@font-face {
    font-family: 'Gilroy';
    src: url('https://raw.githubusercontent.com/majoocharteKellanova/oc-to-transit/main/assets/gilroy-medium.ttf');
}
            
/* fuente global */
*, div, span, section, button, label, input, textarea, h1, h2, h3, p {
    font-family: 'Gilroy', sans-serif !important;
}

/* fondo degradado vino -> rojo */
html, body, [data-testid="stAppViewContainer"] {
    background: linear-gradient(180deg, #7A1531 0%, #E2003E 100%);
    color-scheme: light;
}

/* contenedor principal que se vuelve la tarjeta blanca */
.block-container {
    background-color: #ffffff !important;
    border-radius: 20px;
    padding: 3rem 4rem !important; /* espacio interno */
    margin-top: 5vh !important;    /* separación del techo */
    margin-bottom: 5vh !important;
    box-shadow: 0px 8px 24px rgba(0,0,0,0.25);
    max-width: 900px !important;   /* controla el ancho de tu tarjeta */
}

/* estilo del Tab seleccionado */
button[aria-selected="true"] {
    color: #7A1531 !important;
    border-bottom: 2px solid #7A1531 !important;
}

/* quitar el padding extra que Streamlit pone arriba por defecto */
.block-container {
    padding-top: 2rem !important;
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
    color: #7A1531 !important; 
    text-align: center; 
    font-family: Gilroy, sans-serif; 
    font-weight: 10000 !important;
    font-size: 3rem; 
    line-height: 1.2;
    margin-bottom: 20px;'>
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
    background-color: #3d5ee8 !important;
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
    background-color: #3d5ee8 !important;
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
    color: #000000;
    margin-top: 2rem;
    opacity: 0.8;
}

/* tamaño de los nombres de las tabs */
button[data-baseweb="tab"] p {
    font-size: 1.5rem !important; /* ajusta este número a tu gusto */
    font-weight: 700 !important;
    color: #000000 !important;
}
    
/* texto normal */
div[data-testid="stMarkdownContainer"] p {
    color: black !important;
}

/* texto dentro de st.write() */
div[data-testid="stMarkdownContainer"] {
    color: #9b9b9b !important;
}
            
</style>
""", unsafe_allow_html=True)
# endregion

# backend xd
hoy = datetime.today()
meses = {
    1: "Enero", 2: "Febrero", 3: "Marzo", 4: "Abril",
    5: "Mayo", 6: "Junio", 7: "Julio", 8: "Agosto",
    9: "Septiembre", 10: "Octubre", 11: "Noviembre", 12: "Diciembre"
}
fecha_bonita = f"{hoy.day} de {meses[hoy.month]}"


st.image(
    "https://raw.githubusercontent.com/majoocharteKellanova/oc-to-transit/main/assets/mars_snacking-logo.png",
    width=160
)

# título de la app
st.markdown(
    """
    <h1 style='text-align: center; font-size: 2.9rem; font-weight: 10000;'>
    CONSOLIDADOR DE <br> ORDENES DE COMPRA
    </h1>
    """,
    unsafe_allow_html=True
)
tab1, tab2, tab3 = st.tabs(["HEB", "City Club", "Soriana"])

# tab 1 - heb
with tab1:

    st.image(
    "https://raw.githubusercontent.com/majoocharteKellanova/oc-to-transit/main/assets/heb.jpg",
    width=180
)

    # subir archivos
    archivos_heb = st.file_uploader("elige tus archivos", type=["xlsx"], accept_multiple_files=True)

    # region para procesar los archivos y mostrar el resultado
    # verificar si se subieron archivos
    if archivos_heb: # una lista vacía se considera False y una con elementos es True, entonces se puede hacer únicamente un if Lista
        lista_dfs = []

        # leer cada archivo con pandas y pasarlo a dataframe, luego lo adjuntas en la lista_dfs
        for archivo in archivos_heb:
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
        df["Código de Barras"] = df["Código de Barras"].astype(int)
        df["No. Tienda"] = df["No. Tienda"].astype(int)
        df['ID'] = (
            df['No. Tienda'].astype(str) + 
            df['Código de Barras'].astype(str)
        )
        df.insert(0, 'ID', df.pop('ID'))
        df['No. Tienda'] = df['No. Tienda'].astype(int)
        df['Código de Barras'] = df['Código de Barras'].astype(int)

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
            file_name=f"Tránsito {fecha_bonita}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    # endregion
    else:
        st.info("sube al menos un archivo .xlsx para comenzar")


# tab 2 - city club
with tab2:
    st.image(
    "https://raw.githubusercontent.com/majoocharteKellanova/oc-to-transit/main/assets/city.png",
    width=140
    )

    # subir archivos
    archivos_city = st.file_uploader("elige tus archivos", type=["xls"], accept_multiple_files=True, key="city")

    # region para procesar los archivos y mostrar el resultado
    if archivos_city:
        with st.spinner("consolidando archivos..."):
            lista_dfs2 = []

            for archivo in archivos_city:
                # leer archivo sin asumir encabezados
                df_raw = pd.read_excel(archivo, header=None, engine="xlrd")

                # extraer encabezado general que da la info de la OC
                proveedor = df_raw.iloc[1, 0]
                pedido = df_raw.iloc[1, 1]
                fecha_pedido = df_raw.iloc[1, 2]
                fecha_inicio = df_raw.iloc[1,3]
                fecha_fin = df_raw.iloc[1,4]
                plazo = df_raw.iloc[1,5]

                # encontrar dónde empieza el detalle
                fila_header = df_raw[
                    df_raw.iloc[:, 0] == "Num. Prov."
                ].index[0]

                # leer solo la sección detalle
                df_detalle = pd.read_excel(
                    archivo,
                    skiprows=fila_header
                )

                # eliminar filas sin código
                df_detalle = df_detalle.dropna(subset=["Codigo"])

                # agregar columnas del encabezado
                df_detalle["Número de Proveedor"] = proveedor
                df_detalle["Número de Pedido"] = pedido
                df_detalle["Fecha de Pedido"] = fecha_pedido
                df_detalle["Fecha de Inicio Emb"] = fecha_inicio
                df_detalle["Fecha de Fin Emb"] = fecha_fin
                df_detalle["Plazo de pago"] = plazo

                lista_dfs2.append(df_detalle)
            df_total2 = pd.concat(lista_dfs2, ignore_index=True)
        
        # crear ID
        df_total2["Num. Tienda"] = df_total2["Num. Tienda"].astype(int)
        df_total2["Codigo"] = df_total2["Codigo"].astype(int)

        df_total2["ID"] = (df_total2["Num. Tienda"].astype(str) +df_total2["Codigo"].astype(str))
        # mover ID al inicio
        df_total2.insert(0, "ID", df_total2.pop("ID"))

        df_total2 = df_total2.drop(columns=["Num. Prov.", "Num. Pedido"])
        df_total2 = df_total2.rename(columns={"Num. Tienda": "No. Tienda", "Codigo": "Código de Barras", "Cant. Pedida": "Total", "Desc.Art.": "Descripción", "Precio Costo": "Costo"})

        cols_fechas = [
            "Fecha de Pedido",
            "Fecha de Inicio Emb",
            "Fecha de Fin Emb"
        ]

        for col in cols_fechas:
            df_total2[col] = pd.to_datetime(
                df_total2[col].astype(str),
                format="%Y%m%d"
            ).dt.date

        st.markdown("<h3 style='color:#F7C844;'>vista previa del consolidado:</h3>", unsafe_allow_html=True)
        st.dataframe(df_total2.head())
 
        from io import BytesIO
        output2 = BytesIO()
        df_total2.to_excel(output2, index=False)
        output2.seek(0)

        st.download_button(
            label=" descargar ⬇️",
            data=output2,
            file_name=f"Tránsito City Club {fecha_bonita}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    else:
        st.info("sube al menos un archivo .xlsx para comenzar")

# tab 3 - soriana
with tab3:
    st.image(
    "https://raw.githubusercontent.com/majoocharteKellanova/oc-to-transit/main/assets/soriana.svg",
    width=190
    )

    # subir archivos
    archivos_soriana = st.file_uploader("elige tus archivos", type=["xls"], accept_multiple_files=True, key="soriana")
    if archivos_soriana:
        with st.spinner("consolidando archivos..."):
                lista_dfs3 = []

                for archivo in archivos_soriana:
                    # leer archivo sin asumir encabezados
                    df_raw2 = pd.read_excel(archivo, header=None, engine="xlrd")

                    # extraer encabezado general que da la info de la OC
                    proveedor2 = df_raw2.iloc[1, 0]
                    pedido2 = df_raw2.iloc[1, 1]
                    fecha_pedido2 = df_raw2.iloc[1, 2]
                    fecha_inicio2 = df_raw2.iloc[1,3]
                    fecha_fin2 = df_raw2.iloc[1,4]
                    plazo2 = df_raw2.iloc[1,5]

                    # encontrar dónde empieza el detalle
                    fila_header2 = df_raw2[
                        df_raw2.iloc[:, 0] == "Num. Prov."
                    ].index[0]

                    # leer solo la sección detalle
                    df_detalle2 = pd.read_excel(
                        archivo,
                        skiprows=fila_header2
                    )

                    # eliminar filas sin código
                    df_detalle2 = df_detalle2.dropna(subset=["Codigo"])

                    # agregar columnas del encabezado
                    df_detalle2["Número de Proveedor"] = proveedor2
                    df_detalle2["Número de Pedido"] = pedido2
                    df_detalle2["Fecha de Pedido"] = fecha_pedido2
                    df_detalle2["Fecha de Inicio Emb"] = fecha_inicio2
                    df_detalle2["Fecha de Fin Emb"] = fecha_fin2
                    df_detalle2["Plazo de pago"] = plazo2

                    lista_dfs3.append(df_detalle2)
                df_total3 = pd.concat(lista_dfs3, ignore_index=True)
            
                # crear ID
                df_total3["Num. Tienda"] = df_total3["Num. Tienda"].astype(int)
                df_total3["Codigo"] = df_total3["Codigo"].astype(int)

                df_total3["ID"] = (df_total3["Num. Tienda"].astype(str) +df_total3["Codigo"].astype(str))
                # mover ID al inicio
                df_total3.insert(0, "ID", df_total3.pop("ID"))

                df_total3 = df_total3.drop(columns=["Num. Prov.", "Num. Pedido"])
                df_total3 = df_total3.rename(columns={"Num. Tienda": "No. Tienda", "Codigo": "Código de Barras", "Cant. Pedida": "Total", "Desc.Art.": "Descripción", "Precio Costo": "Costo"})

                cols_fechas = [
                    "Fecha de Pedido",
                    "Fecha de Inicio Emb",
                    "Fecha de Fin Emb"
                ]
                
                for col in cols_fechas:
                    df_total3[col] = pd.to_datetime(
                        df_total3[col].astype(str),
                        format="%Y%m%d"
                    ).dt.date

                st.markdown("<h3 style='color:#F7C844;'>vista previa del consolidado:</h3>", unsafe_allow_html=True)
                st.dataframe(df_total3.head())
        
                from io import BytesIO
                output3 = BytesIO()
                df_total3.to_excel(output3, index=False)
                output3.seek(0)

                st.download_button(
                    label=" descargar ⬇️",
                    data=output3,
                    file_name=f"Tránsito Soriana {fecha_bonita}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
    else:
        st.info("sube al menos un archivo .xlsx para comenzar")

# descripción breve
st.write("sube aquí los archivos de OC .xlsx con el mismo formato y obtén un solo archivo consolidado")


# footer visible
st.markdown(
    "<footer> :) </footer>",
    unsafe_allow_html=True
)
