from utils_classes import PreProcessing, AssociationMining
import os
import pandas as pd
from mlxtend.frequent_patterns import fpgrowth, association_rules, apriori
from mlxtend.preprocessing import TransactionEncoder


from pprint import pprint
from tabulate import tabulate

path = os.path.abspath('example_data.csv')
p = PreProcessing(path)
p.read_data()
p.reduction()
p.build_matrix()
df = pd.DataFrame(data=p.final_matrix, columns=set(p.description_titles))


a = AssociationMining(0.05, df)

# FpGrowth
print("processing data with FPGrowth algorithm")
fi1 = a.fp_growth()
print(fi1)

# Apriori
print("processing data with apriori algorithm")
fi2 = a.apriori()
print(fi2)

# Association Rules
print("rule mining")
print(a.rule_mining(min_threshold=0.85, fi=fi1))
print(a.rule_mining(min_threshold=0.85, fi=fi2))


