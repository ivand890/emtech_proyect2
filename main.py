import pandas as pd

# cargar la base de datos como DataFrame de pandas
data = pd.read_csv("synergy_logistics_database.csv")

# Separar la sase de datos en importaciones y exportaciones
export_data = data[data["direction"] == "Exports"]
import_data = data[data["direction"] == "Imports"]

# Opción uno
# Agrupar las entradas a la base de datos por ruta, calcular 
# la suma total y ordenar de forma descendiente tanto para las 
# exportaciones como para las imporaciones

export_total = (
    export_data.groupby(["origin", "destination"])
    .sum()["total_value"]
    .sort_values(ascending=False)
)

import_total = (
    import_data.groupby(["origin", "destination"])
    .sum()["total_value"]
    .sort_values(ascending=False)
)

# Opción dos
# Agrupar las entradas a la base de datos por medio de transporte empleado, 
# calcular la suma total y ordenar de forma descendiente tanto para las 
# exportaciones como para las imporaciones

tmode_export = (
    export_data.groupby(["transport_mode"])
    .sum()["total_value"]
    .sort_values(ascending=False)
)
tmode_import = (
    import_data.groupby(["transport_mode"])
    .sum()["total_value"]
    .sort_values(ascending=False)
)
# Cálculo de las ganancias totales por medio de trasporte
tmode_total = (tmode_import + tmode_export).sort_values(ascending=False)

# Opción tres
# Calculo de los las rutas de importación y exportación que representan 
# el valor mas cercano al 80 % de las ganancias totales. Cálculo del 
# porcentaje real que representan esa fracción de rutas
eighty_export = export_total[export_total.cumsum() <= export_total.sum() * 4 / 5]
actual_export_percent = round(eighty_export.sum() / export_total.sum() * 100, 1)

eighty_import = import_total[import_total.cumsum() <= import_total.sum() * 4 / 5]
actual_import_percent = round(eighty_import.sum() / import_total.sum() * 100, 1)


# Guardado de las la información ya procesada en distintos archivos csv 
# para realizar la confección de gráficos en Tableau

export_total.to_csv("export_total.csv")
import_total.to_csv("import_total.csv")
tmode_export.to_csv("tmode_export.csv")
tmode_import.to_csv("tmode_import.csv")
eighty_export.to_csv("eighty_export.csv")
eighty_import.to_csv("eighty_import.csv")

pd.Series(
    {
        "actual_export_percent": actual_export_percent,
        "actual_import_percent": actual_import_percent,
    },
).to_csv("actual_percent.csv", header=False)
