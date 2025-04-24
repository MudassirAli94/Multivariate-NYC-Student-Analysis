from tabulate import tabulate
import pandas as pd
import warnings
warnings.filterwarnings("ignore")
def print_df(df,rows=None):
    if rows is None:
        print(tabulate(df.head(),headers=list(df.columns),tablefmt="double_grid"))
    else:
        print(tabulate(df.head(rows), headers=list(df.columns),tablefmt="double_grid"))