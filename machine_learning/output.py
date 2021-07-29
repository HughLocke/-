import pandas as pd
def Output(PATH):
    data = pd.read_csv(PATH)
    data.to_excel(PATH)

if __name_ == "__main__":
    Output("../data/Account.csv")