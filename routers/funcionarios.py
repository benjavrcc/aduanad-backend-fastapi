# routers/funcionarios.py

from fastapi import APIRouter
from pydantic import BaseModel
import pandas as pd
from utils.hourly_distribution import distribute_expected_by_hour
import time

router = APIRouter()

# ============================
# CARGAR CSV CON E_dia
# ============================
df_expected = pd.read_csv("data/esperados_dia.csv")

# ============================
# ALMACENAMIENTO TEMPORAL (RAM)
# formato: { timestamp: {fecha, hora, cantidad} }
# ============================
TEMP_STORAGE = {}
EXPIRATION_SECONDS = 15 * 60   # 15 minutos


def clean_expired():
    """Elimina registros guardados hace más de 15 minutos."""
    now = time.time()
    to_delete = []
    for ts, record in TEMP_STORAGE.items():
        if now - ts > EXPIRATION_SECONDS:
            to_delete.append(ts)

    for ts in to_delete:
        del TEMP_STORAGE[ts]


# ============================
# MODELO PARA /registrar
# ============================
class Registro(BaseModel):
    fecha_llegada: str
    hora_llegada: str
    cantidad_viajeros: int


# ============================
# ENDPOINT /registrar
# ============================
@router.post("/registrar")
def registrar_viaje(registro: Registro):
    """
    Guarda el registro durante 15 minutos.
    """

    clean_expired()  # limpiar los viejos

    timestamp = time.time()

    TEMP_STORAGE[timestamp] = {
        "fecha": registro.fecha_llegada,
        "hora": registro.hora_llegada,
        "cantidad": registro.cantidad_viajeros
    }

    print("📌 Guardado temporal:", TEMP_STORAGE[timestamp])

    return {
        "status": "ok",
        "mensaje": "Datos recibidos y almacenados 15 minutos",
        "registrado": TEMP_STORAGE[timestamp]
    }


# ============================
# ENDPOINT para ver registros recientes (debug)
# ============================
@router.get("/registros")
def ver_registros():
    clean_expired()
    return TEMP_STORAGE


# ============================
# ENDPOINT expected-hourly/{fecha}
# ============================
@router.get("/expected-hourly/{fecha}")
def expected_hourly(fecha: str):
    row = df_expected[df_expected["fecha"] == fecha]
    if row.empty:
        return {"error": f"Fecha {fecha} no existe"}

    daily_expected = int(row["E_dia"].values[0])

    clean_expired()

    # Construir registros ponderados con viajeros
    day_records = []
    for rec in TEMP_STORAGE.values():
        if rec["fecha"] == fecha:
            day_records.append({
                "hora": rec["hora"],
                "viajeros": rec["cantidad"]
            })

    # Si no hay registros reales, usar baseline simple
    if not day_records:
        day_records = [
            {"hora": "08:00", "viajeros": 3},
            {"hora": "09:00", "viajeros": 5},
            {"hora": "14:00", "viajeros": 4}
        ]

    hourly = distribute_expected_by_hour(day_records, daily_expected)

    return {
        "fecha": fecha,
        "E_dia": daily_expected,
        "expected_hourly": hourly,
        "registros_reales": day_records
    }
