# 💳 Predicrédito — Sistema Predictivo de Riesgo Crediticio Automático

Este repositorio aloja el código fuente completo de **Predicrédito**, una solución basada en Inteligencia Artificial y Machine Learning diseñada específicamente para la pre-aprobación automatizada y la clasificación del riesgo financiero en créditos vehiculares, tomando como caso de estudio la optimización de los procesos operativos de la entidad de credito en la ciudad de Bogotá, Colombia.

---

## 🚀 1. Problema o Necesidad Solucionada mediante IA
En el contexto financiero de Bogotá, la evaluación de solicitudes de crédito de vehículos suele depender de revisiones manuales exhaustivas o de matrices estadísticas rígidas de puntuación (*Scorecards*). Este enfoque analógico genera tres problemas operativos críticos:
* **Altos tiempos de respuesta:** Procesos lentos y complejos para dictaminar la viabilidad de un cliente, lo que genera fricción comercial y pérdida de prospectos.
* **Subjetividad y riesgo de default:** Margen de error humano latente que puede derivar en la aprobación involuntaria de perfiles de alta morosidad.
* **Falta de escalabilidad:** Incapacidad de procesar, cruzar y ponderar múltiples variables financieras simultáneamente en tiempo real.

**Predicrédito** resuelve esta necesidad transformando el proceso manual en un sistema automatizado, ágil y objetivo fundamentado en Machine Learning, reduciendo la subjetividad institucional y blindando la seguridad financiera de la organización.

---

## 🛠️ 2. Librerías, Frameworks y Recursos Utilizados
El ecosistema tecnológico del proyecto fue seleccionado para garantizar un procesamiento matemático eficiente y una experiencia fluida de usuario:
* **Pandas & NumPy:** Manipulación, limpieza y procesamiento matricial de las estructuras de datos y simulación estadística de perfiles.
* **Scikit-Learn (Sklearn):** Pipeline completo de Machine Learning, incluyendo el preprocesamiento (`MinMaxScaler`), modelado (`RandomForestClassifier`, `LogisticRegression`, `GradientBoostingClassifier`) y métricas de validación.
* **Joblib:** Serialización y exportación binaria de los archivos de variables persistidas (`modelo.pkl` y `scalador.pkl`).
* **Streamlit:** Framework principal para el desarrollo de la interfaz de usuario web y control de la lógica frontend/backend.
* **Pytz:** Sincronización horaria nativa para la persistencia del historial bajo la zona oficial de Colombia (`America/Bogota`).
* **Matplotlib & Seaborn:** Generación de gráficos analíticos y visualización de matrices de confusión durante la fase de desarrollo en el notebook.

---

## 📊 3. Construcción del Dataset y Balanceo Perfecto
El dataset del proyecto fue diseñado mediante un pipeline de generación sintética controlada que simula perfiles socioeconómicos reales mediante distribuciones estadísticas específicas (Normal, Uniforme y Poisson) agrupadas en tres grandes semillas operativas:
* **Perfil de Riesgo Bajo:** Clientes con altos puntajes crediticios (media de 820), ingresos elevados (media de $6.000.000 COP), baja tasa de endeudamiento (15%), alta estabilidad laboral (60 meses) y cero atrasos recientes.
* **Perfil de Riesgo Medio:** Clientes con scores intermedios (media de 640), ingresos promedio ($3.500.000 COP), endeudamiento del 45% e historial de moras bajo (distribución de Poisson con &lambda;=0.7).
* **Perfil de Riesgo Alto:** Clientes con historial crediticio penalizado (media de 400), bajos ingresos ($1.800.000 COP), alto endeudamiento (75%) y atrasos frecuentes (Poisson con &lambda;=2.2).

### ⚖️ Estrategia de Balanceo y Prevención de Sesgos
Para entrenar de forma óptima el modelo, se utilizaron **24,000 registros totales** distribuidos equitativamente. Con el fin de evitar sesgos algorítmicos hacia una clase específica, se implementó un proceso de balanceo perfecto utilizando la función `pd.qcut()` de Pandas. Este método calcula un indicador de riesgo compuesto continuo y divide matemáticamente el dataset en tres grupos con la **exacta cantidad de filas (33.33% por categoría)**, garantizando una equidad estadística absoluta entre las clases objetivo:
* `0`: Riesgo Bajo (Aprobado)
* `1`: Riesgo Medio (Requiere Estudio Adicional)
* `2`: Riesgo Alto (Rechazado)

---

## 🧠 4. Selección de Variables por Consenso Multi-Modelo
Con el propósito de descartar variables con ruido o que indujeran al modelo a cometer "trampa" (como la puntuación técnica continua base, la cual fue eliminada del dataframe), se desarrolló un algoritmo avanzado de **Selección de Variables por Consenso**: 
1. Se entrenaron de manera del todo simultánea tres modelos evaluadores: *Random Forest, Gradient Boosting y Regresión Logística*.
2. Las relevancias e importancias de características otorgadas por cada uno de estos algoritmos fueron transformadas a una escala homogénea de 0 a 1 mediante `MinMaxScaler`.
3. Se calculó el Promedio de Consenso reuniendo los votos ponderados de los tres modelos.

