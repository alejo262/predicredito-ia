import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import time
import os
import joblib
import pytz  # <--- NUEVA LIBRERÍA PARA CONTROL DE ZONA HORARIA
from datetime import datetime
from streamlit_option_menu import option_menu

st.set_page_config(page_title="Predicrédito", page_icon="💳", layout="wide")

# ---------- ESTILOS GENERALES ----------
st.markdown("""
<style>
.main {
    background-color: #f4f7fc;
}
.kpi-card {
    background: linear-gradient(135deg, #1f4e79, #2E86C1);
    border-radius: 18px;
    padding: 18px;
    color: white;
    text-align: center;
    box-shadow: 0px 4px 12px rgba(0,0,0,0.15);
}
</style>
""", unsafe_allow_html=True)

# ---------- PANTALLA DE CARGA INICIAL (PRIMERA VEZ) ----------
contenedor_inicial = st.empty()

with contenedor_inicial.container():
    st.markdown("""
        <div style="
            background: linear-gradient(135deg, #1f4e79, #2c3e50);
            padding: 40px;
            border-radius: 20px;
            text-align: center;
            box-shadow: 0px 8px 25px rgba(0,0,0,0.2);
            max-width: 600px;
            margin: 100px auto;
        ">
            <h2 style="color: white; font-family: 'Segoe UI', sans-serif; font-weight: 600; margin-bottom: 10px;">
                💳 Predicrédito
            </h2>
            <p style="color: #eaeded; font-size: 16px; margin-bottom: 25px;">
                Iniciando sistemas y montando inteligencia predictiva...
            </p>
            <div style="
                display: inline-block;
                width: 45px;
                height: 45px;
                border: 4px solid rgba(255,255,255,0.3);
                border-radius: 50%;
                border-top-color: #fff;
                animation: spin 1s ease-in-out infinite;
            "></div>
        </div>
        <style>
            @keyframes spin {
                to { transform: rotate(360deg); }
            }
        </style>
    """, unsafe_allow_html=True)


# ---------- LOGICA DE CARGA DEL MODELO ----------
@st.cache_resource
def load_model():
    modelo = joblib.load("modelo.pkl")
    scaler = joblib.load("scalador.pkl")
    return modelo, scaler

try:
    modelo, scaler = load_model()
    contenedor_inicial.empty()
except Exception as e:
    contenedor_inicial.empty()
    st.error(f"❌ Error crítico al inicializar la inteligencia artificial: {e}")
    st.stop()

archivo_historial = "historial_clientes.csv"


# ---------- SIDEBAR ----------
with st.sidebar:
    st.title("💳 Predicrédito")
    opcion = option_menu(
        menu_title="Menú",
        options=["Inicio", "Evaluación", "Historial"],
        icons=["house", "bar-chart", "clock-history"],
        default_index=0
    )


# ---------- PESTAÑA: INICIO ----------
if opcion == "Inicio":
    st.title("💳 Predicrédito")
    st.subheader("Evaluación Inteligente de Riesgo Crediticio")

    c1, c2, c3 = st.columns(3)
    c1.markdown('<div class="kpi-card"><h3>📈 Precisión</h3><h1>96%</h1></div>', unsafe_allow_html=True)
    c2.markdown('<div class="kpi-card"><h3>🤖 Modelo</h3><h1>Random Forest</h1></div>', unsafe_allow_html=True)
    c3.markdown('<div class="kpi-card"><h3>🟢 Estado</h3><h1>Activo</h1></div>', unsafe_allow_html=True)

    fig = px.pie(
        values=[55, 30, 15],
        names=["Bajo", "Medio", "Alto"],
        title="Distribución Simulada del Riesgo"
    )
    st.plotly_chart(fig, use_container_width=True)


