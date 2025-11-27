# utils/hourly_distribution.py

from collections import Counter

def distribute_expected_by_hour(day_records, daily_expected):
    """
    day_records: lista de horas tipo ["08:30", "09:00", "09:45"]
    daily_expected: entero E_dia desde el CSV

    Retorna: { "08": 1200, "09": 1800, ... }
    """

    if daily_expected is None or daily_expected <= 0:
        return {}

    if not day_records:
        return {}

    # Extraer solo la hora (HH) de cada registro
    hours = []
    for h in day_records:
        h_str = str(h)
        hour_only = h_str.split(":")[0]  # Ej: "08:30" → "08"
        hours.append(hour_only)

    # Contar cuántos registros hay por hora
    counts = Counter(hours)  # Ej: {"09": 2, "08": 1}

    total_records = sum(counts.values())
    if total_records == 0:
        return {}

    hourly_expectation = {}

    # Distribución proporcional
    for hour, cnt in counts.items():
        proportion = cnt / total_records
        hourly_expectation[hour] = round(daily_expected * proportion)

    return hourly_expectation
