import pandas as pd
from pathlib import Path

from utils.utils import convert_csv_to_pandas, TRANS_DATE_COLUMN, CODE_COLUMN

FOLDER_DATA_CSV_PATH = "../mining/data/"


def get_data(code='MWG'):
    df = pd.read_csv(FOLDER_DATA_CSV_PATH + code + ".csv")
    head = df.head(1)
    tail = df.tail(1)

    close_start = float(head['close'].to_string(index=False))
    year_start = int(head[TRANS_DATE_COLUMN].to_string(index=False).split('/')[2])

    close_end = float(tail['close'].to_string(index=False))
    year_end = int(tail[TRANS_DATE_COLUMN].to_string(index=False).split('/')[2])

    n = year_end - year_start + 1

    return df, close_end, close_start, n


def check_volume_value(data_frame):
    count_volume_lose = 0
    total_volume = 0
    for index, row in data_frame.iterrows():
        total_volume += 1
        volume = row['volume']
        if volume == 0:
            count_volume_lose += 1

    return (count_volume_lose / total_volume) <= 0.2


def calculator_tssl_f_code(code="MWG", limit=0):
    if code == "":
        print("Please input code name. Ex: MWG, ...")
        return

    path = FOLDER_DATA_CSV_PATH + code + ".csv"
    file = Path(path)
    if file.is_file():
        df, fv, pv, n = get_data(code)
        if pv > 0 and n >= 5:
            r = ((fv / pv) ** (1 / n) - 1) * 100
            if r >= limit and check_volume_value(df):
                print('code = {}, n = {}, pv = {}, fv = {}, r = {}'.format(code, n, pv, fv, r))


def tssl_f_year(path, limit):
    data_frame = convert_csv_to_pandas(path)
    for index, row in data_frame.iterrows():
        code = row[CODE_COLUMN]
        calculator_tssl_f_code(code, limit)


tssl_f_year('../mining/code/code.csv', 20)
