from typing import Optional
import pandas as pd
from mlxtend.frequent_patterns import fpgrowth, association_rules, apriori
from mlxtend.preprocessing import TransactionEncoder


class PreProcessing:

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

    @staticmethod
    def _clean_colons(obj):
        obj = str(obj)
        list_obj = obj.split(",")

        for index in range(len(list_obj)):
            list_obj[index] = list_obj[index].strip()

        obj = ",".join(list_obj)

        obj.replace(",,", ",")

        if obj[-1] == ",":
            obj = obj[:-1]

        return obj

    def _clean_string_column(self, attribute):
        self.cleaned_data[attribute] = self.cleaned_data[attribute].apply(self._clean_colons)

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
                matrix[-1][description_title_table.get(each_item)] = 1

        self.final_matrix = matrix


from mlxtend.frequent_patterns import fpgrowth


class AssociationMining:
    def __init__(self, min_support):
        self.min_support = min_support
        self.growth_result = None
        self.apriori_result = None

    def fp_growth(self, df, use_colnames=None):
        return fpgrowth(df, self.min_support, use_colnames=use_colnames)

    def apriori(self, description_titles):
        te = TransactionEncoder()
        te_ary = te.fit(description_titles).transform(description_titles)
        df = pd.DataFrame(te_ary, columns=te.columns_)
        result = apriori(df, min_support=self.min_support)
        return result

    def rule_mining(self, description_titles, min_threshold):
        te = TransactionEncoder()
        te_ary = te.fit(description_titles).transform(description_titles)
        df = pd.DataFrame(te_ary, columns=te.columns_)
        frequent_itemsets = self.fp_growth(df, use_colnames=True)
        res = association_rules(frequent_itemsets, metric="confidence", min_threshold=min_threshold)
        return res
