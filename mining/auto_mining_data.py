from bs4 import BeautifulSoup
import pandas
import requests
import json
from pathlib import Path


def mining_data_follow_code_name(code_name, out_directory='data'):
    json_string = get_json_string(code_name)
    result = convert_json_to_pandas(json_string)
    save_pandas_to_csv(result, code_name, out_directory)


def get_json_string(name_code):
    web_content = get_page_content(name_code)

    content_list = web_content.split('drawChartForFirstTime(')

    if len(content_list) >= 2:
        json_string_list = content_list[1].split(');')
        json_string = json.loads(json_string_list[0])
    else:
        print('Not find json string of ' + name_code)

    return json_string


def convert_json_to_pandas(json_string):
    result = pandas.DataFrame(json_string)
    result['transDate'] = pandas.to_datetime(result['transDate'], unit='ms').dt.strftime('%d/%m/%Y')

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
    url = 'https://www.vndirect.com.vn/portal/bieu-do-ky-thuat/' + name_code + '.shtml'

    return url


def create_directory(directory):
    Path(directory).mkdir(parents=True, exist_ok=True)


mining_data_follow_code_name('MWG')


