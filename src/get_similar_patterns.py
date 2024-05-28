from collections import defaultdict
import pandas as pd
import numpy as np


def get_rowinit2freq(resistance_support_cleaned_df: pd.DataFrame, min_count: int):
    rowinit2freq = defaultdict(int)
    rowinit2full = {}

    for idx, row in resistance_support_cleaned_df.iterrows():
        row = row.dropna().tolist()
        for idx in list(range(0, len(row))):
            if idx < 2:
                continue
            part_row = row[idx-2: idx+1]
            initial_path = '_'.join(part_row[:2])

            if part_row and len(part_row) > 2:
                if initial_path not in rowinit2full.keys():
                    rowinit2full[initial_path] = defaultdict(int)
                rowinit2freq[initial_path] += 1

                end_harmonic = int(part_row[2][:-1])
                rowinit2full[initial_path][end_harmonic] += 1
    rowinit2freq = pd.Series(rowinit2freq).sort_values(ascending=False)
    return rowinit2freq

def get_row_init_prob_df(resistance_support_cleaned_df: pd.DataFrame, min_count: int):
    rowinit2freq = defaultdict(int)
    rowinit2full = {}

    for idx, row in resistance_support_cleaned_df.iterrows():
        row = row.dropna().tolist()
        for idx in list(range(0, len(row))):
            if idx < 2:
                continue
            part_row = row[idx-2: idx+1]
            initial_path = '_'.join(part_row[:2])

            if part_row and len(part_row) > 2:
                if initial_path not in rowinit2full.keys():
                    rowinit2full[initial_path] = defaultdict(int)
                rowinit2freq[initial_path] += 1

                end_harmonic = int(part_row[2][:-1])
                rowinit2full[initial_path][end_harmonic] += 1

    rowinit2freq = pd.Series(rowinit2freq).sort_values(ascending=False)

    rowinit2full_df = pd.DataFrame(rowinit2full).T
    rowinit2full_df = rowinit2full_df.loc[rowinit2freq.index].fillna(0)
    rowinit2full_df['sum'] = rowinit2freq
    rowinit2full_df = rowinit2full_df[rowinit2full_df['sum'] > min_count]

    min_harmonic = rowinit2full_df.drop('sum', axis=1).columns.min()
    max_harmonic = rowinit2full_df.drop('sum', axis=1).columns.max()
    harmonic_cols = np.arange(min_harmonic, max_harmonic+1)
    harmonic_cols = rowinit2full_df.columns.intersection(harmonic_cols)
    rowinit2_prob_df = rowinit2full_df[harmonic_cols] / rowinit2full_df['sum'].values[:, None]
    return rowinit2_prob_df
    