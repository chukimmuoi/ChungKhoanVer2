import pandas as pd
from pathlib import Path

from utils.utils import convert_csv_to_pandas, TRANS_DATE_COLUMN, CODE_COLUMN

FOLDER_DATA_CSV_PATH = "../mining/data/"
MA_CK_COLUMN = 'Ma CK'
CHU_KY_COLUMN = 'Chu ky'
START_COLUMN = 'Gia tri qua khu'
END_COLUMN = 'Gia tri hien tai'
TSSL_COLUMN = 'Ty suat sinh loi / nam'


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


def check_volume_value(data_frame,
                       day_not_work_percent):
    count_volume_lose = 0
    total_volume = 0
    for index, row in data_frame.iterrows():
        total_volume += 1
        volume = row['volume']
        if volume == 0:
            count_volume_lose += 1

    return (count_volume_lose / total_volume) <= day_not_work_percent


def calculator_tssl_f_code(df_out,
                           code="MWG",
                           kyvong_percent=0,
                           limit_min_chu_ky=0,
                           day_not_work_percent=0):
    if code == "":
        print("Please input code name. Ex: MWG, ...")
        return

    path = FOLDER_DATA_CSV_PATH + code + ".csv"
    file = Path(path)
    if file.is_file():
        df, fv, pv, n = get_data(code)
        if pv > 0 and n >= limit_min_chu_ky:
            r = ((fv / pv) ** (1 / n) - 1) * 100
            if r >= kyvong_percent and check_volume_value(df, day_not_work_percent):
                df_out = df_out.append(
                    {
                        MA_CK_COLUMN: code,
                        CHU_KY_COLUMN: n,
                        START_COLUMN: pv,
                        END_COLUMN: fv,
                        TSSL_COLUMN: r
                    },
                    ignore_index=True
                )
                print('code = {}, n = {}, pv = {}, fv = {}, r = {}'.format(code, n, pv, fv, r))

    return df_out


def tssl_f_year(path, kyvong_percent, limit_min_chu_ky, day_not_work_percent):
    data_frame = convert_csv_to_pandas(path)
    df_out = pd.DataFrame(columns=[MA_CK_COLUMN, CHU_KY_COLUMN, START_COLUMN, END_COLUMN, TSSL_COLUMN])
    for index, row in data_frame.iterrows():
        code = row[CODE_COLUMN]
        df_out = calculator_tssl_f_code(df_out,
                                        code,
                                        kyvong_percent,
                                        limit_min_chu_ky,
                                        day_not_work_percent)

    df_out = df_out.sort_values(by=[TSSL_COLUMN], ascending=False, ignore_index=True)
    df_out.to_csv('TSSL[kyvong={}][chu_ky={}][max_percent_not_work={}].csv'
                  .format(kyvong_percent, limit_min_chu_ky, day_not_work_percent))


tssl_f_year('../mining/code/code.csv', 20, 5, 0.2)
