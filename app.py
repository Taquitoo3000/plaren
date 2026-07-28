import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, text
from database import get_catalogo, guardar_respuesta

st.set_page_config(
    page_title="PLAREN",
    page_icon="assets/icon_sectech.png",
    menu_items={
        'Report a bug': 'https://sectechnologies.vercel.app/',
        'About': "# PLAREN\nPlataforma de Revisión Normativa."
    }
)
st.markdown("""
    <style>
    [data-testid="stHeaderActionElements"] {
        display: none !important;
    }
    </style>
""", unsafe_allow_html=True)

# ============================================
# NAVEGACIÓN CON SESSION STATE
# ============================================
if "pagina" not in st.session_state:
    st.session_state.pagina = "inicio"

if "capitulo_actual" not in st.session_state:
    st.session_state.capitulo_actual = None


def ir_a_capitulo(nombre_capitulo):
    st.session_state.capitulo_actual = nombre_capitulo
    st.session_state.pagina = "capitulo"
    # Limpiar selects al entrar a un capítulo nuevo
    for k in ["sel_seccion", "sel_articulo", "sel_fraccion"]:
        if k in st.session_state:
            del st.session_state[k]
    st.rerun()


def volver_a_inicio():
    st.session_state.pagina = "inicio"
    st.session_state.capitulo_actual = None
    for k in ["sel_seccion", "sel_articulo", "sel_fraccion"]:
        if k in st.session_state:
            del st.session_state[k]
    st.rerun()

def render_footer():
    st.markdown("""
    <hr>
    <div style="text-align: center; color: grey; font-size: 0.9em;">
        © 2026 COPRAEDEG |
        Desarrollado por <a href="https://taquitoo3000.github.io/isael/" style="color: mediumorchid;">SECtech</a>
    </div>
    """, unsafe_allow_html=True)


# ============================================
# PÁGINA DE INICIO — ÍNDICE DE 8 CAPÍTULOS
# ============================================
if st.session_state.pagina == "inicio":
    st.title("PLAREN",text_alignment="center")
    #st.subheader("Plataforma de Revisión Normativa del Consejo para Prevenir, Atender y Erradicar la Discriminación en el Estado de Guanajuato",
    #             text_alignment="center")
    st.markdown("""
        <div style="
            background: #8055AB;
            padding: 0px;
            border-radius: 12px;
            margin-bottom: 0px;
            text-align: center;
        ">
            <h4 style="color: white; margin: 0;">Plataforma de Revisión Normativa del Consejo para Prevenir, Atender y Erradicar la Discriminación en el Estado de Guanajuato</h4>
        </div>
    """, unsafe_allow_html=True)
    st.markdown("### Índice")
    st.divider()

    catalogo, leyes = get_catalogo()
    capitulos = catalogo['capitulo'].drop_duplicates().tolist()

    cols = st.columns(2)
    for i, nombre in enumerate(capitulos):
        with cols[i % 2]:
            with st.container(border=True):
                st.subheader(nombre,text_alignment="center")
                if st.button(f"Entrar", key=f"btn_{i}", use_container_width=True):
                    ir_a_capitulo(nombre)


