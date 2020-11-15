from bs4 import BeautifulSoup
import requests
from utils.file import save_pandas_to_csv, convert_string_to_string_to_pandas
from utils.utils import convert_csv_to_pandas, CODE_COLUMN

DIRECTORY_NAME_CSV_DEFAULT = 'data'

START_JSON_VALUES = 'drawChartForFirstTime('
END_JSON_VALUES = ');'

URL_FORMAT = 'https://www.vndirect.com.vn/portal/bieu-do-ky-thuat/{}.shtml'


def mining_data_follow_code_name(code_name, out_directory=DIRECTORY_NAME_CSV_DEFAULT):
    string = get_string_json(code_name)
    result = convert_string_to_string_to_pandas(string)
    save_pandas_to_csv(result, code_name, out_directory)


def get_string_json(name_code):
    web_content = get_page_content(name_code)

    content_list = web_content.split(START_JSON_VALUES)

    if len(content_list) >= 2:
        string_json_list = content_list[1].split(END_JSON_VALUES)
        string_json = string_json_list[0]
        if string_json == '':
            raise Exception('Not find json string of ' + name_code)
    else:
        raise Exception('Not find json string of ' + name_code)

    return string_json


def get_page_content(name_code):
    url = get_url(name_code)

    page = requests.get(url, verify=True)
    page_content = BeautifulSoup(page.text, "html.parser")

    return str(page_content)


def get_url(name_code):
    url = URL_FORMAT.format(name_code)

    return url


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


mining_data_follow_code_name('MWG')
# mining_data_follow_code_file('code/code.csv')


