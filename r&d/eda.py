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

print(df)
df = df.merge(
    df[["Name", "Net Profit"]],
    left_on="From",
    right_on="Name",
    how="left",
)


# print(df["Net Profit"].sum())
ing_df = (
    df[["Ingredient"]].assign(Increase=df["Net Profit_x"] - df["Net Profit_y"]).dropna()
)
print(ing_df)
