import streamlit as st
import pandas as pd
import geopandas as gpd
import numpy as np
import plotly.figure_factory as ff
import plotly.express as px
from datetime import datetime as dt
import folium
from statsmodels.tsa.holtwinters import SimpleExpSmoothing
import warnings
warnings.filterwarnings("ignore")

DATA_URL = 'https://raw.githubusercontent.com/kiramishima/pp_lgbtq/master/Datasets/reportes_visible_2023-10-oct.csv'
LGBTQ_COLORS = ["#c095cb", "#6a95d5", "#74ac6f", "#f7d168", "#f6934c", "#e15971"]
LGBTQ_COLORS2 = LGBTQ_COLORS + ["#71d1fb", "#5766ce", "#c6237c", "#ed595e"]

st.set_page_config(
    page_title="LCDN 504 - LGBTQ+ Dashboard",
    page_icon="📊",
    layout="wide",
)

@st.cache_data
def load_data():
    df = pd.read_csv(DATA_URL, encoding='latin1')
    return df

st.title('Violencia hacia la comunidad LGBTQ+ (2018-2023)')

df = load_data()
# Parser dia incidente to DateTime type
df.dia_incidente = pd.to_datetime(df.dia_incidente)
df_select = df[df.dia_incidente.dt.year >= 2018]

# Setting GeoDataFrame
gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.longitud, df.latitud), crs ="EPSG:4326")


st.header('Sample Dataframe LGBTQ+')
st.write(df_select.sample(20))

st.divider()
st.header('Serie de tiempo de casos de violencia hacía la comunidad LGBTQ+')
df_yearly = df_select.groupby(df_select.dia_incidente.dt.year, as_index=False).size()
df_bymonth = df_select.groupby(pd.Grouper(key='dia_incidente', freq='M'), as_index=False).size()

years = df_select.dia_incidente.dt.year.unique().tolist()
years.insert(0, 'Todo')

tab1, tab2 = st.tabs(["Por año", "Por mes"])
with tab1:
    
    fig = px.line(df_yearly,
                x='dia_incidente',
                y='size',
                labels={'dia_incidente': 'Año', 'size': 'Total'},
                title='Violencia LGBTQ+ del 2018 al 2023 de manera anualizada',
                width=1080,
                height=720,
                markers=True)

    fig.update_layout(showlegend=True)
    fig.update_traces(line={'width': 5})

    fig.update_layout({
        'plot_bgcolor': 'rgba(0, 0, 0, 0)',
        'paper_bgcolor': 'rgba(0, 0, 0, 0)',
    })
    st.plotly_chart(fig, theme="streamlit")
