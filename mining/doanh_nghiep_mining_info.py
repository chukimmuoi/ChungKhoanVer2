from bs4 import BeautifulSoup
import requests

from utils.file import convert_string_to_string_to_pandas, save_pandas_to_csv
from utils.utils import convert_csv_to_pandas, CODE_COLUMN

URL_FORMAT = 'https://www.vndirect.com.vn/portal/tong-quan/{}.shtml'
DIRECTORY_NAME_CSV_DEFAULT = 'doanhnghiep'


def mining_info_doanh_nghiep_folow_code(code, out_directory=DIRECTORY_NAME_CSV_DEFAULT):
    page = requests.get(URL_FORMAT.format(code), verify=True)
    soup = BeautifulSoup(page.text, "html.parser")
    doanh_nghiep = soup.find_all('div', class_='content_doanhnghiep')
    content_left = doanh_nghiep[0].find_all('div', class_='content_left')

    column_statistic_1 = str(content_left[0].find('div', class_='width255'))
    column_statistic_1_json = column_statistic_1 \
        .replace('\n', '') \
        .replace(' ', '') \
        .replace('	', '') \
        .replace('<divclass="width255">', '') \
        .replace('<ulclass="list14">', '{') \
        .replace('<li>', '') \
        .replace('<divclass="rowa">', '\"') \
        .replace('</div>', '\"') \
        .replace('<divclass="rowc">', ':\"') \
        .replace('\"</li>', '\",') \
        .replace(',</ul>\"', '}')

    column_statistic_2 = str(content_left[0].find('div', class_='width190'))
    column_statistic_2_json = column_statistic_2 \
        .replace('\n', '') \
        .replace(' ', '') \
        .replace('	', '') \
        .replace('<divclass="width190">', '') \
        .replace('<ulclass="list14">', '{') \
        .replace('<li>', '') \
        .replace('<divclass="rowb">', '\"') \
        .replace('</div>', '\"') \
        .replace('<divclass="rowc">', ':\"') \
        .replace('\"</li>', '\",') \
        .replace(',</ul>\"', '}')

    doanh_nghiep_data_info_string = '[{}{}]'.format(column_statistic_1_json, column_statistic_2_json) \
        .replace('}{', ',')

    result = convert_string_to_string_to_pandas(doanh_nghiep_data_info_string, False)
    save_pandas_to_csv(result, code, out_directory)


def mining_info_doanh_nghiep_folow_file(path):
    passed = 0
    failed = 0

    data_frame = convert_csv_to_pandas(path)
    for index, row in data_frame.iterrows():
        code = row[CODE_COLUMN]
        try:
            mining_info_doanh_nghiep_folow_code(code)
            passed += 1
            print('index = {}, code name = {}'.format(index, code))
        except Exception as error:
            failed += 1
            print('index = {}, code name = {}, error = {}'.format(index, code, error))
    print('passed = {}, failed = {}'.format(passed, failed))  # passed = 1344, failed = 607


# mining_info_doanh_nghiep_folow_code('MWG')
mining_info_doanh_nghiep_folow_file('code/code.csv')
