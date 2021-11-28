from utils_classes import ProjectPreProcessing
import os
import pandas as pd
from pprint import pprint
from tabulate import tabulate


path = os.path.abspath('example_data.csv')
p = ProjectPreProcessing(path)
p.read_data()
p.reduction()
# print(tabulate(df, headers='keys', tablefmt='psql'))
df = p.cleaned_data
# pprint(df[df["Description"] == "WHITE HANGING HEART T-LIGHT HOLDER"])
p.build_matrix()
print(p.final_matrix)