with tab2:

    option = st.selectbox(
        "Visualizar por año",
        years,
        index=0,
        placeholder="2023",
    )

    option2 = st.selectbox(
        "Aplicar método de suavizamiento a la serie",
        ('No aplicar', 'Promedio móvil', 'Promedios móviles ponderados', 'Suavizamiento exponencial', 'Todos los métodos'),
        index=0,
        placeholder="",
    )

    temp_df_bymonth = df_bymonth.copy()
    if option != 'Todo':
        temp_df_bymonth = df_select[df_select.dia_incidente.dt.year == option].groupby(pd.Grouper(key='dia_incidente', freq='M'), as_index=False).size()

    match option2:
        case 'Promedio móvil':
            data = temp_df_bymonth['size'].tolist()
            #print(data)
            data2 = []
            for idx, item in enumerate(data):
                if idx - 3 >= 0:
                    # print(idx, item)
                    v1 = data[idx-3]
                    v2 = data[idx-2]
                    v3 = data[idx-1]
                    # mes, _ = item
                    prom = (v1 + v2 + v3) / 3
                    # print(prom)
                    data2.append(round(prom, 2))
                else:
                    data2.append(item)
            temp_df_bymonth['PM'] = data2
        case 'Promedios móviles ponderados':
            data = temp_df_bymonth['size'].tolist()
            #print(data)
            data2 = []
            for idx, item in enumerate(data):
                if idx != len(data) and idx >= 3:
                    v0 = data[idx-3]
                    v1 = data[idx-2]
                    v2 = data[idx-1]
                    prom = v0/6 + 2*v1/6 + 3*v2/6
                    # print(prom)
                    data2.append(round(prom, 2))
                else:
                    data2.append(item)
            temp_df_bymonth['PMP'] = data2
        case 'Suavizamiento exponencial':
            data = temp_df_bymonth['size'].tolist()
            d = [0 if i is None else i for i in data]
            model = SimpleExpSmoothing(d[:len(d)]).fit(smoothing_level=0.6)
            res = model.fittedvalues
            temp_df_bymonth['SuaExp'] = res
        case 'Todos los métodos':
            data = temp_df_bymonth['size'].tolist()
            # PM
            data2 = []
            for idx, item in enumerate(data):
                if idx - 3 >= 0:
                    # print(idx, item)
                    v1 = data[idx-3]
                    v2 = data[idx-2]
                    v3 = data[idx-1]
                    # mes, _ = item
                    prom = (v1 + v2 + v3) / 3
                    # print(prom)
                    data2.append(round(prom, 2))
                else:
                    data2.append(item)
            # PMP
            data3 = []
            for idx, item in enumerate(data):
                if idx != len(data) and idx >= 3:
                    v0 = data[idx-3]
                    v1 = data[idx-2]
                    v2 = data[idx-1]
                    prom = v0/6 + 2*v1/6 + 3*v2/6
                    # print(prom)
                    data3.append(round(prom, 2))
                else:
                    data3.append(item)
            # SuaExp
            d = [0 if i is None else i for i in data]
            model = SimpleExpSmoothing(d[:len(d)]).fit(smoothing_level=0.6)
            res = model.fittedvalues
            # Agregando la data
            temp_df_bymonth['SuaExp'] = res
            temp_df_bymonth['PMP'] = data3
            temp_df_bymonth['PM'] = data2

    fig2 = px.line(temp_df_bymonth,
        x='dia_incidente',
        y='size',
        labels={'dia_incidente': 'Fecha', 'size': 'Total'},
        title='Violencia hacia la comunidad LGBTQ+ del 2018 al presente año',
        width=1080,
        height=720)
    if option2 == 'Promedio móvil':
        fig2 = px.line(temp_df_bymonth,
            x='dia_incidente',
            y=['size', 'PM'],
            labels={'dia_incidente': 'Fecha', 'size': 'Total'},
            title='Violencia hacia la comunidad LGBTQ+ del 2018 al presente año',
            width=1080,
            height=720)

    if option2 == 'Promedios móviles ponderados':
        fig2 = px.line(temp_df_bymonth,
            x='dia_incidente',
            y=['size', 'PMP'],
            labels={'dia_incidente': 'Fecha', 'size': 'Total'},
            title='Violencia hacia la comunidad LGBTQ+ del 2018 al presente año',
            width=1080,
            height=720)

    if option2 == 'Suavizamiento exponencial':
        fig2 = px.line(temp_df_bymonth,
            x='dia_incidente',
            y=['size', 'SuaExp'],
            labels={'dia_incidente': 'Fecha', 'size': 'Total'},
            title='Violencia hacia la comunidad LGBTQ+ del 2018 al presente año',
            width=1080,
            height=720)
        
    if option2 == 'Todos los métodos':
        fig2 = px.line(temp_df_bymonth,
            x='dia_incidente',
            y=['size', 'PM', 'PMP', 'SuaExp'],
            labels={'dia_incidente': 'Fecha', 'size': 'Total'},
            title='Violencia hacia la comunidad LGBTQ+ del 2018 al presente año',
            width=1080,
            height=720)

    fig2.update_layout({
        'plot_bgcolor': 'rgba(0, 0, 0, 0)',
        'paper_bgcolor': 'rgba(0, 0, 0, 0)',
    })
    fig2.update_xaxes(
        dtick="M1",
        ticklabelmode="period")
    st.plotly_chart(fig2, theme="streamlit")

