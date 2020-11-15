import pandas

TRANS_DATE_COLUMN = 'transDate'
CODE_COLUMN = 'code'

DATE_FORMAT = '%d/%m/%Y'


def convert_csv_to_pandas(path):
    data_frame = pandas.read_csv(path)

    return data_frame