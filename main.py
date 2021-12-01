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
# print(tabulate(df, headers='keys', tablefmt='psql'))
df = p.cleaned_data
# pprint(df[df["Description"] == "WHITE HANGING HEART T-LIGHT HOLDER"])
p.build_matrix()
# print(p.final_matrix)



a = AssociationMining(0.6)
dataf = pd.DataFrame(data=p.final_matrix, columns=set(p.description_titles))

# FpGrowth
# print(a.fp_growth(dataf))

# Apriori
# frequent_itemsets = a.apriori(p.description_titles)
# print(frequent_itemsets)

# Association Rules
# print(a.rule_mining(p.description_titles,0.85))


# ---------------------


# te = TransactionEncoder()
# te_ary = te.fit(p.description_titles).transform(p.description_titles)
# daf = pd.DataFrame(te_ary, columns=te.columns_)
# frequent_itemsets = fpgrowth(daf, min_support=0.6, use_colnames=True)
# res = association_rules(frequent_itemsets, metric="confidence", min_threshold=0.7)
# print(res)

# ---------------------
# te = TransactionEncoder()
# te_ary = te.fit(p.description_titles).transform(p.description_titles)
# daaf = pd.DataFrame(te_ary, columns=te.columns_)
# ap = apriori(daaf, min_support=0.6)
# print()
# print(ap)