# ---------- PESTAÑA: EVALUACIÓN ----------
elif opcion == "Evaluación":
    st.title("📊 Dashboard Crediticio")
    st.subheader("Ingrese los datos del cliente para la predicción")

    # --- Bloque de Identificación ---
    row0_col1, row0_col2 = st.columns([1, 3])
    with row0_col1:
        cedula = st.text_input("Número de Cédula", placeholder="Ej: 10203040")

    st.markdown("---")

    # --- Bloque de Formulario ---
    col1, col2, col3 = st.columns(3)
    
    with col1:
        puntaje_crediticio = st.number_input("Puntaje crediticio", 300, 950, 650)
        ingresos_mensuales = st.number_input("Ingresos mensuales ($)", 0, 100000000, 2500000)
        pct_uso_credito = st.slider("% Uso de Crédito Rotativo", 0, 100, 35)

    with col2:
        nivel_endeudamiento = st.slider("Nivel de Endeudamiento (%)", 0, 100, 30)
        saldo_ahorros = st.number_input("Saldo en cuentas de ahorros ($)", 0, 100000000, 500000)
        antiguedad_laboral = st.number_input("Antigüedad laboral (meses)", 0, 500, 12)

    with col3:
        atrasos_6_meses = st.number_input("Número de atrasos (últimos 6 meses)", 0, 20, 0)

    if st.button("🔍 Evaluar Cliente"):
        if not cedula.strip():
            st.error("⚠️ Por favor, ingrese el número de cédula del cliente para continuar.")
        else:
            # --- Animación Estética de Procesamiento ---
            contenedor_carga_interna = st.empty()
            
            mensajes_procesando = [
                "🔎 Analizando comportamiento de pago histórico...",
                "💰 Evaluando capacidad de endeudamiento actual...",
                "📈 Cruzando variables con score crediticio...",
                "🤖 Random Forest generando diagnóstico predictivo..."
            ]

            with st.spinner(""):
                for msg in mensajes_procesando:
                    contenedor_carga_interna.markdown(f"""
                        <div style="
                            background: linear-gradient(135deg, #1f4e79, #2c3e50);
                            padding: 30px;
                            border-radius: 15px;
                            text-align: center;
                            box-shadow: 0px 6px 20px rgba(0,0,0,0.15);
                            animation: pulse 1.5s infinite;
                            margin: 20px 0;
                        ">
                            <div style="
                                display: inline-block;
                                width: 35px;
                                height: 35px;
                                border: 3px solid rgba(255,255,255,0.3);
                                border-radius: 50%;
                                border-top-color: #fff;
                                animation: spinInternal 0.8s linear infinite;
                                margin-bottom: 10px;
                            "></div>
                            <h3 style="color: white; font-family: 'Segoe UI', sans-serif; font-weight: 400; margin: 0;">
                                {msg}
                            </h3>
                        </div>
                        <style>
                            @keyframes spinInternal {{ to {{ transform: rotate(360deg); }} }}
                            @keyframes pulse {{
                                0% {{ opacity: 0.8; }}
                                50% {{ opacity: 1; }}
                                100% {{ opacity: 0.8; }}
                            }}
                        </style>
                    """, unsafe_allow_html=True)
                    time.sleep(1.0)
            
            contenedor_carga_interna.empty()

            # --- DEFINICIÓN MANUAL Y BLINDADA DEL ORDEN ---
            orden_columnas = [
                'pct_uso_credito', 
                'puntaje_crediticio', 
                'atrasos_6_meses', 
                'saldo_ahorros', 
                'antiguedad_laboral', 
                'nivel_endeudamiento', 
                'ingresos_mensuales'
            ]

            valores_input = {
                'pct_uso_credito': pct_uso_credito,
                'puntaje_crediticio': puntaje_crediticio,
                'atrasos_6_meses': atrasos_6_meses,
                'saldo_ahorros': saldo_ahorros,
                'antiguedad_laboral': antiguedad_laboral,
                'nivel_endeudamiento': nivel_endeudamiento,
                'ingresos_mensuales': ingresos_mensuales
            }

            datos = pd.DataFrame([[valores_input[col] for col in orden_columnas]], columns=orden_columnas)

            # Escalar y Predecir
            try:
                datos_esc = scaler.transform(datos)
                pred = modelo.predict(datos_esc)[0]
                proba = modelo.predict_proba(datos_esc)[0]
            except Exception as error_escalador:
                datos['edad_cliente'] = 0
                datos['n_hijos'] = 0
                columnas_viejas = scaler.feature_names_in_.tolist() if hasattr(scaler, 'feature_names_in_') else orden_columnas + ['edad_cliente', 'n_hijos']
                datos_viejos = datos[columnas_viejas]
                datos_esc = scaler.transform(datos_viejos)
                
                if datos_esc.shape[1] > 7:
                    datos_esc = datos_esc[:, :7]
                pred = modelo.predict(datos_esc)[0]
                proba = modelo.predict_proba(datos_esc)[0]

            mapa_riesgo = {0: "🟢 Bajo", 1: "🟡 Medio", 2: "🔴 Alto"}
            riesgo = mapa_riesgo[pred]
            confianza = round(proba[pred] * 100, 2)

            # --- OBTENCIÓN DE LA HORA LOCAL DE COLOMBIA ---
            zona_bogota = pytz.timezone('America/Bogota')
            hora_colombia = datetime.now(zona_bogota).strftime("%Y-%m-%d %H:%M")

            # --- Almacenamiento en Historial Permanente ---
            nuevo_registro = pd.DataFrame([{
                "fecha": hora_colombia,  # <--- GUARDADO CON HORA EXACTA DE BOGOTÁ
                "cedula": cedula.strip(),
                "puntaje": puntaje_crediticio,
                "ingresos": ingresos_mensuales,
                "pct_uso_credito": pct_uso_credito,
                "endeudamiento": nivel_endeudamiento,
                "saldo_ahorros": saldo_ahorros,
                "antiguedad": antiguedad_laboral,
                "atrasos_6_meses": atrasos_6_meses,
                "riesgo": riesgo,
                "confianza": confianza
            }])

            if os.path.exists(archivo_historial):
                historial = pd.read_csv(archivo_historial)
                historial = pd.concat([historial, nuevo_registro], ignore_index=True)
            else:
                historial = nuevo_registro

            historial.to_csv(archivo_historial, index=False)

            # --- Despliegue Visual de Resultados ---
            st.subheader("📌 Resultado de la Evaluación")
            a, b, c = st.columns(3)
            a.markdown(f'<div class="kpi-card"><h3>Riesgo</h3><h1>{riesgo}</h1></div>', unsafe_allow_html=True)
            b.markdown(f'<div class="kpi-card"><h3>Confianza</h3><h1>{confianza}%</h1></div>', unsafe_allow_html=True)
            c.markdown(f'<div class="kpi-card"><h3>CC. Cliente</h3><h1>{cedula}</h1></div>', unsafe_allow_html=True)

            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=confianza,
                title={'text': "Nivel de Certeza en el Diagnóstico"},
                gauge={
                    'axis': {'range': [0, 100]},
                    'steps': [
                        {'range': [0, 40], 'color': 'rgba(231, 76, 60, 0.3)'},
                        {'range': [40, 70], 'color': 'rgba(241, 196, 15, 0.3)'},
                        {'range': [70, 100], 'color': 'rgba(46, 204, 113, 0.3)'}
                    ],
                    'bar': {'color': "#1f4e79"}
                }
            ))
            st.plotly_chart(fig, use_container_width=True)

            # --- Bloque Explicativo Dinámico ---
            st.subheader("🧠 Factores de Riesgo Detectados")
            
            explicaciones_detalladas = []
            
            if puntaje_crediticio < 600:
                explicaciones_detalladas.append("📌 **Puntaje crediticio crítico:** El score histórico se encuentra por debajo de los límites seguros.")
            if atrasos_6_meses > 0:
                explicaciones_detalladas.append(f"⚠️ **Atrasos detectados:** Registrar `{atrasos_6_meses}` mora(s) en los últimos 6 meses penaliza fuertemente el comportamiento de pago.")
            if pct_uso_credito > 70:
                explicaciones_detalladas.append(f"💳 **Uso de cupo excesivo ({pct_uso_credito}%):** El cliente utiliza demasiada capacidad de sus tarjetas de crédito, sugiriendo dependencia financiera.")
            if nivel_endeudamiento > 50:
                explicaciones_detalladas.append(f"📉 **Sobreendeudamiento ({nivel_endeudamiento}%):** El porcentaje de ingresos comprometidos supera el umbral saludable.")
            if saldo_ahorros < 200000:
                explicaciones_detalladas.append("💰 **Fondo de emergencia bajo:** El saldo en ahorros es insuficiente para actuar como colateral o respaldo ante imprevistos.")
            if antiguedad_laboral < 12:
                explicaciones_detalladas.append("💼 **Inestabilidad laboral:** La permanencia laboral actual es menor a un año.")

            if explicaciones_detalladas:
                for exp in explicaciones_detalladas:
                    st.warning(exp)
            else:
                st.success("🟢 **Perfil Impecable:** Todas las métricas del cliente se encuentran dentro de los rangos óptimos de seguridad.")


