import pandas as pd

data = pd.read_csv("synergy_logistics_database.csv")

# split data, imports and exports
export_data = data[data["direction"] == "Exports"]
import_data = data[data["direction"] == "Imports"]

# option one
# group data by route, compute sum and sort by total value

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

# option two
# group data by transport mode, compute sum and sort by total value
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
tmode_total = (tmode_import + tmode_export).sort_values(ascending=False)

# option tree
eighty_export = export_total[export_total.cumsum() <= export_total.sum() * 4 / 5]
actual_export_percent = round(eighty_export.sum() / export_total.sum() * 100, 1)

eighty_import = import_total[import_total.cumsum() <= import_total.sum() * 4 / 5]
actual_import_percent = round(eighty_import.sum() / import_total.sum() * 100, 1)


# save in csv file

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
