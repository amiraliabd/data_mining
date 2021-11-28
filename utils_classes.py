from typing import Optional
import pandas as pd
import pprint


class ProjectPreProcessing:

    def __init__(self, file_absolute_path):
        self.raw_data: Optional[pd.DataFrame] = None
        self.cleaned_data: Optional[pd.DataFrame] = None
        self.file_absolute_path = file_absolute_path
        self.description_titles = []
        self.final_matrix = []

    def read_data(self):
        self.raw_data = pd.read_csv(self.file_absolute_path)
        self.cleaned_data = self.raw_data
        return self.raw_data

    def reduction(self):
        df = self.cleaned_data

        useless_data_indexes = df[
            (df["Quantity"] < 0) |
            (df["StockCode"] >= "AAAAA") |
            (df["InvoiceNo"] >= "C00000") |
            (df["Description"].isnull())
        ].index
        self.cleaned_data = df.drop(useless_data_indexes)

    def _clean_string_column(self, attribute):
        self.cleaned_data[attribute] = self.cleaned_data[attribute].apply(lambda a: str(a).strip())
        # todo: it needs to be cleaned and improved for performance
        self.cleaned_data[attribute] = self.cleaned_data[attribute].apply(lambda a: a.replace(", ", ","))
        self.cleaned_data[attribute] = self.cleaned_data[attribute].apply(lambda a: a.replace(" ,", ","))

    def _integrate_rows(self) -> pd.Series:
        df = self.cleaned_data.astype(str)
        return df.groupby("InvoiceNo")["Description"].apply(",".join)

    def _gather_all_descriptions(self, value: str):
        value = str(value)

        if "," in value:
            self.description_titles.extend(value.split(","))
        else:
            self.description_titles.append(value)

    def build_matrix(self):
        matrix = []
        self._clean_string_column("Description")
        self.cleaned_data["Description"].apply(self._gather_all_descriptions)

        # for two reasons we will cast `self.description_titles` to set and then to a dictionary
        # 1- we need to remove duplicate values
        # 2- we will need to select values from this list many times and as we know selecting items
        #    in python list in O(n) and this list it a long one, So we cast it to dictionary to select
        #    values with O(1)

        description_title_table = {}
        for index, title in enumerate(set(self.description_titles)):
            description_title_table[title] = index

        count_of_all_titles = len(description_title_table)

        series_of_items_descriptions = self._integrate_rows()

        for items in series_of_items_descriptions:
            matrix.append([0 for _ in range(count_of_all_titles)])
            for each_item in items.split(","):

                if not description_title_table.get(each_item):
                    # todo: we have empty values here
                    print(type(each_item))
                    print("shit")

                matrix[-1][description_title_table.get(each_item)] = 1

        self.final_matrix = matrix