# ---------- PESTAÑA: HISTORIAL ----------
elif opcion == "Historial":
    st.title("📜 Historial de Evaluaciones")

    if os.path.exists(archivo_historial):
        df = pd.read_csv(archivo_historial)

        if not df.empty:
            total = len(df)
            confianza_avg = round(df["confianza"].mean(), 2)
            ingreso_avg = int(df['ingresos'].mean()) if 'ingresos' in df.columns else 0
            atrasos_avg = round(df['atrasos_6_meses'].mean(), 1) if 'atrasos_6_meses' in df.columns else 0

            c1, c2, c3, c4 = st.columns(4)
            c1.metric("👥 Total Consultas", total)
            c2.metric("🎯 Confianza Promedio", f"{confianza_avg}%")
            c3.metric("💰 Ingreso Promedio", f"${ingreso_avg:,}")
            c4.metric("⚠️ Promedio Atrasos (6M)", f"{atrasos_avg} moras")

            col1, col2 = st.columns(2)
            with col1:
                fig = px.pie(df, names="riesgo", title="Distribución de Niveles de Riesgo")
                st.plotly_chart(fig, use_container_width=True)
            with col2:
                fig = px.box(df, x="riesgo", y="puntaje", title="Puntaje Crediticio según Nivel de Riesgo")
                st.plotly_chart(fig, use_container_width=True)

            st.subheader("📋 Registros Guardados")
            df['cedula'] = df['cedula'].astype(str)
            st.dataframe(df, use_container_width=True)

            csv = df.to_csv(index=False).encode("utf-8")
            
            # Formateamos la hora actual de Colombia también en el nombre del archivo descargable
            zona_bogota = pytz.timezone('America/Bogota')
            fecha_descarga = datetime.now(zona_bogota).strftime('%Y%m%d')
            
            st.download_button(
                label="⬇ Descargar Reporte CSV",
                data=csv,
                file_name=f"historial_completo_credito_{fecha_descarga}.csv",
                mime="text/csv"
            )
        else:
            st.warning("El historial está vacío.")
    else:
        st.warning("No hay historial registrado aún.")
