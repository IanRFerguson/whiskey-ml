def model(dbt, session):
    df = dbt.ref("stg__long")
    df["test"] = True

    return df
