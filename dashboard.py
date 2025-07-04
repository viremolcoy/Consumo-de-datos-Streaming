import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
st.set_page_config(page_title="Dashboard Streaming DUOC", layout="wide")

st.title("📊 Dashboard Interactivo de Ventas (Streaming DUOC)")
st.markdown("Los datos se actualizan automáticamente desde el webhook en tiempo real.")

@st.cache_data(ttl=5)
def cargar_datos():
    try:
        df = pd.read_csv("datos_limpiados.csv")
        df['fecreg'] = pd.to_datetime(df['fecreg'])
        df['precio'] = pd.to_numeric(df['precio'], errors='coerce')
        df['cantidad'] = pd.to_numeric(df['cantidad'], errors='coerce')
        df['monto'] = pd.to_numeric(df['monto'], errors='coerce')
        return df
    except:
        return pd.DataFrame()

df = cargar_datos()

if df.empty:
    st.warning("Esperando datos desde el webhook...")
    st.stop()

# =================== PESTAÑAS ===================
tab1, tab2, tab4, tab5, tab6 = st.tabs([
    "📊 Dashboard General",
    "📈 Historial de Precios",
    "👥 Patrones por Cliente",
    "💳 Comparativa de Pagos",
    "🕯️ Simulación Candlestick"
])

# ========== TAB 1 ==========
with tab1:
    st.subheader("Filtros")
    col1, col2, col3 = st.columns(3)
    with col1:
        cliente = st.selectbox("Filtrar por Cliente", ["Todos"] + sorted(df['cliente'].unique()))
    with col2:
        producto = st.selectbox("Filtrar por Producto", ["Todos"] + sorted(df['producto'].unique()))
    with col3:
        forma_pago = st.selectbox("Filtrar por Forma de Pago", ["Todos"] + sorted(df['forma_pago'].unique()))

    df_filtrado = df.copy()
    if cliente != "Todos":
        df_filtrado = df_filtrado[df_filtrado["cliente"] == cliente]
    if producto != "Todos":
        df_filtrado = df_filtrado[df_filtrado["producto"] == producto]
    if forma_pago != "Todos":
        df_filtrado = df_filtrado[df_filtrado["forma_pago"] == forma_pago]

    col1, col2, col3 = st.columns(3)
    col1.metric("🧾 Total Transacciones", f"{len(df_filtrado)}")
    col2.metric("💰 Total Vendido", f"${df_filtrado['monto'].sum():,.0f}")
    col3.metric("📦 Productos Vendidos", f"{df_filtrado['cantidad'].sum():,.0f}")

    st.subheader("📦 Ventas por Producto")
    st.bar_chart(df_filtrado.groupby("producto")["monto"].sum())

    st.subheader("📆 Ventas en el Tiempo")
    st.line_chart(df_filtrado.groupby(df_filtrado["fecreg"].dt.strftime('%Y-%m-%d %H:%M'))["monto"].sum())

    st.subheader("💳 Distribución por Forma de Pago")

    formas_pago = df_filtrado["forma_pago"].value_counts().reset_index()
    formas_pago.columns = ["Forma de Pago", "Cantidad"]

    fig_pago = px.pie(
        formas_pago,
        values='Cantidad',
        names='Forma de Pago',
        title='Distribución de formas de pago',
        color_discrete_sequence=px.colors.sequential.RdBu
    )
    fig_pago.update_traces(textposition='inside', textinfo='percent+label')
    fig_pago.update_layout(
        showlegend=False,
        margin=dict(t=40, b=0, l=0, r=0),
        height=350
    )

    st.plotly_chart(fig_pago, use_container_width=True)

# ========== TAB 2 ==========
with tab2:
    st.subheader("🔎 Productos con Mayor y Menor Precio Promedio")

    precio_prom = df.groupby('producto')['precio'].mean().sort_values(ascending=False)

    st.write("🧠 Top 5 productos con **precio promedio más alto**:")
    st.bar_chart(precio_prom.head(5))

    st.write("🔍 Top 5 productos con **precio promedio más bajo**:")
    st.bar_chart(precio_prom.tail(5))

# ========== TAB 4 ==========
with tab4:
    st.subheader("👥 Ranking de Clientes por Monto Total")
    ranking = df.groupby("cliente")["monto"].sum().sort_values(ascending=False).head(10)
    st.bar_chart(ranking)

# ========== TAB 5 ==========
with tab5:
    st.subheader("💳 Monto Promedio por Forma de Pago")
    promedios = df.groupby("forma_pago")["monto"].mean().sort_values(ascending=False)
    st.bar_chart(promedios)

# ========== TAB 6 ==========
with tab6:
    st.subheader("📊 Relación entre Precio Unitario y Cantidad por Producto")

    producto_seleccionado = st.selectbox("Selecciona un producto", df['producto'].unique(), key="relacion_precio_cantidad")
    datos_producto = df[df['producto'] == producto_seleccionado]

    st.write(f"📈 Distribución de cantidad comprada vs precio para **{producto_seleccionado}**")
    st.scatter_chart(datos_producto[["cantidad", "precio"]])

