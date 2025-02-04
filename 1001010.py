import datetime
from collections import defaultdict
from typing import List, Dict, Any, Optional

def calcular_estadisticas_pacientes(
    registros: List[Dict[str, Any]],
    fecha_inicio: datetime.date,
    fecha_fin: datetime.date,
    campo_metrica: Optional[str] = None
) -> Dict[str, Dict[str, float]]:
    """
    Calcula la cantidad de pacientes por tipo de enfermedad y, opcionalmente,
    el promedio de una métrica adicional si se indica `campo_metrica`.

    Parámetros:
        - registros: lista de diccionarios, donde cada uno representa la información de un paciente.
        Se espera que cada registro tenga, al menos, las claves "fechaIngreso" y "tipoEnfermedad".
        La fecha puede estar en formato datetime.date o en cadena con formato "YYYY-MM-DD".
        - fecha_inicio: fecha de inicio del intervalo (inclusive).
        - fecha_fin: fecha de fin del intervalo (inclusive).
        - campo_metrica: (opcional) nombre del campo numérico del registro que se utilizará para calcular un promedio.

    Retorna:
        Un diccionario donde la clave es el tipo de enfermedad y el valor es otro diccionario con:
            - "cantidad": cantidad de pacientes en el intervalo.
            - "promedio": promedio de la métrica, si se indicó `campo_metrica`.
    """
    # Diccionario para acumular resultados. Cada clave (tipo de enfermedad) tiene:
    # - "count": contador de pacientes.
    # - "sum_metric": suma acumulada del campo de la métrica (si se solicita).
    resultados = defaultdict(lambda: {"count": 0, "sum_metric": 0.0})
    
    for registro in registros:
        # Obtención y normalización de la fecha de ingreso.
        fecha_ingreso = registro.get("fechaIngreso")
        if isinstance(fecha_ingreso, str):
            try:
                fecha_ingreso = datetime.datetime.strptime(fecha_ingreso, "%Y-%m-%d").date()
            except ValueError:
                # Si el formato no es el esperado, se omite el registro.
                continue
        
        # Se verifica que la fecha esté dentro del intervalo
        if fecha_ingreso is None or not (fecha_inicio <= fecha_ingreso <= fecha_fin):
            continue
        
        # Se obtiene el tipo de enfermedad y se actualiza el contador.
        tipo = registro.get("tipoEnfermedad")
        if not tipo:
            continue  # se omite si no se especifica el tipo
        
        resultados[tipo]["count"] += 1
        
        # Si se requiere calcular la métrica adicional y el registro la posee:
        if campo_metrica and campo_metrica in registro:
            try:
                valor = float(registro[campo_metrica])
                resultados[tipo]["sum_metric"] += valor
            except (ValueError, TypeError):
                # Se ignora el valor si no es convertible a float.
                pass

    # Preparar el diccionario final con los resultados.
    estadisticas = {}
    for tipo, data in resultados.items():
        estadisticas[tipo] = {"cantidad": data["count"]}
        if campo_metrica:
            # Se calcula el promedio siempre que la cantidad sea mayor a 0.
            promedio = data["sum_metric"] / data["count"] if data["count"] > 0 else 0.0
            estadisticas[tipo]["promedio"] = promedio

    return estadisticas

# Ejemplo de uso:
if __name__ == "__main__":
    # Datos de ejemplo
    datos_pacientes = [
        {"ID": 1, "fechaIngreso": "2025-01-10", "tipoEnfermedad": "VIH", "tiempoHospitalizacion": 5},
        {"ID": 2, "fechaIngreso": "2025-01-15", "tipoEnfermedad": "HCV", "tiempoHospitalizacion": 3},
        {"ID": 3, "fechaIngreso": "2025-01-20", "tipoEnfermedad": "HBV", "tiempoHospitalizacion": 4},
        {"ID": 4, "fechaIngreso": "2025-01-25", "tipoEnfermedad": "VIH", "tiempoHospitalizacion": 6},
        {"ID": 5, "fechaIngreso": "2025-02-05", "tipoEnfermedad": "HCV", "tiempoHospitalizacion": 2},
        # Otros registros...
    ]
    print(calcular_estadisticas_pacientes(datos_pacientes,datetime.date(2025,1,10),datetime.date(2025,2,4),"tiempoHospitalizacion"))
    