El sistema seleccionó de manera exitosa el **TOP 7 de Variables Definitivas**, las cuales son las únicas requeridas para alimentar el modelo final y realizar las inferencias en la app web:
1.  `pct_uso_credito` (Porcentaje de utilización de cupos rotativos)
2.  `puntaje_crediticio` (Score del buró de crédito/DataCrédito)
3.  `atrasos_6_meses` (Número de cuotas en mora en el último semestre)
4.  `saldo_ahorros` (Liquidez de respaldo financiero)
5.  `antiguedad_laboral` (Estabilidad en el empleo actual expresada en meses)
6.  `nivel_endeudamiento` (Porcentaje de ingresos mensuales comprometidos)
7.  `ingresos_mensuales` (Capacidad adquisitiva declarada del solicitante)

---

## 📉 5. Benchmarking y Elección del Modelo Final
Para la asignación definitiva del motor predictivo, se llevó a cabo un proceso de evaluación comparativa entrenando los modelos sobre una división del conjunto de datos del **80% para entrenamiento y 20% para test**, aplicando una estratificación estricta (`stratify=y`) para conservar las proporciones perfectas en las muestras.

### 📊 Tabla Comparativa de Rendimiento Final:
* **Random Forest Classifier:** **96.00%** de Accuracy en Test | F1-Score: 96.00% | Varianza en Validación Cruzada (CV Std): Mínima | Tiempo de cómputo óptimo.
* **Gradient Boosting Classifier:** 95.80% de Accuracy | Alto rendimiento en entrenamiento pero menor capacidad de generalización en fronteras difusas.
* **Logistic Regression:** Rendimiento significativamente inferior debido a su incapacidad inherente de modelar relaciones e interacciones no lineales entre las variables financieras.

### 🔬 Justificación Técnica de la Elección:
Se seleccionó de forma definitiva **Random Forest Classifier** debido a que demostró el mejor comportamiento de generalización en las matrices de confusión. Su arquitectura basada en múltiples árboles de decisión independientes reduce drásticamente el sobreajuste (*overfitting*), maneja con robustez valores atípicos (outliers) y genera salidas probabilísticas estables que permiten construir un medidor de aguja interactivo y transparente para el usuario final. El modelo fue exportado mediante joblib como `modelo.pkl` junto con el escalador ajustado exclusivamente para las 7 variables seleccionadas (`scalador.pkl`).

---

## 🖥️ 6. Arquitectura, Frontend y Backend de la Solución Digital
La solución fue llevada a la web integrando la lógica analítica de datos en un entorno productivo distribuido:
* **Backend (Motor Predictivo):** Construido sobre Python. Emplea la directiva `st.cache_resource` de Streamlit para cargar de manera diferida los archivos binarios serializados `modelo.pkl` y `scalador.pkl`. Esto asegura que el modelo se mantenga residente en memoria y resuelva las inferencias en microsegundos, optimizando el uso de la CPU del servidor.
* **Frontend (Interfaz de Usuario):** Desarrollado completamente en Streamlit, ofreciendo un diseño limpio con un panel de navegación estructurado en tres grandes módulos:
    1.  **Inicio:** Presentación corporativa, métricas clave del modelo (96.00% de precisión) y distribución global de la data.
    2.  **Evaluación de Clientes:** Panel operativo interactivo equipado con sliders y selectores numéricos para la digitación segura de los datos financieros.
    3.  **Historial de Consultas:** Cuadro de mando administrativo para visualización y monitoreo de auditoría.

---

## ⚙️ 7. Explicabilidad, Reglas de Negocio e Integración del Sistema
El sistema no se comporta como una "caja negra"; utiliza las predicciones probabilísticas para desencadenar lógicas personalizadas dentro del flujo operativo de la entidad crediticia:
* **Validación de Identidad Obligatoria:** Exige la digitación del número de Cédula de Ciudadanía; si el campo está vacío, bloquea automáticamente los cálculos previniendo registros anónimos.
* **Semáforo de Riesgo Dinámico:** Traduce la clase predicha en un componente visual semántico inmediato para el asesor: `Riesgo Bajo (Verde / Aprobación Directa)`, `Riesgo Medio (Amarillo / Requiere Co-deudor)` o `Riesgo Alto (Rojo / Rechazo Automático)`.
* **Gráfico de Aguja Interactivo (*Gauge Chart*):** Extrae las probabilidades asociadas a la predicción usando `predict_proba()` y grafica de manera exacta el nivel de certeza con el que el modelo emitió el veredicto.
* **Tarjetas de Alerta Contextuales:** Mediante reglas condicionales empotradas en la interfaz, si el cliente posee variables fuera de rango (como un score menor a 500 o más de 2 retrasos), el frontend despliega advertencias dinámicas explicándole al asesor el porqué del dictamen de la IA.
* **Persistencia Local y Control Horario Nativo:** Cada evaluación realizada se añade al instante como una fila inmutable en un archivo centralizado `historial_creditos.csv`. Para cumplir con las normativas de auditoría interna de la organización, se acopló la librería `pytz` forzando la zona horaria de `America/Bogota`. Esto previene desfases horariós comunes de los servidores de Streamlit Cloud, garantizando marcas de tiempo precisas para Colombia.

---
*Desarrollado de manera íntegra como proyecto final práctico para la asignatura de Inteligencia Artificial por Daniel Alejandro Jaime Díaz.*