# ============================================
# PÁGINA DE CAPÍTULO — SECCIÓN → ARTÍCULO → FRACCIÓN → OPINIÓN
# ============================================
elif st.session_state.pagina == "capitulo":
    capitulo = st.session_state.capitulo_actual
    catalogo, leyes = get_catalogo()

    if st.button("⬅️ Volver al índice", type="secondary"):
        volver_a_inicio()

    st.title(f"📖 {capitulo}")
    st.divider()

    # ---------- 1. ¿SELECCIONAR SECCIÓN? ----------
    secciones = catalogo[catalogo['capitulo']==capitulo]
    secciones = secciones['seccion'].drop_duplicates().tolist()
    secciones = [s for s in secciones if s != ""]

    if secciones:
        seccion = st.selectbox("🔹 Sección:", secciones, key="sel_seccion")
    else:
        seccion = ""

    # ---------- 2. SELECCIONAR RESUMEN ----------
    resumenes = catalogo[
        (catalogo['capitulo']==capitulo) &
        (catalogo['seccion']==seccion)
    ]
    resumenes = resumenes['resumen'].drop_duplicates().tolist()
    resumen = st.selectbox("🔹 Resumen:", resumenes, key="sel_resumen")
    # ---------- 3. SELECCIONAR ARTÍCULO ----------
    articulos = catalogo[
        (catalogo['capitulo']==capitulo) &
        (catalogo['seccion']==seccion) &
        (catalogo['resumen']==resumen)
    ]
    articulos = articulos['articulo'].drop_duplicates().tolist()
    articulo = st.selectbox("🔹 Artículo:", articulos, key="sel_articulo")
    # ---------- 3. ¿SELECCIONAR FRACCIÓN? ----------
    fracciones = catalogo[
        (catalogo['capitulo']==capitulo) &
        (catalogo['seccion']==seccion) &
        (catalogo['resumen']==resumen) &
        (catalogo['articulo']==articulo)
    ]
    fracciones = fracciones['fraccion'].drop_duplicates().tolist()
    fracciones = [f for f in fracciones if f != ""]
    if fracciones:
        fraccion = st.selectbox(
            "🔹 Fracción:",
            fracciones,
            key="sel_fraccion"
        )
    else: fraccion=""

    # Obtener id y texto de la fracción
    ley_id= catalogo[
        (catalogo['capitulo']==capitulo) &
        (catalogo['seccion']==seccion) &
        (catalogo['resumen']==resumen) &
        (catalogo['articulo']==articulo) &
        (catalogo['fraccion']==fraccion)
    ]['id']

    st.divider()
    st.markdown(f"### {capitulo}: {seccion}\n\n{resumen}\n\n{articulo}\n\n{fraccion}")
    st.divider()

    st.subheader("📝 Tu opinión")
    with st.container(border=True):

        opinion = st.text_area(
            "**Escribe tu opinión:**",
            height=150,
            key=f"op_{ley_id}"  # ← key para que no se borre entre reruns
        )
        
        st.markdown("**Tipo de Impacto**")

        pres_bolean=st.radio(
            "Presupuestal",
            options=['Sí requiere esfuerzo presupuestal','No requiere esfuerzo presupuestal'],
            index=1
        )
        presupues = (pres_bolean == 'Sí requiere esfuerzo presupuestal')

        jur_bolean=st.radio(
            "Jurídico",
            options=['Sí requiere entramado normativo','No requiere entramado normativo'],
            index=1
        )
        jur_bolean = (jur_bolean == 'Sí requiere entramado normativo')
        ley = st.multiselect(
            "Leyes que trastoca:",
            leyes['titulo'].to_list(),
            disabled=not jur_bolean,
            key=f"ley_{ley_id}"
        )

        soc_bolean=st.radio(
            "Social",
            options=['Sí involucra grupos prioritarios','No involucra grupos prioritarios'],
            index=1
        )
        soc_bolean = (soc_bolean == 'Sí involucra grupos prioritarios')
        grupo_vul = st.multiselect(
            "Grupos vulnerables afectados:",
            [
                'Discapacidad Mental',
                'Discapacidad Motriz',
                'Discapacidad Orgánica',
                'Discapacidad Psicosocial',
                'Discapacidad Sensorial',
                'Estudiantes',
                'Minorías nacionales o religiosas',
                'Mujeres, niñas o adolescentes',
                'Niñas, niños y adolescentes',
                'Periodistas',
                'Persona en situación de movilidad',
                'Personas de edad',
                'Personas de la diversidad sexogenérica',
                'Personas defensoras de Derechos Humanos -Activistas-',
                'Personas defensoras de Derechos Humanos -Colectivos de Búsqueda de Personas Desaparecidas-',
                'Personas defensoras de Derechos Humanos -Defensoras Privadas-',
                'Personas defensoras de Derechos Humanos -Defensoras Públicas-',
                'Personas desaparecidas',
                'Personas en situación de calle',
                'Personas privadas de la libertad',
                'Población afromexicana',
                'Población indígena',
                'Víctimas'
            ],
            disabled=not soc_bolean,
            key=f"gru_{ley_id}"
        )
        enviar = st.button("💾 Guardar opinión", use_container_width=True, key=f"btn_{ley_id}")

    if enviar:
        if opinion.strip() == "":
            st.warning("⚠️ El campo está vacío. Escribe algo antes de guardar.")
        elif ley_id is None:
            st.error("❌ No se pudo identificar el registro de la ley. No se guardó.")
        else:
            ley_final = ley if jur_bolean else []
            grupo_vul_final = grupo_vul if soc_bolean else []
            exito = guardar_respuesta(int(ley_id.iloc[0]), opinion.strip(), presupues, ley_final, grupo_vul_final)
            if exito:
                st.success("✅ ¡Opinión guardada correctamente!")
                st.balloons()
            else:
                st.error("❌ No se pudo guardar.")

render_footer()