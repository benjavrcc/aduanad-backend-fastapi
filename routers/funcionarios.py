# routers/funcionarios.py

from fastapi import APIRouter
import pandas as pd
from utils.hourly_distribution import distribute_expected_by_hour

router = APIRouter()

# Cargar CSV con valores esperados diarios (E_dia)
df_expected = pd.read_csv("data/esperados_dia.csv")


@router.get("/expected-hourly/{fecha}")
def expected_hourly(fecha: str):
    """
    Devuelve el valor esperado por hora para la fecha indicada (YYYY-MM-DD).
    Usa el valor E_dia del CSV.
    """

    # 1) Buscar valor esperado del día
    row = df_expected[df_expected["fecha"] == fecha]

    if row.empty:
        return {"error": f"La fecha {fecha} no existe en el CSV esperados_dia.csv"}

    daily_expected = int(row["E_dia"].values[0])

    # 2) Registros de horarios por ahora están hardcodeados (luego los conectamos a tu BD real)
    day_records = [
        "08:30",
        "09:00",
        "09:45",
        "14:00",
        "14:20",
    ]

    # 3) Distribuir el valor E_dia entre las horas registradas
    hourly = distribute_expected_by_hour(day_records, daily_expected)

    return {
        "fecha": fecha,
        "E_dia": daily_expected,
        "expected_hourly": hourly
    }
