def aggregate_monthly_sales(df):

    monthly_sales = df.groupby(
        ["Customer Name", "order_month"],
        as_index=False
    ).agg(
        monthly_sales=("Sales", "sum"),
        monthly_quantity=("Quantity", "sum")
    )

    return monthly_sales


    def create_historical_features(df):
        