import pandas as pd


class BasePreProcessing:

    def __init__(self, file_absolute_path):
        self.raw_data: pd.DataFrame = None
        self.cleaned_data: pd.DataFrame = None
        self.file_absolute_path = file_absolute_path

    def read_data(self):
        self.raw_data = pd.read_csv(self.file_absolute_path)
        self.cleaned_data = self.raw_data
        return self.raw_data

    def reduction(self, pair_data: dict):
        for attribute, value in pair_data.items():

            useless_data_indexes = self.cleaned_data[self.cleaned_data[attribute] == value].index
            self.cleaned_data = self.cleaned_data.drop(useless_data_indexes)


class ProjectPreProcessing(BasePreProcessing):

    def reduction(self, pair_data: dict):
        super(ProjectPreProcessing, self).reduction(pair_data)

        df = self.cleaned_data
        useless_data_indexes = df[
            (df["Quantity"] < 0) | (df["StockCode"] >= "AAAAA")
        ].index
        self.cleaned_data = df.drop(useless_data_indexes)

        return self.cleaned_data

    def _integrate_rows(self):
        df = self.cleaned_data.astype(str)
        return df.groupby("InvoiceNo")["Description"].apply(",".join)
