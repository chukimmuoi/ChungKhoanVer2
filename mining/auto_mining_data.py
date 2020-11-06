from bs4 import BeautifulSoup
import pandas
import requests
import json
from pathlib import Path

DIRECTORY_NAME_CSV_DEFAULT = 'data'

START_JSON_VALUES = 'drawChartForFirstTime('
END_JSON_VALUES = ');'

URL_FORMAT = 'https://www.vndirect.com.vn/portal/bieu-do-ky-thuat/{}.shtml'
DATE_FORMAT = '%d/%m/%Y'

TRANS_DATE_COLUMN = 'transDate'
CODE_COLUMN = 'code'


def mining_data_follow_code_name(code_name, out_directory=DIRECTORY_NAME_CSV_DEFAULT):
    json_string = get_json_string(code_name)
    result = convert_json_to_pandas(json_string)
    save_pandas_to_csv(result, code_name, out_directory)


def get_json_string(name_code):
    web_content = get_page_content(name_code)

    content_list = web_content.split(START_JSON_VALUES)

    if len(content_list) >= 2:
        json_string_list = content_list[1].split(END_JSON_VALUES)
        json_string = json.loads(json_string_list[0])
        if json_string == '':
            raise Exception('Not find json string of ' + name_code)
    else:
        raise Exception('Not find json string of ' + name_code)

    return json_string


def convert_json_to_pandas(json_string):
    result = pandas.DataFrame(json_string)
    result[TRANS_DATE_COLUMN] = pandas.to_datetime(result[TRANS_DATE_COLUMN], unit='ms').dt.strftime(DATE_FORMAT)

    return result


def save_pandas_to_csv(result, name_code, out_directory):
    create_directory(out_directory)

    result.to_csv(out_directory + '/' + name_code + ".csv", index=False)


def get_page_content(name_code):
    url = get_url(name_code)

    page = requests.get(url, verify=True)
    page_content = BeautifulSoup(page.text, "html.parser")

    return str(page_content)


def get_url(name_code):
    url = URL_FORMAT.format(name_code)

    return url


def create_directory(directory):
    Path(directory).mkdir(parents=True, exist_ok=True)


def mining_data_follow_code_file(path):
    passed = 0
    failed = 0

    data_frame = convert_csv_to_pandas(path)
    for index, row in data_frame.iterrows():
        code = row[CODE_COLUMN]
        try:
            mining_data_follow_code_name(code)
            passed += 1
            print('index = {}, code name = {}'.format(index, code))
        except Exception as error:
            failed += 1
            print('index = {}, code name = {}, error = {}'.format(index, code, error))
    print('passed = {}, failed = {}'.format(passed, failed))  # passed = 1344, failed = 607


def convert_csv_to_pandas(path):
    data_frame = pandas.read_csv(path)

    return data_frame


mining_data_follow_code_file('code/code.csv')


