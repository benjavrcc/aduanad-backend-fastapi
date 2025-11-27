# utils/hourly_distribution.py

def distribute_expected_by_hour(day_records, daily_expected, min_weight=1):
    """
    day_records: lista de dicts con {"hora": "HH:MM", "viajeros": X}
       ejemplo:
       [
         {"hora": "08:30", "viajeros": 3},
         {"hora": "09:00", "viajeros": 1},
         {"hora": "09:45", "viajeros": 40}
       ]

    daily_expected: entero E_dia del CSV

    min_weight: peso mínimo para TODAS las horas (default 1)
    """

    # Inicializar todas las horas con peso mínimo
    hour_weights = {str(h).zfill(2): min_weight for h in range(24)}

    # Sumar pesos reales según viajeros
    for rec in day_records:
        hora = str(rec["hora"]).split(":")[0]
        viajeros = rec["viajeros"]
        hour_weights[hora] += viajeros

    # Calcular total de peso
    total_weight = sum(hour_weights.values())

    if total_weight == 0:
        return {}

    # Distribución proporcional
    hourly_expectation = {}
    for hour, weight in hour_weights.items():
        proportion = weight / total_weight
        hourly_expectation[hour] = round(daily_expected * proportion)

    return hourly_expectation
