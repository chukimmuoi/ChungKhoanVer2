import matplotlib.pyplot as plt
import pandas as pd

FOLDER_DATA_CSV_PATH = "../mining/data/"

DATE_COLUMN = "transDate"
CLOSE_COLUMN = "close"
OPEN_COLUMN = "open"
LOW_COLUMN = "low"
HIGH_COLUMN = "high"

X_LABEL = 'Thời gian'
Y_LABEL = 'Giá chứng khoán'


def stock_price(code=""):
    if code == "":
        print("Please input code name. Ex: MWG, ...")
        return

    df = pd.read_csv(FOLDER_DATA_CSV_PATH + code + ".csv")

    plot_df = df.set_index([DATE_COLUMN])
    plot_df[CLOSE_COLUMN].plot()
    plot_df[OPEN_COLUMN].plot()
    plot_df[LOW_COLUMN].plot()
    plot_df[HIGH_COLUMN].plot()

    plt.xlabel(X_LABEL)
    plt.ylabel(Y_LABEL)
    plt.title(code)

    plt.legend()
    plt.show()