st.divider()
st.header('Tipo de agresores hacía la comunidad LGBTQ+')
dfTAgresores = df[df.tipo_de_agresora.notnull()].groupby('tipo_de_agresora', as_index=False).size()
dfTAgresores = dfTAgresores.sort_values('size', ascending=False)
dfTAgresores.reset_index(inplace=True, drop='index')

tab3, tab4 = st.tabs(["Mayor presencia", "Menor presencia"])
with tab3:
    fig3 = px.pie(dfTAgresores.head(5),
        values='size',
        names='tipo_de_agresora',
        title='Tipo de agresores con mayor presencia registrados',
        color_discrete_sequence=LGBTQ_COLORS,
        width=1080,
        height=720)

    fig3.update_layout(showlegend=True)

    fig3.update_layout({
        'plot_bgcolor': 'rgba(0, 0, 0, 0)',
        'paper_bgcolor': 'rgba(0, 0, 0, 0)',
    })

    st.plotly_chart(fig3, theme=None)
with tab4:
    fig4 = px.pie(dfTAgresores.tail(5),
            values='size',
            names='tipo_de_agresora',
            title='Tipo de agresores con menor presencia registrados',
            color_discrete_sequence=LGBTQ_COLORS,
            width=1080,
            height=720)

    fig.update_layout(showlegend=True)

    fig.update_layout({
        'plot_bgcolor': 'rgba(0, 0, 0, 0)',
        'paper_bgcolor': 'rgba(0, 0, 0, 0)',
    })

    st.plotly_chart(fig4, theme=None)

st.divider()
st.header('Tipo de agresión cometida hacía la comunidad LGBTQ+')

dfTAgresion = df[df.tipo_de_agresion.notnull()].groupby('tipo_de_agresion', as_index=False).size()
dfTAgresion = dfTAgresion.sort_values('size', ascending=False)
dfTAgresion.reset_index(inplace=True, drop='index')

tab5, tab6 = st.tabs(["Top 5", "Otros"])
with tab5:
    fig5 = px.pie(dfTAgresion.head(5),
        names='tipo_de_agresion',
        values='size',
        title='Tipo de agresiones con mayor presencia registradas',
        color_discrete_sequence=LGBTQ_COLORS,
        width=1080,
        height=720)

    fig5.update_layout(showlegend=True)

    fig5.update_layout({
        'plot_bgcolor': 'rgba(0, 0, 0, 0)',
        'paper_bgcolor': 'rgba(0, 0, 0, 0)',
    })
    st.plotly_chart(fig5, theme=None)
with tab6:
    fig6 = px.pie(dfTAgresion[dfTAgresion['size'] < 41].head(5),
        names='tipo_de_agresion',
        values='size',
        title='Tipo de agresiones con menor presencia registradas',
        color_discrete_sequence=LGBTQ_COLORS,
        width=1080,
        height=720)

    fig6.update_layout(showlegend=True)

    fig6.update_layout({
        'plot_bgcolor': 'rgba(0, 0, 0, 0)',
        'paper_bgcolor': 'rgba(0, 0, 0, 0)',
    })
    st.plotly_chart(fig6, theme=None)

# Relacion Agresor x Tipo de agresión
st.divider()
st.subheader('Relación entre tipo de agresor y tipo de agresión cometida.')
dfAgresorAgresiones = df[(df.tipo_de_agresora.notnull()) & (df.tipo_de_agresion.notnull())].groupby(['tipo_de_agresora', 'tipo_de_agresion'], as_index=False).size()
dfAgresorAgresiones = dfAgresorAgresiones.sort_values('size', ascending=False)
dfAgresorAgresiones.reset_index(inplace=True, drop='index')
dfAgresorAgresiones['porcentaje'] = round(dfAgresorAgresiones['size']/dfAgresorAgresiones['size'].sum(), 2) * 100

fig7 = px.sunburst(
    dfAgresorAgresiones.head(10),
    title='Tipo de agresión por tipo de agresor',
    path=['tipo_de_agresora', 'tipo_de_agresion'],
    names='tipo_de_agresora',
    values='size',
    color_discrete_sequence=LGBTQ_COLORS,
    labels={'size': 'Identidad genero'},
    width=1080,
    height=720)

