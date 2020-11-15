from pathlib import Path
import pandas
import json

from utils.utils import TRANS_DATE_COLUMN, DATE_FORMAT


def create_directory(directory):
    Path(directory).mkdir(parents=True, exist_ok=True)


def save_pandas_to_csv(result, name_code, out_directory):
    create_directory(out_directory)

    result.to_csv(out_directory + '/' + name_code + ".csv", index=False)


def convert_string_to_json(string):
    return json.loads(string)


def convert_json_to_pandas(json_string, isMiningDayData=True):
    result = pandas.DataFrame(json_string)
    if isMiningDayData:
        result[TRANS_DATE_COLUMN] = pandas.to_datetime(result[TRANS_DATE_COLUMN], unit='ms').dt.strftime(DATE_FORMAT)

    return result


def convert_string_to_string_to_pandas(string, isMiningDayData=True):
    json_string = convert_string_to_json(string)
    result = convert_json_to_pandas(json_string, isMiningDayData)

    return result