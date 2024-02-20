import pandas as pd
import numpy as np

def get_harmonics_range(harmonics: pd.Series,
                        search_price: float,
                        diapozan_week: 'str'):

    sorted_series = harmonics.loc[diapozan_week].sort_values().copy()
#     if previous_price >= search_price:
#         sorted_series = sorted_series * (1 + margin_of_error)
#     else:
#         sorted_series = sorted_series * (1 - margin_of_error)
    index = sorted_series.searchsorted(search_price)

    # Get the minimum and maximum thresholds
    min_threshold = index-1
    max_threshold = index
    harmonics_range = sorted_series.iloc[min_threshold: max_threshold+1].index
    if not harmonics_range.empty:
        return harmonics_range[0] - 1
    return harmonics.columns.max()

def get_week2paths(harmonics,
                   es_df,
                   week_numbers,
                   week_number2diapazonweek,
                   window: int,
                   past_shift: int):
    """
        In: window - int - number of weeks forward to look forward
            past_shift - int - on how many "granularity" to shift prices from the past
                               to get direction of prices
        Out: at which diapazon look
    """

    week2path2count  = {week_number: {} for week_number in week_numbers}

    for week_number, diapazons_weeks in week_number2diapazonweek.items():
        for diapozon_week in diapazons_weeks:
            path = []

            start_date = es_df[
                (es_df['diapazan_week'] == diapozon_week) & (~es_df['is_diapazon_day'])
            ].index.min()
            end_date = start_date + pd.Timedelta(window, unit='w')

            future_prices = es_df.loc[start_date: end_date, 'close']
            for curr_price in future_prices:
                harmonic_number = get_harmonics_range(harmonics, curr_price, diapozon_week)
                path.append(harmonic_number)
            week2path2count[week_number][diapozon_week] = path
    return week2path2count

def get_total_weeks_pathes(week2path2count):
    total_pathes_df = pd.DataFrame()
    for _, path2count_dict in week2path2count.items():
        path2count_week = pd.Series(path2count_dict)
        pathes_df_week = (
            path2count_week.apply(pd.Series)
                .replace('', np.nan)
                .dropna(how='all', axis=1)
                .astype(float)
        )
        total_pathes_df = pd.concat([pathes_df_week, total_pathes_df], axis=0)
    total_pathes_df = total_pathes_df.sort_index()
    return total_pathes_df


def get_week_pathes(week2path2count, week: int):
    """
    """
    path2count_dict = week2path2count[week]
    path2count_week = pd.Series(path2count_dict)
    pathes_df_week = (
        path2count_week.apply(pd.Series)
            .replace('', np.nan)
            .dropna(how='all', axis=1)
            .astype(float)
    )
    return pathes_df_week