fig7.update_layout({
    'plot_bgcolor': 'rgba(0, 0, 0, 0)',
    'paper_bgcolor': 'rgba(0, 0, 0, 0)',
})
st.plotly_chart(fig7, theme=None)

# Lugar donde se comete la agresion
st.divider()
st.subheader('Lugar donde se comete la agresión.')
dfLugarSubLugar = df[(df.tipo_de_lugar.notnull()) & (df.subtipo_de_lugar.notnull())].groupby(['tipo_de_lugar', 'subtipo_de_lugar'], as_index=False).size()
dfLugarSubLugar = dfLugarSubLugar.sort_values('size', ascending=False)
dfLugarSubLugar.reset_index(inplace=True, drop='index')
dfLugarSubLugar['porcentaje'] = round(dfLugarSubLugar['size']/dfLugarSubLugar['size'].sum(), 2) * 100

fig8 = px.bar(
    dfLugarSubLugar.head(10),
    title='Lugar donde se comete la agresión.',
    x='tipo_de_lugar',
    y='size',
    color='subtipo_de_lugar',
    labels={'size': 'Total', 'tipo_de_lugar': 'Entorno', 'subtipo_de_lugar': 'Lugar'},
    text='size',
    width=1080,
    height=720)

fig8.update_layout({
    'plot_bgcolor': 'rgba(0, 0, 0, 0)',
    'paper_bgcolor': 'rgba(0, 0, 0, 0)',
})
fig8.update_layout(barmode='stack')
st.plotly_chart(fig8, theme=None)

# Nivel de estudios
st.divider()
st.header('Nivel de estudios de las personas de la comunidad LGBTQ+.')
data_escolaridad = df.groupby('escolaridad', as_index=False).size().sort_values('size', ascending=True)

fig9 = px.bar(data_escolaridad,
    x='escolaridad',
    y='size',
    labels={'escolaridad': 'Nivel de estudios', 'size': 'Total'},
    color='escolaridad',
    title='Nivel de escolaridad de las victimas',
    width=1080,
    height=720,
    color_discrete_sequence=LGBTQ_COLORS)

fig9.update_layout(showlegend=True)

fig9.update_layout({
    'plot_bgcolor': 'rgba(0, 0, 0, 0)',
    'paper_bgcolor': 'rgba(0, 0, 0, 0)',
})
st.plotly_chart(fig9, theme=None)

st.divider()
st.header('Estados con más número de agresiones')

dfEntidades = df[df.entidad.notnull()].groupby('entidad', as_index=False).size()
dfEntidades = dfEntidades.sort_values('size', ascending=True)
dfEntidades.reset_index(inplace=True, drop='index')

fig10 = px.bar(dfEntidades.head(10),
    y='size',
    x='entidad',
    title='Estados con mayor número de agresiones',
    color='entidad',
    text='size',
    labels={'entidad': 'Estado'},
    width=1080,
    height=720)

fig10.update_layout(showlegend=True)

fig10.update_layout({
    'plot_bgcolor': 'rgba(0, 0, 0, 0)',
    'paper_bgcolor': 'rgba(0, 0, 0, 0)',
})
st.plotly_chart(fig10, theme=None)


st.divider()
st.header('Mapa agresión en CDMX')

cdmx_map = [19.432608, -99.133209]
cdmx = gdf[gdf.entidad == 'Ciudad de México']

m = folium.Map(location=cdmx_map, zoom_start=10, tiles="CartoDB positron")

px.set_mapbox_access_token(st.secrets['MAPBOX_KEY'])

fig11 = px.scatter_mapbox(cdmx,
    lat=cdmx.geometry.y,
    lon=cdmx.geometry.x,
    color="tipo_de_agresion",
    color_continuous_scale=px.colors.cyclical.IceFire,
    labels={'tipo_de_agresion': 'Tipo de agresión'},
    zoom=10,
    width=1080,
    height=720)

st.plotly_chart(fig11, theme=None)
