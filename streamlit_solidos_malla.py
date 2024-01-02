import streamlit as st
import pandas as pd

# Función para crear nuevas categorías y calcular proporciones
def categorizar_y_calcular(df, start_date, end_date):
    # Filtrar por rango de fechas
    mask = (df['fecha'] >= pd.to_datetime(start_date)) & (df['fecha'] <= pd.to_datetime(end_date))
    df_filtrado = df.loc[mask]

    # Crear nuevas columnas basadas en las condiciones
    df_filtrado['solidos_a0_cat'] = df_filtrado['solidos_a0'].apply(lambda x: 1 if x < 41 else 0)
    df_filtrado['malla_a0_cat'] = df_filtrado['malla_a0'].apply(lambda x: 1 if x < 31 else 0)

    # Calcular la proporción para cada categoría
    prop_solidos = df_filtrado['solidos_a0_cat'].sum() / len(df_filtrado)
    prop_malla = df_filtrado['malla_a0_cat'].sum() / len(df_filtrado)

    return prop_solidos, prop_malla

# Título de la aplicación
st.title('Categorización y Cálculo de Proporciones')

# Subtítulo con estilo
st.markdown("""
    <style>
    .subtitulo {
        font-size:20px !important;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<p class="subtitulo">Seleccione el rango de fechas y cargue su archivo CSV:</p>', unsafe_allow_html=True)

# Carga de archivo
uploaded_file = st.file_uploader("Elige un archivo CSV", type="csv")
if uploaded_file is not None:
    # Lectura de datos
    data = pd.read_csv(uploaded_file)

    # Asegurarse de que la columna de fecha es de tipo datetime
    data['fecha'] = pd.to_datetime(data['fecha'])

    # Selector de rango de fecha
    min_date = data['fecha'].min()
    max_date = data['fecha'].max()
    start_date = st.date_input('Fecha de inicio', min_date)
    end_date = st.date_input('Fecha de fin', max_date)

    if start_date <= end_date:
        # Categorización y cálculo de proporciones
        prop_solidos, prop_malla = categorizar_y_calcular(data, start_date, end_date)
        
        # Mostrar resultados con estilo
        st.markdown(f'<h2>Proporción de solidos menor a 41:     {prop_solidos*100:.2f} % </h2>', unsafe_allow_html=True)
        st.markdown(f'<h2>Proporción de malla menor a 31:       {prop_malla*100:.2f} % </h2>', unsafe_allow_html=True)
    else:
        st.error('Error: La fecha de inicio debe ser anterior a la fecha de fin.')
