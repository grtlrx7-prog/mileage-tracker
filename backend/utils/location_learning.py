import pandas as pd


# =================================================
# DETECT HOME
# =================================================

def detect_home(df):

    try:

        # Night trips
        night_df = df[
            (
                pd.to_datetime(
                    df["Start Time"]
                ).dt.hour >= 18
            )
            |
            (
                pd.to_datetime(
                    df["Start Time"]
                ).dt.hour <= 6
            )
        ]

        if night_df.empty:
            return "Unknown"

        home = (
            night_df["From"]
            .mode()[0]
        )

        return home

    except:

        return "Unknown"


# =================================================
# DETECT WORK
# =================================================

def detect_work(df, home):

    try:

        weekday_df = df[
            pd.to_datetime(
                df["Start Time"]
            ).dt.weekday < 5
        ]

        weekday_df = weekday_df[
            weekday_df["From"] != home
        ]

        if weekday_df.empty:
            return "Unknown"

        work = (
            weekday_df["To"]
            .mode()[0]
        )

        return work

    except:

        return "Unknown"