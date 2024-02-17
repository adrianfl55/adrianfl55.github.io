from datetime import datetime
import pandas as pd


def consumptions_csv_to_df(path: str = "dataset/consumptions.csv") -> pd.DataFrame:
    consumptions = pd.read_csv(path, delimiter=";")

    # Crear campo de fecha y hora
    consumptions["Fecha_Hora"] = pd.to_datetime(
        consumptions["Fecha"] + " " + (consumptions["Hora"] - 1).astype(str) + ":00:00",
        format="%d/%m/%Y %H:%M:%S",
    )

    # Eliminar campos de fecha y hora
    consumptions = consumptions.drop(columns=["Fecha", "Hora"])

    return consumptions


def consumptions_csv_to_dict(path: str = "dataset/consumptions.csv") -> dict:

    consumptions = {}

    with open(path, "r") as f:
        data = f.readlines()

    for line in data[1:]:
        cups, fecha, hora, kWh, metodo = line.strip().split(";")

        fecha = fecha.split("/")[::-1]

        fechahora = datetime.strptime(
            f"{fecha[0]}-{fecha[1]}-{fecha[2]} {int(hora)-1}:00:00", "%Y-%m-%d %H:%M:%S"
        )

        consumptions[fechahora.timestamp()] = float(kWh.replace(",", "."))

    return consumptions