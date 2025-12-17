import streamlit as st
import pandas as pd
import pydeck as pdk

st.set_page_config(page_title="Cargatron", layout="wide", page_icon=":battery:")

@st.cache_data
def load_data():
    return pd.read_csv("data/red_recarga_acceso_publico_2021.csv", sep=";")

def page_home():
    st.title("Cargatron")
    st.image("img/puntos-recarga-madrid.jpg")
    with st.expander("See explanation", expanded=True):
        st.write("Pequeña descripción")

    st.write("Bienvenido. Usa el menú lateral para navegar.")
    st.info("En 'Datos' puedes ver el mapa y los gráficos.")

    uploaded_file = st.file_uploader("Sube un archivo .csv", type=["csv"])
    if uploaded_file is not None:
        st.success("Archivo subido. (Si quieres, luego lo usamos en la página Datos)")

def page_datos():
    st.title("Datos")

    # Carga SOLO aquí
    datos = load_data()

    st.subheader("Preview")
    with st.echo():
        st.dataframe(datos.head(20), use_container_width=True)

    st.header("Mapa de estaciones")
    map_datos = (
        datos[["latidtud", "longitud"]]
        .dropna()
        .rename(columns={"latidtud": "lat", "longitud": "lon"})
    )
    st.map(map_datos)

    st.header("Cargadores por distrito")
    # Ojo: si "Nº CARGADORES" viene como texto con comas, conviértelo a número antes
    datos["Nº CARGADORES"] = pd.to_numeric(datos["Nº CARGADORES"], errors="coerce")

    by_district = (
        datos.groupby("DISTRITO")["Nº CARGADORES"]
        .sum()
        .sort_values(ascending=False)
    )
    st.bar_chart(by_district)

    st.header("Cargadores por operador")
    by_operator = (
        datos.groupby("OPERADOR")["Nº CARGADORES"]
        .sum()
        .sort_values(ascending=False)
    )
    st.bar_chart(by_operator)

def page_filtros():
    st.title("Filtros")

    datos = load_data()
        # --- SIDEBAR filtros + checkboxes ---
    st.sidebar.header("Filtros")

    # 1) Distrito
    use_distrito = st.sidebar.checkbox("Filtrar por distrito", value=False)
    distritos = sorted(datos["DISTRITO"].dropna().unique().tolist())
    distrito_sel = st.sidebar.selectbox("Distrito", ["(todos)"] + distritos, index=0, disabled=not use_distrito)

    # 1) Operador
    use_operador = st.sidebar.checkbox("Filtrar por operador", value=False)
    operadores = sorted(datos["OPERADOR"].dropna().unique().tolist())
    operador_sel = st.sidebar.selectbox("Operador", ["(todos)"] + operadores, index=0, disabled=not use_operador)

    # 2) Min/Max cargadores
    use_cargadores = st.sidebar.checkbox("Filtrar por nº cargadores", value=False)

    # Rango del slider (si todo es NaN, fallback)
    min_c = int(datos["Nº CARGADORES"].min()) if datos["Nº CARGADORES"].notna().any() else 0
    max_c = int(datos["Nº CARGADORES"].max()) if datos["Nº CARGADORES"].notna().any() else 0

    # Para que el slider vaya por enteros
    rango_sel = st.sidebar.select_slider(
        "Rango nº cargadores (min, max)",
        options=list(range(min_c, max_c + 1)) if max_c >= min_c else [0],
        value=(min_c, max_c) if max_c >= min_c else (0, 0),
        disabled=not use_cargadores,
    )

    # --- aplicar filtros ---
    datos_f = datos

    if use_distrito and distrito_sel != "(todos)":
        datos_f = datos_f[datos_f["DISTRITO"] == distrito_sel]

    if use_operador and operador_sel != "(todos)":
        datos_f = datos_f[datos_f["OPERADOR"] == operador_sel]

    if use_cargadores:
        a, b = rango_sel
        datos_f = datos_f[datos_f["Nº CARGADORES"].between(a, b, inclusive="both")]

    # 5) Si vacío -> warning + stop
    if datos_f.empty:
        st.warning("Con estos filtros no hay estaciones. Prueba a relajarlos.")
        st.stop()

    # --- layout 3:2 ---
    col_map, col_stats = st.columns([3, 2], gap="large")

    # 6) Mapa estaciones
    with col_map:
        st.subheader("Mapa de estaciones")

        # 7) Zoom: si filtro de distrito -> zoom 13; si no -> 11
        zoom = 13 if (use_distrito and distrito_sel != "(todos)") else 11

        # Centro del mapa: media de coords del filtrado
        center_lat = float(datos_f["latidtud"].mean())
        center_lon = float(datos_f["longitud"].mean())

        layer = pdk.Layer(
            "ScatterplotLayer",
            data=datos_f.rename(columns={"latidtud": "lat", "longitud": "lon"}),
            get_position="[lon, lat]",
            get_color="[255, 75, 75]",
            get_radius=100,
            pickable=True,
        )

        view_state = pdk.ViewState(
            latitude=center_lat,
            longitude=center_lon,
            zoom=zoom,
        )

        tooltip = {
            "html": "<b>Distrito:</b> {DISTRITO}<br/>"
                    "<b>Operador:</b> {OPERADOR}<br/>"
                    "<b>Nº cargadores:</b> {Nº CARGADORES}",
            "style": {"fontSize": "12px"},
        }

        st.pydeck_chart(pdk.Deck(layers=[layer], initial_view_state=view_state, tooltip=tooltip), use_container_width=True)

        st.caption(f"Estaciones mostradas: {len(datos_f)}")

    with col_stats:
        st.subheader("Distribuciones")

        # 8) Si NO filtro distrito -> distribución por distritos
        if not use_distrito or distrito_sel == "(todos)":
            st.markdown("**Estaciones por distrito**")
            dist_distrito = datos_f["DISTRITO"].value_counts().sort_values(ascending=False)
            st.bar_chart(dist_distrito)

        # 9) Si NO filtro operador -> distribución por operador
        if not use_operador or operador_sel == "(todos)":
            st.markdown("**Estaciones por operador**")
            dist_operador = datos_f["OPERADOR"].value_counts().sort_values(ascending=False)
            st.bar_chart(dist_operador)

        # 10) Cargadores por tamaño (bins)
        st.markdown("**Cargadores por tamaño (estación)**")
        # Define bins razonables (ajusta si quieres)
        bins = [-1, 1, 2, 4, 8, 16, 10**9]
        labels = ["1", "2", "3-4", "5-8", "9-16", "17+"]
        size_cat = pd.cut(datos_f["Nº CARGADORES"].fillna(0), bins=bins, labels=labels)
        size_counts = size_cat.value_counts().sort_index()
        st.bar_chart(size_counts)


# ---------- Sidebar Menu ----------
st.sidebar.title("Menú")
page = st.sidebar.selectbox("Elige una página", ["Home", "Datos", "Filtros"], index=0)

# ---------- Router ----------
if page == "Home":
    page_home()
elif page == 'Datos':
    page_datos()
else:
    page_filtros()