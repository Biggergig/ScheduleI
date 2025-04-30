import pandas as pd

convert_money = lambda s: float(s.replace("$", "")) if s else None
df = pd.read_csv(
    "data.csv",
    delimiter="\t",
    converters={
        col: convert_money
        for col in (
            "Market Value",
            "Ingredient Price",
            "Market Value",
            "Bill of Materials",
            "Net Profit",
            "ROI Net Profit",
            "Net profit per step",
        )
    },
)

# print(df)
df = df.merge(
    df[["Name", "Net Profit"]],
    left_on="From",
    right_on="Name",
    how="left",
)


# print(df["Net Profit"].sum())
ing_df = (
    (
        df[["Ingredient"]]
        .assign(Increase=df["Net Profit_x"] - df["Net Profit_y"])
        .dropna()
    )
    .sort_values("Increase", ascending=False)
    .merge(df[["Ingredient #"]], left_index=True, right_index=True)
)
# print(ing_df)

recipies = {"Meth": []}
# prices = df[["Name_x", "Net Profit_x"]].reset_index(drop=True).to_dict()
prices = dict(zip(df["Name_x"], df["Net Profit_x"]))
print(prices)

for row in list(df.itertuples())[1:]:
    recipies[row.Name_x] = recipies[row.From] + [row.Ingredient]
print(recipies)

enc_df = pd.DataFrame([[prices[name], recipies[name]] for name in recipies])
print(pd.get_dummies(enc_df[1]))
