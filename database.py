import streamlit as st
from sqlalchemy import create_engine, text
import pandas as pd

def get_engine():
    """Crea y retorna el engine de SQLAlchemy."""
    try:
        # Opción A: variables sueltas en secrets.toml
        user = st.secrets.get("DB_USER", st.secrets.get("username"))
        password = st.secrets.get("DB_PASS", st.secrets.get("password"))
        host = st.secrets.get("DB_SERVER", st.secrets.get("host"))
        port = st.secrets.get("DB_PORT", st.secrets.get("port", 3306))
        database = st.secrets.get("DB_NAME", st.secrets.get("database"))

        connection_string = (
            f"mysql+pymysql://{user}:{password}"
            f"@{host}:{port}/{database}?charset=utf8mb4"
        )
        engine = create_engine(connection_string, pool_pre_ping=True)
        return engine
    except Exception as e:
        st.error(f"Error al crear el engine: {str(e)[:200]}")
        return None

def guardar_respuesta(ley_id, respuesta, presupuestal, juridico, social):
    "Inserta una opinión en la base de datos."
    engine = get_engine()
    if engine is None:
        return False
    try:
        with engine.connect() as conn:
            conn.execute(text("""
                INSERT INTO copraedeg_opiniones
                (ley_id, respuesta, impacto_presupuestal, impacto_juridico, impacto_social)
                VALUES (:ley_id, :resp, :pres, :jur, :soc)
            """), {
                "ley_id": ley_id,
                "resp": respuesta,
                "pres": 1 if presupuestal else 0,
                "jur": " | ".join(juridico) if juridico else None,
                "soc": " | ".join(social) if social else None,
            })
            conn.commit()
        return True
    except Exception as e:
        st.error(f"Error al guardar la opinión: {e}")
        return False

@st.cache_data(ttl=900)
def get_catalogo():
    engine = get_engine()
    try:
        df = pd.read_sql("SELECT * FROM copraedeg_ley", engine)
        df2 = pd.read_sql("select * from copraedeg_leyes_congreso", engine)
        df = df.fillna("")
        return df, df2
    except Exception as e:
        st.error(f"Error al obtener catalogo: {e}")
        return None