from datetime import datetime
import pandas as pd
from statsmodels.tsa.seasonal import STL


def smoothCurve(data):
    arr = []
    for i in range(len(data)):
        if i == 0:
            arr.append(0)
            continue
        arr.append(data[i] - data[i-1])
    return arr


def STLDecomposition(csvData):
    initialDate = datetime.strptime(
        csvData.index[0], "%Y.%m.%d")
    convertedDate = initialDate.strftime("%d-%m-%Y")

    dict = {}

    for column in csvData.columns[:-1]:
        data = csvData[[column]]
        flat_arr = data.to_numpy().flatten()
        d = smoothCurve(flat_arr)
        series = pd.Series(d, index=pd.date_range(
            convertedDate, periods=len(d), freq='D'), name=column)
        stl = STL(series, seasonal=5, seasonal_deg=0,
                  trend_deg=0, low_pass_deg=0, robust=True)
        res = stl.fit()
        dict[column] = [res.trend.to_numpy(), res.seasonal.to_numpy(),
                        res.resid.to_numpy()]

    return dict['open'], dict['highest'], dict['lowest'], dict['close'], dict['volume']
